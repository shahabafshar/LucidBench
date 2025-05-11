#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Clear screen
clear

# Display ASCII art
echo -e "${CYAN}"
cat << "EOF"
██╗     ██╗   ██╗ ██████╗██╗██████╗  ██████╗ ███████╗███╗   ██╗ ██████╗██╗  ██╗
██║     ██║   ██║██╔════╝██║██╔══██╗ ██╔══██╗██╔════╝████╗  ██║██╔════╝██║  ██║
██║     ██║   ██║██║     ██║██║  ██║ ██████╔╝█████╗  ██╔██╗ ██║██║     ███████║
██║     ██║   ██║██║     ██║██║  ██║ ██╔══██╗██╔══╝  ██║╚██╗██║██║     ██╔══██║
███████╗╚██████╔╝╚██████╗██║██████╔╝ ██████╔╝███████╗██║ ╚████║╚██████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝
EOF
echo -e "${NC}"

# Display welcome message
echo -e "${GREEN}Welcome to LucidBench!${NC}"
echo -e "${YELLOW}A Docker-based filesystem benchmarking tool${NC}"
echo -e "${BLUE}===========================================${NC}\n"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}This script must be run as root${NC}"
    exit 1
fi

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the orchestrator
echo -e "${YELLOW}Starting LucidBench Orchestrator...${NC}\n"
# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}Error: tmux is not installed${NC}"
    exit 1
fi

# Create logs directory if it doesn't exist
LOGS_DIR="${PROJECT_ROOT}/logs"
mkdir -p "$LOGS_DIR"

# Generate timestamp for log file
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOGS_DIR}/lucidbench_${TIMESTAMP}.log"

# Create a new tmux session named 'lucidbench' if it doesn't exist
if ! tmux has-session -t lucidbench 2>/dev/null; then
    tmux new-session -d -s lucidbench
fi

# Start logging the session
tmux pipe-pane -t lucidbench "cat >> ${LOG_FILE}"

# Run the orchestrator in the tmux session
tmux send-keys -t lucidbench "${PROJECT_ROOT}/scripts/orchestrator.sh $*" C-m

# Attach to the tmux session
tmux attach-session -t lucidbench