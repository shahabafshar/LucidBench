# LucidBench: A Comprehensive Framework for Docker Storage Backend Performance Analysis

Shahabeddin Afsharghoochani, Department of Electrical and Computer Engineering, Iowa State University, Ames, IA, USA. Email: safshar@iastate.edu

## Abstract

Performance of storage backends in containerized systems is a major driver of application efficiency, reliability, and scalability.We present LucidBench, a Docker-based benchmarking toolkit to enable automatic testing of various filesystems on various storage devices.LucidBench provides a thorough assessment of storage performance in containerized environments through real-world workload patterns and system resource utilization. Results of experimentation exhibit high contrast of performance in storage types and filesystems with up to five times more IOPS by NVMe SSD over HDD. The results provide insightful recommendations for resource usage and container overhead, informing the choice of storage backends for containerized workloads. 

Index Terms— Docker, storage performance, filesystem benchmarking, IOPS, container, monitoring, automation.

## I. Introduction

The widespread adoption of containerized systems for enterprise computing, artificial intelligence, and cloud-native applications has made it more important to comprehend storage performance trade-offs. Docker, a leading containerization platform, has several operating system-level storage drivers whose performance will be a function of both the workload type and the storage device characteristics. The range of storage drivers available, from traditional HDDs to high-performance NVMe SSDs, further complicates storage choice.

With increasing workloads shifting to container environments, the performance profile of storage backends has become a primary consideration. How well the resources are utilized, the performance variability across multiple storage drivers and filesystems, and the absence of standard benchmarking environments for container configurations are some of the reasons making the problem so complex. Current benchmarking packages do not include the particular overheads of containers, lack a full vision of resource monitoring, and fail to provide representative workloads for containers [1]. There is an urgent requirement for a standardized solution that can provide meaningful performance assessments directed towards containerized environments.

## II. Related Work and Motivation

Storage backends' influence on the performance of containers has been researched extensively. I/O efficiency in highly container-consolidated environments has been studied, and the focus is especially on OverlayFS and optimization of synchronization [1]. How crucial it is to understand overhead that is container-specific in performance analysis of storage has been exhibited. Performance metrics of ZFS and Btrfs filesystems under different scenarios have been compared [2]. Different backing filesystem effects on Docker storage performance have been tested, underscoring the importance of benchmarking methodologies to be thorough [3].

Storage backend performance behavior in containerized environments has become increasingly significant as organizations move more workloads to container platforms.The adoption of container technologies, especially Docker, has revolutionized application deployment and management. Surveys across industries have reported that majority of organizations utilize containers in production nowadays [3]. As the popularity increases so is the need to comprehend storage performance behavior in containerized workloads better.

Storage system performance traits in containerized systems exhibit significant variation depending on a variety of key factors. Storage driver selection, such as overlay2 and devicemapper, plays an important role to determine overall system performance [1]. Selection of underlying filesystem implementation, ext4, xfs, or btrfs, further introduces varying performance traits that must be critically examined [2]. Physical storage device type, ranging from traditional HDDs to blazing NVMe SSDs, contributes further to these variations.

## III. Research Questions and Methodology

The research question revolves around three major areas of concern in Docker storage backend performance and trend. The first issue is concerned with the inherent trends of performance encountered by various Docker storage backends operated on various forms of storage devices from traditional Hard Disk Drives (HDDs), Serial ATA Solid State Devices (SATA SSDs), to Non-Volatile Memory Express Solid State Devices (NVMe SSDs). This research incorporates a detailed analysis of Input/Output Operations Per Second (IOPS), throughput metrics, latency values, and the respective CPU and RAM consumption patterns.

The second area of research examines the impacts of heterogeneous I/O workload patterns on storage performance in containerized systems. Research involves comparative performance patterns under random and sequential access patterns, performance differences under read and write operations, effects of mixed workload conditions on performance, and impacts of varying block sizes on system-wide performance [3].

The third research focus investigates the intricate relationship between storage performance and system resource consumption.This research is interested in quantifying the CPU overhead incurred by different storage drivers [1], memory usage behavior profiling across different storage settings, and examining the impact of I/O wait times on system load.

## IV. System Architecture and Implementation

The LucidBench tool uses a seasoned modular architecture that integrates four main components for end-to-end storage benchmarking assistance in containers. The architecture attempts to provide a scientific approach to measuring performance with flexibility and extensibility.

The Device Detection Module is the foundation of the system, employing sophisticated hardware detection techniques through the hybridization of `lsblk` and `smartctl` utilities. The module performs thorough device detection and applies high-level classification algorithms to categorize storage devices into pre-established classes: HDD, SATA SSD, and NVMe SSD. Pre-benchmark device characterization capability is also included in the module, which establishes baseline performance thresholds to serve as benchmarks for subsequent analysis.

Benchmark Orchestrator module orchestrates the complex orchestration of benchmark operation. It enables rich container lifecycle management with complete control of Docker container lifecycle from launching to shutdown.The Orchestrator governs benchmark performance across different storage configurations with intense control over test parameters and environments. The system stability is ensured by mature error recovery capability, robust error recovery mechanism, and intensive logging.

The Resource Monitoring subsystem allows real-time performance monitoring along multiple dimensions. It monitors system-level metrics such as CPU usage, memory, and I/O operations in real time. The subsystem offers monitoring to the container level, with high-granularity visibility into resource consumption patterns in containerized environments. All of the performance data is logged in a structured format with high-granularity timestamps to support high-granularity post-processing as well as correlation research.

The Result Analysis module has sophisticated data processing capabilities, utilizing sophisticated aggregation and result normalization algorithms. The module generates in-depth visualizations through comparative charts and graphs utilized to facilitate easy analysis of complex performance information. The analysis subsystem concludes through the generation of in-depth performance reports, for instance, statistical analysis and performance data resulting in storage backend decision-making.

## V. Results and Discussion

LucidBench is a tool providing copious data about storage performance capacity on diverse storage and filesystems:

### Device-specific Performance
- **NVMe SSDs:** Illustrated higher performance with 5.63 performance rating (ext4), handling 46,855 IOPS up to and 1.33 GB/s of bandwidth
- **SATA SSDs:** Posted medium-level performance with scores of 0.97 to 1.42, outputting 7,820-9,761 IOPS
- **HDDs:** Posted lowest-performance scores (0.04-0.09) with native filesystems putting out 147-243 IOPS

### Filesystem Comparison in Performance
- **ext4:** Had peak performance on NVMe (5.63) with lowest latency (7.46ms)
- **xfs & btrfs:** Expressed excellent performance on all storage with equal bandwidth
- **NTFS anomaly:** Expressed very excellent performance on HDDs (1.36) compared to native filesystems (0.09), suggesting caching impact
- **vfat:** Expressed poorest performance on HDDs (0.04) but similar performance on NVMe (5.12)

### Latency Characteristics
- **NVMe devices:** Expressed lowest latency for all filesystems (7.46-17.13ms)
- **SSD configurations:** Logged intermediate latency (33.10-75.54ms)
- **HDD systems:** Logged highest latency (133.05-214.40ms), particularly in ext2/ext3 filesystem

### Workload Patterns
- **Random I/O:** NVMe SSD logged 3-4 times better performance
- **Sequential I/O:** Comparable good performance by SATA SSD to NVMe
- **Mixed Workloads:** Performance disparity obvious according to device type

## VI. Future Work

The LucidBench system is planned for significant enhancements across several key areas. The workload simulation capabilities will be expanded to include realistic application scenarios such as web server operations with open-read-close patterns and log appending, email server workloads featuring multi-threaded operations in single directories, and file server workloads combining random and sequential operations [3]. These simulations will incorporate varying block sizes to better represent real-world usage patterns.

A comprehensive filesystem performance analysis framework will be developed to evaluate the characteristics of Ext4, XFS, and Btrfs filesystems [2]. This analysis will investigate the impact of Copy-on-Write (CoW) mechanisms across different workload types, examine the performance implications of synchronous versus asynchronous write operations, and assess the effectiveness of filesystem-specific features including journaling and checksumming capabilities.

The system will incorporate advanced multi-container performance analysis capabilities, focusing on scaling behavior with concurrent containers ranging from one to three instances [3]. This analysis will examine resource contention patterns under various workload scenarios, evaluate the performance implications of container density on storage backends, and investigate cross-container I/O interference patterns [1].

## VII. Benchmarking Pitfalls and Interpretation Challenges

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

[1] N. Mizusawa, Y. Seki, J. Tao, and S. Yamaguchi, "A Study on I/O Performance in Highly Consolidated Container-Based Virtualized Environment on OverlayFS with Optimized Synchronization," in 2020 14th International Conference on Ubiquitous Information Management and Communication (IMCOM), IEEE, Jan. 2020, pp. 1–4. doi: 10.1109/imcom48794.2020.9001733.

[2] D. Gurjar and S. S. Kumbhar, "A Review on Performance Analysis of ZFS & BTRFS," in 2019 International Conference on Communication and Signal Processing (ICCSP), IEEE, Apr. 2019, pp. 0073–0076. doi: 10.1109/iccsp.2019.8698103. 

[3] Faculty of Computer Sciences, Megatrend University, Belgrade, Serbia and A. Ramadan, "A Dockers Storage Performance Evaluation: Impact of Backing File Systems," JISIoT, pp. 8–17, 2021, doi: 10.54216/JISIoT.030101.
