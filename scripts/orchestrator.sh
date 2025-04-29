#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}This script must be run as root${NC}"
    exit 1
fi

# Create required directories
mkdir -p "${PROJECT_ROOT}/results" "${PROJECT_ROOT}/monitoring"

# Function to handle cleanup
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    
    # Stop any running containers
    docker ps -q --filter "name=lucidbench" | xargs -r docker stop
    
    # Unmount any mounted devices
    mount | grep "/mnt/benchmark" | awk '{print $3}' | xargs -r umount
    
    # Stop monitoring
    python3 "${PROJECT_ROOT}/src/monitoring/monitor.py" stop_monitoring
    
    echo -e "${GREEN}Cleanup complete${NC}"
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Function to run setup script
run_setup() {
    echo -e "\n${YELLOW}Running setup script...${NC}"
    "${PROJECT_ROOT}/scripts/setup.sh"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Setup failed${NC}"
        exit 1
    fi
}

# Function to build Docker image
build_docker_image() {
    echo -e "\n${YELLOW}Building Docker image...${NC}"
    cd "${PROJECT_ROOT}"
    docker build -t lucidbench -f config/Dockerfile .
    if [ $? -ne 0 ]; then
        echo -e "${RED}Docker build failed${NC}"
        exit 1
    fi
}

# Function to run benchmark for a device
run_benchmark() {
    local device=$1
    local filesystem=$2
    local device_type=$3
    local test_type=$4
    local run_dir=$5
    
    echo -e "\n${YELLOW}Running benchmark for ${device} with ${filesystem} (${test_type})${NC}"
    
    # Create test directory
    local test_dir="${run_dir}/${device_type}_${device}_${filesystem}_${test_type}"
    mkdir -p "$test_dir"
    
    # Start system monitoring
    python3 "${PROJECT_ROOT}/src/monitoring/monitor.py" \
        "${test_dir}/monitoring.json" \
        "$device_type" \
        "$device" \
        "$filesystem" \
        "$test_type" &
    monitor_pid=$!
    
    # Wait for monitoring to start
    sleep 2
    
    # Run benchmark container
    docker run --rm \
        --name lucidbench \
        --privileged \
        -v "$test_dir:/results" \
        -v "/dev/${device}:/dev/benchmark" \
        lucidbench \
        /dev/benchmark \
        "$filesystem" \
        "/results/test.json" \
        "$device_type" \
        "$device" \
        "$test_type"
    
    # Stop system monitoring
    kill $monitor_pid
    wait $monitor_pid 2>/dev/null
}

# Main execution
echo -e "${GREEN}LucidBench Orchestrator${NC}"
echo "======================="

# Parse arguments
USE_ALL=0
if [[ "$1" == "--all" ]]; then
    USE_ALL=1
    shift
fi

# Run setup
run_setup

# Build Docker image
build_docker_image

# Detect devices
echo -e "\n${YELLOW}Detecting devices...${NC}"
python3 "${PROJECT_ROOT}/src/core/device_detector.py" > "${PROJECT_ROOT}/device_info.json" 2> "${PROJECT_ROOT}/device_detection_error.log"

# Check if device detection was successful
if [ ! -s "${PROJECT_ROOT}/device_info.json" ]; then
    echo -e "${RED}Error: Device detection failed or no output was produced${NC}"
    if [ -s "${PROJECT_ROOT}/device_detection_error.log" ]; then
        echo -e "${YELLOW}Error details:${NC}"
        cat "${PROJECT_ROOT}/device_detection_error.log"
    fi
    cleanup
    exit 1
fi

# Read detected storage categories
STORAGE_CATEGORIES=$(python3 -c "import json; f=open('${PROJECT_ROOT}/device_info.json'); d=json.load(f); print(', '.join([k for k,v in d['free_devices_by_type'].items() if v]))")

# Read filesystems from config
FILESYSTEMS=()
while IFS= read -r fs; do
    [ -n "$fs" ] && FILESYSTEMS+=("$fs")
done < "${PROJECT_ROOT}/config/filesystems.txt"
FILESYSTEMS_LIST=$(IFS=, ; echo "${FILESYSTEMS[*]}")

# Define test types
TEST_TYPES="random_read, random_write, sequential_read, sequential_write"

# Show summary and prompt user
clear

echo -e "${YELLOW}Detected Storage Categories:${NC} $STORAGE_CATEGORIES"
echo -e "${YELLOW}Configured Filesystems:${NC} $FILESYSTEMS_LIST"
echo -e "${YELLOW}Test Types:${NC} $TEST_TYPES"
echo
read -p "Do you want to continue with these settings? (y/n): " CONTINUE
if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
    echo -e "${RED}Aborting as per user request.${NC}"
    cleanup
    exit 0
fi

# Create run directory
RUN_ID=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="${PROJECT_ROOT}/results/run_${RUN_ID}"
mkdir -p "$RUN_DIR"

# Read device information
devices_found=0
for device_type in "HDD" "SSD" "NVMe"; do
    devices=$(python3 -c "
import json
try:
    with open('${PROJECT_ROOT}/device_info.json') as f:
    data = json.load(f)
        devices = data['free_devices_by_type'].get('$device_type', [])
        print(' '.join(devices))
except Exception as e:
    import sys
    print(f'Error reading device info: {e}', file=sys.stderr)
    sys.exit(1)
")
    
    if [ -n "$devices" ]; then
        echo -e "\n${GREEN}Testing ${device_type} devices: ${devices}${NC}"
        devices_found=1
        
        # If not using all devices, take only the first one
        if [ $USE_ALL -eq 0 ]; then
            devices=$(echo $devices | awk '{print $1}')
        fi
        
        for device in $devices; do
            for filesystem in "${FILESYSTEMS[@]}"; do
                for test_type in "random_read" "random_write" "sequential_read" "sequential_write"; do
                    run_benchmark "$device" "$filesystem" "$device_type" "$test_type" "$RUN_DIR"
                done
            done
        done
    else
        echo -e "\n${YELLOW}No ${device_type} devices found${NC}"
    fi
done

if [ $devices_found -eq 0 ]; then
    echo -e "\n${RED}No devices available for benchmarking${NC}"
    echo "Please ensure you have unformatted block devices available"
    cleanup
    exit 1
fi

echo -e "\n${GREEN}Benchmarking complete${NC}"
echo "Results are available in: $RUN_DIR"

# Cleanup
cleanup 