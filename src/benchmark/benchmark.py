#!/usr/bin/env python3

import os
import sys
import json
import time
import subprocess
import signal
from datetime import datetime

class FilesystemBenchmark:
    def __init__(self, device_path, filesystem, output_file, storage_type, device, test_type):
        self.device_path = device_path
        self.filesystem = filesystem
        self.output_file = output_file
        self.storage_type = storage_type
        self.device = device
        self.test_type = test_type
        self.mount_point = "/mnt/benchmark"
        self.cleanup_needed = False
        
        # Create mount point if it doesn't exist
        os.makedirs(self.mount_point, exist_ok=True)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

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
            if self.filesystem == "ext2":
                subprocess.run(["/usr/sbin/mkfs.ext2", "-F", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "ext3":
                subprocess.run(["/usr/sbin/mkfs.ext3", "-F", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "ext4":
                subprocess.run(["/usr/sbin/mkfs.ext4", "-F", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "xfs":
                subprocess.run(["/usr/sbin/mkfs.xfs", "-f", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "btrfs":
                subprocess.run(["/usr/sbin/mkfs.btrfs", "-f", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "vfat":
                subprocess.run(["/usr/sbin/mkfs.vfat", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "fat":
                subprocess.run(["/usr/sbin/mkfs.fat", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "ntfs":
                subprocess.run(["/usr/sbin/mkfs.ntfs", "-F", self.device_path], check=True, capture_output=True, text=True)
            elif self.filesystem == "f2fs":
                subprocess.run(["/usr/sbin/mkfs.f2fs", self.device_path], check=True, capture_output=True, text=True)
            else:
                raise ValueError(f"Unsupported filesystem: {self.filesystem}")
        except subprocess.CalledProcessError as e:
            print(f"Error formatting device: {e.stderr}", file=sys.stderr)
            raise
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
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

    def run_fio_test(self):
        """Run an FIO benchmark test."""
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
        
        if self.test_type not in fio_config:
            raise ValueError(f"Unknown test type: {self.test_type}")
        
        config = fio_config[self.test_type]
        print(f"Running {self.test_type} benchmark...")
        
        try:
            cmd = [
            "fio",
                "--name=test",
                f"--filename={self.mount_point}/testfile",
            "--output-format=json",
                f"--output={self.output_file}",
            ] + [f"--{k}={v}" for k, v in config.items()]
            
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Add metadata to the output file
            with open(self.output_file, 'r') as f:
                data = json.load(f)
            
            metadata = {
                "storage_type": self.storage_type,
                "device": self.device,
                "filesystem": self.filesystem,
                "test_type": self.test_type,
                "start_time": datetime.now().isoformat()
            }
            
            output_data = {**metadata, **data}
            
            with open(self.output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            return self.output_file
        except subprocess.CalledProcessError as e:
            print(f"Error running FIO test: {e.stderr}", file=sys.stderr)
            raise

    def run_benchmark(self):
        """Run the benchmark test."""
        try:
            # Prepare device
            self.unmount_device()  # Ensure device is unmounted
            self.format_device()
            self.mount_device()
            
            # Run benchmark
            result_file = self.run_fio_test()
            
            print(f"\nBenchmark Results:")
            print(f"=================")
            print(f"Result file: {result_file}")
            
            return result_file
            
        except Exception as e:
            print(f"\nError during benchmark: {e}", file=sys.stderr)
            raise
        finally:
            self.cleanup()

def main():
    if len(sys.argv) != 7:
        print("Usage: benchmark.py <device_path> <filesystem> <output_file> <storage_type> <device> <test_type>", file=sys.stderr)
        sys.exit(1)
    
    device_path = sys.argv[1]
    filesystem = sys.argv[2]
    output_file = sys.argv[3]
    storage_type = sys.argv[4]
    device = sys.argv[5]
    test_type = sys.argv[6]
    
    if not os.path.exists(device_path):
        print(f"Error: Device {device_path} does not exist", file=sys.stderr)
        sys.exit(1)
    
    if filesystem not in ["ext2", "ext3", "ext4", "xfs", "btrfs", "vfat", "fat", "ntfs", "f2fs"]:
        print(f"Error: Unsupported filesystem {filesystem}", file=sys.stderr)
        sys.exit(1)
    
    try:
        benchmark = FilesystemBenchmark(device_path, filesystem, output_file, storage_type, device, test_type)
        result_file = benchmark.run_benchmark()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 