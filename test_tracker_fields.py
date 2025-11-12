#!/usr/bin/env python3
"""
Test that the download script preserves message_text fields.
"""

import json
import os

def test_tracker_fields():
    """Test that tracker has message_text fields."""
    tracker_file = 'Malcom Skylar/downloaded_files_tracker.json'
    
    if not os.path.exists(tracker_file):
        print("❌ Tracker file not found!")
        return False
    
    with open(tracker_file, 'r', encoding='utf-8') as f:
        tracker = json.load(f)
    
    total = len(tracker['downloaded_files'])
    with_message = sum(1 for info in tracker['downloaded_files'].values() 
                       if 'message_text' in info)
    with_size = sum(1 for info in tracker['downloaded_files'].values() 
                    if 'file_size' in info)
    
    print(f"Total files: {total}")
    print(f"Files with message_text: {with_message}/{total}")
    print(f"Files with file_size: {with_size}/{total}")
    
    if with_message == total and with_size == total:
        print("✅ All files have required fields!")
        return True
    else:
        print("❌ Some files are missing fields!")
        return False

if __name__ == '__main__':
    print("="*60)
    print("TRACKER FIELDS TEST")
    print("="*60)
    test_tracker_fields()
