#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "LucidBench Orchestrator Setup"
echo "============================"

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}✗ $1 is not installed${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 is installed${NC}"
        return 0
    fi
}

# Function to check if a package is installed
check_package() {
    if ! dpkg -l | grep -q "^ii  $1 "; then
        echo -e "${RED}✗ $1 package is not installed${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $1 package is installed${NC}"
        return 0
    fi
}

# Function to install package
install_package() {
    echo -e "${YELLOW}Installing $1...${NC}"
    apt-get install -y $1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 installed successfully${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to install $1${NC}"
        return 1
    fi
}

# Check for root access
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}✗ This script must be run as root${NC}"
    exit 1
fi

# Update package lists
echo -e "\nUpdating package lists..."
apt-get update

# Check and install required commands
echo -e "\nChecking and installing required commands..."
required_commands=("docker" "lsblk" "smartctl" "iostat" "vmstat" "fio")
missing_commands=0

for cmd in "${required_commands[@]}"; do
    if ! check_command $cmd; then
        case $cmd in
            "docker")
                echo -e "${YELLOW}Installing Docker...${NC}"
                curl -fsSL https://get.docker.com -o get-docker.sh
                sh get-docker.sh
                rm get-docker.sh
                ;;
            "smartctl")
                install_package "smartmontools"
                ;;
            "iostat"|"vmstat")
                install_package "sysstat"
                ;;
            "fio")
                install_package "fio"
                ;;
        esac
    if ! check_command $cmd; then
        missing_commands=1
        fi
    fi
done

# Check required packages
echo -e "\nChecking required packages..."
required_packages=(
    "smartmontools"
    "sysstat"
    "python3"
    "python3-pip"
    "python3-venv"
    "python3-setuptools"
    "python3-numpy"
    "python3-psutil"
)
missing_packages=0

for pkg in "${required_packages[@]}"; do
    if ! check_package $pkg; then
        if ! install_package $pkg; then
        missing_packages=1
        fi
    fi
done

# Check Docker service
echo -e "\nChecking Docker service..."
if ! systemctl is-active --quiet docker; then
    echo -e "${RED}✗ Docker service is not running${NC}"
    echo -e "${YELLOW}Starting Docker service...${NC}"
    systemctl start docker
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Docker service started successfully${NC}"
    else
        echo -e "${RED}✗ Failed to start Docker service${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Docker service is running${NC}"
fi

# Create required directories
echo -e "\nCreating required directories..."
mkdir -p "${PROJECT_ROOT}/results" "${PROJECT_ROOT}/monitoring"

# Set permissions
chmod 755 "${PROJECT_ROOT}/results" "${PROJECT_ROOT}/monitoring"

# Create Python requirements file if it doesn't exist
if [ ! -f "${PROJECT_ROOT}/config/requirements.txt" ]; then
    echo -e "\nCreating requirements.txt..."
    cat > "${PROJECT_ROOT}/config/requirements.txt" << EOL
numpy>=1.24.0
psutil>=5.9.0
EOL
fi

# Summary
echo -e "\nSetup Summary:"
if [ $missing_commands -eq 0 ] && [ $missing_packages -eq 0 ]; then
    echo -e "${GREEN}✓ All requirements are met${NC}"
    echo -e "You can now run the orchestrator with: sudo ${PROJECT_ROOT}/scripts/orchestrator.sh"
else
    echo -e "${RED}✗ Some requirements are missing${NC}"
    echo -e "Please install the missing components and run this script again"
    exit 1
fi 