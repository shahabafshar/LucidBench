#!/usr/bin/env python3

import os
import sys
import json
import time
import subprocess
import signal
from datetime import datetime

class FilesystemBenchmark:
    def __init__(self, device_path, filesystem):
        self.device_path = device_path
        self.filesystem = filesystem
        self.mount_point = "/mnt/benchmark"
        self.results_dir = "/results"
        self.cleanup_needed = False
        
        # Create mount point if it doesn't exist
        os.makedirs(self.mount_point, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)

    def cleanup(self):
        """Clean up resources."""
        if self.cleanup_needed:
            try:
                self.unmount_device()
            except Exception as e:
                print(f"Warning: Error during cleanup: {e}", file=sys.stderr)
            self.cleanup_needed = False

    def format_device(self):
        """Format the device with the specified filesystem."""
        print(f"Formatting {self.device_path} with {self.filesystem}...")
        try:
            if self.filesystem == "ext4":
                subprocess.run(["mkfs.ext4", "-F", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "xfs":
                subprocess.run(["mkfs.xfs", "-f", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "btrfs":
                subprocess.run(["mkfs.btrfs", "-f", self.device_path], check=True, capture_output=True, text=True)
            else:
                raise ValueError(f"Unsupported filesystem: {self.filesystem}")
        except subprocess.CalledProcessError as e:
            print(f"Error formatting device: {e.stderr}", file=sys.stderr)
            raise

    def mount_device(self):
        """Mount the device to the mount point."""
        print(f"Mounting {self.device_path} to {self.mount_point}...")
        try:
            subprocess.run(["mount", "-t", self.filesystem, self.device_path, self.mount_point], 
                         check=True, capture_output=True, text=True)
            self.cleanup_needed = True
        except subprocess.CalledProcessError as e:
            print(f"Error mounting device: {e.stderr}", file=sys.stderr)
            raise

    def unmount_device(self):
        """Unmount the device if it's mounted."""
        print(f"Unmounting {self.device_path}...")
        try:
            # Check if device is mounted
            result = subprocess.run(["mountpoint", "-q", self.mount_point], capture_output=True)
            if result.returncode == 0:
                subprocess.run(["umount", self.mount_point], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error unmounting device: {e.stderr}", file=sys.stderr)
            raise

    def run_fio_test(self, test_type):
        """Run an FIO benchmark test."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.results_dir, f"{test_type}_{self.filesystem}_{timestamp}.json")
        
        fio_config = {
            "random_read": {
                "rw": "randread",
                "bs": "4k",
                "size": "1G",
                "runtime": "60",
                "direct": "1",
                "ioengine": "libaio",
                "iodepth": "32",
                "numjobs": "4"
            },
            "random_write": {
                "rw": "randwrite",
                "bs": "4k",
                "size": "1G",
                "runtime": "60",
                "direct": "1",
                "ioengine": "libaio",
                "iodepth": "32",
                "numjobs": "4"
            },
            "sequential_read": {
                "rw": "read",
                "bs": "1M",
                "size": "4G",
                "runtime": "60",
                "direct": "1",
                "ioengine": "libaio",
                "iodepth": "32",
                "numjobs": "1"
            },
            "sequential_write": {
                "rw": "write",
                "bs": "1M",
                "size": "4G",
                "runtime": "60",
                "direct": "1",
                "ioengine": "libaio",
                "iodepth": "32",
                "numjobs": "1"
            }
        }
        
        if test_type not in fio_config:
            raise ValueError(f"Unknown test type: {test_type}")
        
        config = fio_config[test_type]
        print(f"Running {test_type} benchmark...")
        
        try:
            cmd = [
                "fio",
                "--name=test",
                f"--filename={self.mount_point}/testfile",
                "--output-format=json",
                f"--output={output_file}",
            ] + [f"--{k}={v}" for k, v in config.items()]
            
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error running FIO test: {e.stderr}", file=sys.stderr)
            raise

    def run_benchmarks(self):
        """Run all benchmark tests."""
        results = {}
        
        try:
            # Prepare device
            self.unmount_device()  # Ensure device is unmounted
            self.format_device()
            self.mount_device()
            
            # Run benchmarks
            test_types = ["random_read", "random_write", "sequential_read", "sequential_write"]
            for test_type in test_types:
                try:
                    results[test_type] = self.run_fio_test(test_type)
                except Exception as e:
                    print(f"Error in {test_type} benchmark: {e}", file=sys.stderr)
                    continue
            
            if not results:
                raise RuntimeError("No benchmarks completed successfully")
            
            print("\nBenchmark Results:")
            print("=================")
            for test_type, result_file in results.items():
                print(f"{test_type}: {result_file}")
            
            return results
            
        except Exception as e:
            print(f"\nError during benchmark: {e}", file=sys.stderr)
            raise
        finally:
            self.cleanup()

def main():
    if len(sys.argv) != 3:
        print("Usage: benchmark.py <device_path> <filesystem>", file=sys.stderr)
        sys.exit(1)
    
    device_path = sys.argv[1]
    filesystem = sys.argv[2]
    
    if not os.path.exists(device_path):
        print(f"Error: Device {device_path} does not exist", file=sys.stderr)
        sys.exit(1)
    
    if filesystem not in ["ext4", "xfs", "btrfs"]:
        print(f"Error: Unsupported filesystem {filesystem}", file=sys.stderr)
        sys.exit(1)
    
    try:
        benchmark = FilesystemBenchmark(device_path, filesystem)
        results = benchmark.run_benchmarks()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 