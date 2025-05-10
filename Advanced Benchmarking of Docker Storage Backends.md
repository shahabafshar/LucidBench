# LucidBench: A Comprehensive Framework for Docker Storage Backend Performance Analysis

**Author:** Shahabeddin Afsharghoochani  
**Department:** Department of Electrical and Computer Engineering  
**Course:** Advanced Data Storage Systems (Spring 2025)  
**Location:** Ames, IA, USA  
**Email:** [safshar@iastate.edu](mailto:safshar@iastate.edu)  
**ORCID:** [0009-0000-3682-0471](https://orcid.org/0009-0000-3682-0471)

## Abstract

Containerized environments rely on optimized storage backends to achieve the best I/O performance, handling snapshots, and system reliability. This research implements LucidBench, a Docker-based filesystem benchmarking tool that automates the testing of different filesystems across various storage devices. The tool provides comprehensive performance analysis of storage backends in containerized environments, with a focus on real-world workload patterns and system resource utilization. Our experimental results demonstrate significant performance variations across different storage types and filesystems, with NVMe SSDs showing up to 5x better IOPS performance compared to traditional HDDs. The analysis reveals critical insights into resource utilization patterns and container overhead, providing valuable guidance for storage backend selection in containerized environments.

**Keywords:** Docker, storage performance, filesystem benchmarking, IOPS, container, monitoring, automation

## Introduction

The rapid adoption of containerized applications in enterprise computing, artificial intelligence, and cloud-native workloads necessitates a deep understanding of storage performance trade-offs. Docker provides several storage drivers whose performance is greatly influenced by workload type and underlying storage devices. This complexity is further compounded by the diverse range of storage technologies available, from traditional hard disk drives (HDDs) to high-performance NVMe solid-state drives (SSDs).

The proliferation of container technology, notably Docker, across diverse enterprise and cloud-native infrastructures emphasizes the necessity for efficient, reliable, and scalable storage solutions. This research implements LucidBench, an automated benchmarking tool that provides insights into storage performance characteristics across different device types and filesystems. The tool addresses the critical need for standardized performance evaluation in containerized environments, where storage performance can significantly impact application behavior and resource utilization.
## Research Questions

This study aims to address the following key research questions:

1. **Performance Characteristics:** How do different Docker storage backends perform across various storage devices (HDD, SATA SSD, NVMe SSD) in terms of:
   - IOPS (Input/Output Operations Per Second)
   - Throughput
   - Latency
   - CPU and RAM utilization

2. **Workload Impact:** How do different I/O patterns affect storage performance in containerized environments?
   - Random vs. sequential access patterns
   - Read vs. write operations
   - Mixed workload scenarios
   - Block size variations

3. **Resource Utilization:** What is the relationship between storage performance and system resource utilization?
   - CPU overhead of different storage drivers
   - Memory consumption patterns
   - I/O wait times and system load


## System Architecture

LucidBench is designed with a modular architecture consisting of several key components:

### Device Detection Module
- **Hardware Identification:** Utilizes `lsblk` and `smartctl` for comprehensive device detection
- **Device Classification:** Automatically categorizes storage devices into HDD, SATA SSD, and NVMe SSD
- **Performance Profiling:** Pre-benchmark device characterization for baseline performance metrics

### Benchmark Orchestrator
- **Container Management:** Handles Docker container lifecycle and configuration
- **Test Execution:** Coordinates benchmark runs across different storage configurations
- **Error Handling:** Implements robust error recovery and logging mechanisms

### Resource Monitoring
- **System Metrics:** Tracks CPU, memory, and I/O statistics in real-time
- **Container Metrics:** Monitors container-specific resource utilization
- **Performance Logging:** Maintains detailed performance logs for post-analysis

### Result Analysis
- **Data Processing:** Aggregates and normalizes benchmark results
- **Visualization:** Generates performance comparison charts and graphs
- **Report Generation:** Creates comprehensive performance reports

## Implementation Details

The system is implemented using Python, Shell Script and Docker, with the following key features:

### Automated Device Detection
- **Device Scanning:** Uses `lsblk` for device enumeration
- **Smart Monitoring:** Implements `smartctl` for device health checks
- **Performance Classification:** Categorizes devices based on performance characteristics

### Docker-based Execution
- **Container Orchestration:** Manages Docker container deployment and configuration
- **Storage Mounting:** Handles filesystem mounting and unmounting
- **Resource Isolation:** Ensures consistent testing environments

### Real-time Monitoring
- **System Metrics:** Tracks CPU, memory, and I/O using `iostat` and `vmstat`
- **Container Metrics:** Monitors container-specific resource usage
- **Performance Logging:** Maintains detailed performance logs

### Benchmark Automation
- **Workload Generation:** Uses `fio` for comprehensive I/O testing
- **Test Patterns:** Implements various I/O patterns (random, sequential, mixed)
- **Result Collection:** Automates data gathering and storage

## Methodology

The benchmarking process follows these steps:

### 1. Device Detection and Classification
- **Device Discovery:** Automatic detection of available storage devices
- **Performance Profiling:** Initial performance assessment
- **Filesystem Preparation:** Mounting and configuration of test filesystems

### 2. Benchmark Execution
- **Container Deployment:** Docker container setup with specified configurations
- **Workload Execution:** Running standardized benchmark tests
- **Performance Monitoring:** Real-time tracking of system metrics

### 3. Data Collection
- **I/O Metrics:** Recording IOPS, throughput, and latency
- **Resource Usage:** Tracking CPU, memory, and I/O utilization
- **Container Metrics:** Monitoring container-specific performance

### 4. Analysis and Reporting
- **Performance Comparison:** Cross-device and cross-filesystem analysis
- **Resource Analysis:** Evaluation of resource utilization patterns
- **Recommendation Generation:** Storage backend selection guidance

## Results and Discussion

The LucidBench tool provides comprehensive insights into storage performance characteristics across different storage types and filesystems:

### Device-specific Performance
- **NVMe SSDs:** Demonstrated superior performance with a performance score of 5.63 (ext4), achieving up to 46,855 IOPS and 1.33 GB/s bandwidth
- **SATA SSDs:** Showed moderate performance with scores ranging from 0.97 to 1.42, delivering 7,820-9,761 IOPS
- **HDDs:** Exhibited the lowest performance scores (0.04-0.09) with native filesystems achieving 147-243 IOPS

### Filesystem Performance Comparison
- **ext4:** Achieved the highest performance on NVMe (5.63) with the lowest latency (7.46ms)
- **xfs & btrfs:** Demonstrated strong performance on all storage types with consistent bandwidth
- **NTFS anomaly:** Reported unusually high performance on HDDs (1.36) compared to native filesystems (0.09), suggesting caching effects
- **vfat:** Showed the lowest performance on HDDs (0.04) but competitive performance on NVMe (5.12)

### Latency Characteristics
- **NVMe devices:** Exhibited the lowest latency across all filesystems (7.46-17.13ms)
- **SSD configurations:** Showed moderate latency (33.10-75.54ms)
- **HDD systems:** Demonstrated the highest latency (133.05-214.40ms), particularly with ext2/ext3 filesystems

### Workload Patterns
- **Random I/O:** NVMe SSDs showed 3-4x better performance
- **Sequential I/O:** SATA SSDs performed competitively with NVMe
- **Mixed Workloads:** Clear performance differentiation based on device type

## Future Work

Planned improvements to the LucidBench system include:
- Support for additional filesystem types (ZFS, f2fs, OverlayFS, etc.)
- Enhanced workload simulation capabilities (Machine Learning Simulation, etc.)
- Significance level calculation based on the comparison between the container based results and direct access on storage device
- Analyzing the impact of concurrency in a multi-container test scenario


## Benchmarking Pitfalls and Interpretation Challenges

While LucidBench provides a comprehensive framework for evaluating storage performance across a variety of filesystems and devices, it is important to recognize certain pitfalls that can affect the accuracy and interpretation of benchmark results. These challenges are particularly relevant when comparing native and non-native filesystems, or when system-level caching mechanisms are involved.

### Filesystem and Driver Limitations

During our experiments, we observed that benchmarking results for non-native filesystems, such as NTFS on Linux (typically accessed via NTFS-3G or similar FUSE-based drivers), can be misleading. For example, NTFS sequential write tests on HDDs reported unrealistically high throughput and IOPS values—far exceeding the physical capabilities of the hardware. This anomaly is primarily due to aggressive caching by the operating system or the filesystem driver, which allows data to be written to memory and reported as complete before it is actually flushed to disk. As a result, the measured performance does not reflect the true capabilities of the storage device.

### Impact of Caching on Results

System and driver-level caching can significantly distort benchmark outcomes, especially for filesystems that are not natively supported by the operating system. In such cases, the benchmark tool may report the speed of writing to RAM rather than to the actual storage medium. This effect is evident in our results, where NTFS on Linux showed much higher performance than native filesystems like ext4, despite using identical hardware and test parameters. Disk utilization metrics further confirmed that the device was not being fully utilized during these tests, reinforcing the conclusion that the results were influenced by caching rather than true disk performance.

### Recommendations for Reliable Benchmarking

To ensure meaningful and comparable results, we recommend the following best practices:
- Prefer native filesystems for the operating system under test (e.g., ext4, xfs, btrfs on Linux).
- Be cautious when interpreting results from non-native filesystems, and clearly annotate or exclude such data from cross-filesystem comparisons.
- Where possible, use benchmark options that minimize caching effects (e.g., direct I/O, cache flushes), but recognize that some drivers may still buffer data in memory.
- Focus on appropriate metrics for each workload: use IOPS for small-block random I/O and throughput (MB/s) for large-block sequential I/O.

By acknowledging these limitations, researchers and practitioners can avoid common pitfalls and draw more accurate conclusions from storage performance benchmarks in containerized environments.

#### Data-driven Comparison Examples

To illustrate these pitfalls, we present two explicit comparisons from our experiments:

**1. ext4 vs. NTFS on HDD (Sequential Write, 1M block size):**

| Filesystem | IOPS | Bandwidth (MB/s) | Elapsed (s) | Disk Util (%) | Realistic? | Notes |
|------------|------|------------------|-------------|---------------|------------|-------|
| ext4       | 218  | 218              | 19          | 99.4          | Yes        | Native Linux FS |
| ntfs       | 860  | 859              | 5           | 0.08          | No         | Caching, not real disk speed |

The ext4 results are consistent with expected HDD performance, while NTFS reports unrealistically high throughput and extremely low disk utilization. This discrepancy is due to aggressive caching by the NTFS driver, which causes the benchmark to measure RAM speed rather than actual disk speed.

**2. NTFS on HDD vs. NTFS on NVMe (Sequential Write, 1M block size):**

| Device | Filesystem | IOPS | Bandwidth (MB/s) | Elapsed (s) | Disk Util (%) | Realistic? | Notes |
|--------|------------|------|------------------|-------------|---------------|------------|-------|
| HDD    | NTFS       | 860  | 859              | 5           | 0.08          | No         | Caching, not real disk speed |
| NVMe   | NTFS       | 879  | 879              | 5           | 0.04          | No         | Caching, not real disk speed |

Despite the significant hardware difference, both devices report nearly identical and implausibly high performance for NTFS. This further confirms that the results are dominated by caching effects rather than true device capabilities.

These examples underscore the importance of careful interpretation and the need to avoid direct comparison of non-native filesystems or results affected by system-level caching.

## References

[1] S. Faculty of Computer Sciences Megatrend University, Belgrade, "A Dockers Storage Performance Evaluation: Impact of Backing File Systems," Journal of intelligent systems and internet of things, 2021, doi: 10.54216/jisiot.030101.

[2] N. Mizusawa, Y. Seki, J. Tao, and S. Yamaguchi, "A Study on I/O Performance in Highly Consolidated Container-Based Virtualized Environment on OverlayFS with Optimized Synchronization," in 2020 14th International Conference on Ubiquitous Information Management and Communication (IMCOM), IEEE, Jan. 2020, pp. 1–4. doi: 10.1109/imcom48794.2020.9001733.

[3] D. Gurjar and S. S. Kumbhar, "A Review on Performance Analysis of ZFS & BTRFS," in 2019 International Conference on Communication and Signal Processing ( ICCSP), IEEE, Apr. 2019, pp. 0073–0076. doi: 10.1109/iccsp.2019.8698103.

[4] D. Gurjar and S. S. Kumbhar, "A Review on Performance Analysis of ZFS & BTRFS," in 2019 International Conference on Communication and Signal Processing ( ICCSP), IEEE, Apr. 2019, pp. 0073–0076. doi: 10.1109/iccsp.2019.8698103. 