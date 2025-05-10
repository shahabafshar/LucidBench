#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Clear screen
clear

# Display ASCII art
echo -e "${BLUE}"
cat << "EOF"
██╗     ██╗   ██╗ ██████╗██╗██████╗     ██████╗ ███████╗███╗   ██╗ ██████╗██╗  ██╗
██║     ██║   ██║██╔════╝██║██╔══██╗    ██╔══██╗██╔════╝████╗  ██║██╔════╝██║  ██║
██║     ██║   ██║██║     ██║██║  ██║    ██████╔╝█████╗  ██╔██╗ ██║██║     ███████║
██║     ██║   ██║██║     ██║██║  ██║    ██╔══██╗██╔══╝  ██║╚██╗██║██║     ██╔══██║
███████╗╚██████╔╝╚██████╗██║██████╔╝    ██████╔╝███████╗██║ ╚████║╚██████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝
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
"${PROJECT_ROOT}/scripts/orchestrator.sh" "$@" 