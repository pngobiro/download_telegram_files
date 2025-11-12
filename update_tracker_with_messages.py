#!/usr/bin/env python3
"""
Update the download tracker with message text from metadata file.
"""

import json
import os

def update_tracker_with_messages(channel_folder):
    """Add message text to tracker from metadata file."""
    
    tracker_file = os.path.join(channel_folder, 'downloaded_files_tracker.json')
    metadata_file = os.path.join(channel_folder, 'file_metadata.json')
    
    # Check if files exist
    if not os.path.exists(tracker_file):
        print(f"Tracker file not found: {tracker_file}")
        return
    
    if not os.path.exists(metadata_file):
        print(f"Metadata file not found: {metadata_file}")
        print("Note: Message text can only be added for files that have metadata.")
        return
    
    # Load both files
    with open(tracker_file, 'r', encoding='utf-8') as f:
        tracker = json.load(f)
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Create a mapping of filename to metadata
    filename_to_metadata = {filename: data for filename, data in metadata.items()}
    
    # Update tracker entries
    updated_count = 0
    added_empty_count = 0
    for file_id, info in tracker['downloaded_files'].items():
        filename = info.get('filename')
        
        # Try to find matching metadata
        if filename and filename in filename_to_metadata:
            meta = filename_to_metadata[filename]
            
            # Add/update message text and file size
            info['message_text'] = meta.get('message_text', '')
            if 'file_size' in meta:
                info['file_size'] = meta['file_size']
            updated_count += 1
        else:
            # Add empty message text field for files without metadata
            if 'message_text' not in info:
                info['message_text'] = ''
                added_empty_count += 1
    
    # Save updated tracker
    with open(tracker_file, 'w', encoding='utf-8') as f:
        json.dump(tracker, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Updated {updated_count} files with message text from metadata")
    print(f"✓ Added empty message_text field to {added_empty_count} files")
    print(f"✓ Total updated: {updated_count + added_empty_count} files")
    print(f"✓ Tracker saved: {tracker_file}")

def main():
    channel_folder = "Malcom Skylar"
    
    if not os.path.exists(channel_folder):
        print(f"Channel folder not found: {channel_folder}")
        return
    
    print("="*60)
    print("UPDATE TRACKER WITH MESSAGE TEXT")
    print("="*60)
    print(f"Channel: {channel_folder}\n")
    
    update_tracker_with_messages(channel_folder)

if __name__ == '__main__':
    main()
