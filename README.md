# LucidBench Orchestrator

A Docker-based filesystem benchmarking tool that automates the testing of different filesystems across various storage devices.

## Features

- Automatic device detection and classification (HDD, SATA SSD, NVMe SSD)
- Support for multiple filesystem types (ext4, xfs, btrfs)
- Real-time system resource monitoring
- Docker-based benchmark execution
- Immediate result logging and monitoring

## Prerequisites

- Linux-based operating system
- Docker installed and running
- Root/sudo access for device operations
- Required system tools:
  - lsblk
  - smartctl (smartmontools)
  - iostat (sysstat)
  - vmstat
  - fio

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/lucidbench-orchestrator.git
cd lucidbench-orchestrator
```

2. Run the setup script to verify requirements:
```bash
sudo ./scripts/setup.sh
```

3. Build the Docker image:
```bash
docker build -t lucidbench ./config
```

## Usage

Run the orchestrator:
```bash
sudo ./scripts/orchestrator.sh
```

Results will be saved in the `results` directory, organized by device type and filesystem.

## Project Structure

```
lucidbench-orchestrator/
├── config/
│   ├── Dockerfile
│   └── requirements.txt
├── scripts/
│   ├── orchestrator.sh
│   └── setup.sh
├── src/
│   ├── benchmark/
│   │   └── benchmark.py
│   ├── core/
│   │   └── device_detector.py
│   ├── monitoring/
│   │   └── monitor.py
│   └── utils/
├── results/
├── monitoring/
└── README.md
```

## License

MIT License 