# LucidBench: Docker Benchmark Framework

## About

```
██╗     ██╗   ██╗ ██████╗██╗██████╗     ██████╗ ███████╗███╗   ██╗ ██████╗██╗  ██╗
██║     ██║   ██║██╔════╝██║██╔══██╗    ██╔══██╗██╔════╝████╗  ██║██╔════╝██║  ██║
██║     ██║   ██║██║     ██║██║  ██║    ██████╔╝█████╗  ██╔██╗ ██║██║     ███████║
██║     ██║   ██║██║     ██║██║  ██║    ██╔══██╗██╔══╝  ██║╚██╗██║██║     ██╔══██║
███████╗╚██████╔╝╚██████╗██║██████╔╝    ██████╔╝███████╗██║ ╚████║╚██████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝
```

This project is developed and maintained by Shahab Afshar.

[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--3682--0471-A6CE39?style=flat-square&logo=ORCID&logoColor=white)](https://orcid.org/0009-0000-3682-0471)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Shahab_Afshar-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shahabafshar)

**Professor:** [Dr. Mai Zheng](https://scholar.google.com/citations?user=mFcB0JMAAAAJ&hl=en) [![Google Scholar](https://img.shields.io/badge/Google_Scholar-4285F4?style=flat-square&logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=mFcB0JMAAAAJ&hl=en)

**Course:** Advanced Data Storage Systems  
**Department:** Electrical and Computer Engineering (ECPE)  
**University:** Iowa State University  

**Testbed:** [Chameleon Cloud](https://www.chameleoncloud.org/)  
Chameleon Cloud is a large-scale, reconfigurable experimental environment for cloud computing research, providing researchers with bare metal access to explore novel cloud architectures and applications [1].

[1] K. Keahey et al., "Lessons Learned from the Chameleon Testbed," in Proceedings of the 2020 USENIX Annual Technical Conference (USENIX ATC '20), USENIX Association, July 2020.

**LucidBench** is A Docker-based filesystem benchmarking tool that automates the testing of different filesystems across various storage devices.

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