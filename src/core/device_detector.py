#!/usr/bin/env python3

import subprocess
import json
import os
import re
import sys
from typing import Dict, List, Optional

class DeviceDetector:
    def __init__(self):
        self.devices = {}
        self.free_devices = {}

    def get_block_devices(self) -> List[Dict]:
        """Get all block devices using lsblk."""
        try:
            output = subprocess.check_output(
                ['lsblk', '-J', '-o', 'NAME,TYPE,SIZE,MODEL,SERIAL,MOUNTPOINT'],
                universal_newlines=True
            )
            return json.loads(output)['blockdevices']
        except subprocess.CalledProcessError as e:
            print(f"Error getting block devices: {e}", file=sys.stderr)
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing lsblk output: {e}", file=sys.stderr)
            return []

    def get_device_info(self, device_name: str) -> Optional[Dict]:
        """Get detailed information about a specific device using smartctl."""
        try:
            output = subprocess.check_output(
                ['smartctl', '-i', f'/dev/{device_name}'],
                universal_newlines=True,
                stderr=subprocess.PIPE
            )
            
            # Extract relevant information
            model = re.search(r'Device Model:\s+(.*)', output)
            serial = re.search(r'Serial Number:\s+(.*)', output)
            type_info = re.search(r'Rotation Rate:\s+(.*)', output)
            
            return {
                'model': model.group(1) if model else 'Unknown',
                'serial': serial.group(1) if serial else 'Unknown',
                'rotation_rate': type_info.group(1) if type_info else 'Unknown'
            }
        except subprocess.CalledProcessError as e:
            print(f"Error getting device info for {device_name}: {e}", file=sys.stderr)
            return None

    def classify_device(self, device_info: Dict, device_name: str = None) -> str:
        """Classify device as HDD, SSD, or NVMe."""
        if not device_info:
            return 'Unknown'
        
        model = device_info.get('model', '').lower()
        # Check model or device name for NVMe
        if 'nvme' in model or (device_name and device_name.startswith('nvme')):
            return 'NVMe'
        
        rotation_rate = device_info.get('rotation_rate', '').lower()
        if 'rpm' in rotation_rate:
            return 'HDD'
        elif 'solid state' in model or 'ssd' in model:
            return 'SSD'
        else:
            return 'Unknown'

    def is_device_free(self, device: Dict) -> bool:
        """Check if a device is free (unformatted and unmounted)."""
        return not device.get('mountpoint') and device.get('type') == 'disk'

    def detect_devices(self):
        """Main method to detect and classify all devices."""
        block_devices = self.get_block_devices()
        
        if not block_devices:
            print("No block devices found", file=sys.stderr)
            return
        
        for device in block_devices:
            device_name = device['name']
            device_info = self.get_device_info(device_name)
            
            if device_info:
                device_type = self.classify_device(device_info, device_name)
                self.devices[device_name] = {
                    'type': device_type,
                    'size': device['size'],
                    'model': device_info['model'],
                    'serial': device_info['serial']
                }
                
                if self.is_device_free(device):
                    self.free_devices[device_name] = self.devices[device_name]

    def get_free_devices_by_type(self) -> Dict[str, List[str]]:
        """Get free devices grouped by their type."""
        devices_by_type = {
            'HDD': [],
            'SSD': [],
            'NVMe': [],
            'Unknown': []
        }
        
        for device_name, info in self.free_devices.items():
            devices_by_type[info['type']].append(device_name)
        
        return devices_by_type

def main():
    try:
        detector = DeviceDetector()
        detector.detect_devices()
        
        output = {
            'devices': detector.devices,
            'free_devices_by_type': detector.get_free_devices_by_type()
        }
        
        print(json.dumps(output, indent=2))
    except Exception as e:
        print(f"Error in device detection: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 