#!/usr/bin/env python3

import os
import sys
import time
import json
import signal
import psutil
import atexit
from datetime import datetime

class SystemMonitor:
    def __init__(self, output_file, storage_type, device, filesystem, test_type):
        self.output_file = output_file
        self.storage_type = storage_type
        self.device = device
        self.filesystem = filesystem
        self.test_type = test_type
        self.running = False
        self.pid_file = os.path.join(os.path.dirname(output_file), "monitor.pid")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Register cleanup handler
        atexit.register(self.cleanup)

    def cleanup(self):
        """Clean up resources."""
        if self.running:
            self.running = False
            try:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            except Exception as e:
                print(f"Warning: Error during cleanup: {e}", file=sys.stderr)

    def setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown."""
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

    def handle_signal(self, signum, frame):
        """Handle termination signals."""
        print(f"\nReceived signal {signum}, stopping monitoring...")
        self.running = False

    def get_system_stats(self):
        """Get current system statistics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used": memory.used,
                "memory_total": memory.total,
                "disk_read_bytes": disk_io.read_bytes if disk_io else 0,
                "disk_write_bytes": disk_io.write_bytes if disk_io else 0,
                "disk_read_count": disk_io.read_count if disk_io else 0,
                "disk_write_count": disk_io.write_count if disk_io else 0
            }
        except Exception as e:
            print(f"Warning: Error getting system stats: {e}", file=sys.stderr)
            return None

    def start_monitoring(self):
        """Start system monitoring."""
        print(f"Started monitoring for {self.storage_type} {self.device} {self.filesystem} {self.test_type}")
        
        # Write PID file
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
        except Exception as e:
            print(f"Error writing PID file: {e}", file=sys.stderr)
            sys.exit(1)
        
        self.setup_signal_handlers()
        self.running = True
        
        # Create metadata
        metadata = {
            "storage_type": self.storage_type,
            "device": self.device,
            "filesystem": self.filesystem,
            "test_type": self.test_type,
            "start_time": datetime.now().isoformat()
        }
        
        stats = []
        try:
            while self.running:
                stat = self.get_system_stats()
                if stat:
                    stats.append(stat)
                time.sleep(1)
        except Exception as e:
            print(f"Error during monitoring: {e}", file=sys.stderr)
        finally:
            # Save collected stats with metadata
            if stats:
                try:
                    output_data = {
                        **metadata,
                        "end_time": datetime.now().isoformat(),
                        "stats": stats
                    }
                    with open(self.output_file, 'w') as f:
                        json.dump(output_data, f, indent=2)
                except Exception as e:
                    print(f"Error saving monitoring data: {e}", file=sys.stderr)
            
            self.cleanup()

def stop_monitoring():
    """Stop the monitoring process."""
    pid_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "monitoring/monitor.pid")
    
    try:
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Send SIGTERM to the monitoring process
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                print(f"Warning: Monitoring process {pid} not found", file=sys.stderr)
                return
            
            # Wait for process to finish
            max_wait = 5  # Maximum wait time in seconds
            while max_wait > 0 and os.path.exists(pid_file):
                time.sleep(0.1)
                max_wait -= 0.1
            
            # Force cleanup if process didn't exit
            if os.path.exists(pid_file):
                try:
                    os.remove(pid_file)
                except Exception as e:
                    print(f"Warning: Error removing PID file: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error stopping monitoring: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 6:
        print("Usage: monitor.py <output_file> <storage_type> <device> <filesystem> <test_type>", file=sys.stderr)
        sys.exit(1)
    
    output_file = sys.argv[1]
    storage_type = sys.argv[2]
    device = sys.argv[3]
    filesystem = sys.argv[4]
    test_type = sys.argv[5]
    
    monitor = SystemMonitor(output_file, storage_type, device, filesystem, test_type)
    monitor.start_monitoring()

if __name__ == "__main__":
    main() 