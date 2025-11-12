#!/usr/bin/env python3
"""
Utility to view and manage the download tracker.
"""

import json
import os
from datetime import datetime

def load_tracker(channel_folder):
    """Load the download tracker file."""
    tracker_file = os.path.join(channel_folder, 'downloaded_files_tracker.json')
    if not os.path.exists(tracker_file):
        print(f"No tracker file found at: {tracker_file}")
        return None
    
    with open(tracker_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def show_statistics(tracker):
    """Display download statistics."""
    stats = tracker.get('statistics', {})
    files = tracker.get('downloaded_files', {})
    
    print("\n" + "="*60)
    print("DOWNLOAD STATISTICS")
    print("="*60)
    print(f"Total files tracked: {stats.get('total_downloads', 0)}")
    print(f"Last download: {stats.get('last_download_date', 'Never')}")
    print(f"Unique files: {len(files)}")
    print("="*60)

def list_downloaded_files(tracker, limit=None):
    """List all downloaded files."""
    files = tracker.get('downloaded_files', {})
    
    print(f"\n{'='*60}")
    print(f"DOWNLOADED FILES ({len(files)} total)")
    print("="*60)
    
    sorted_files = sorted(
        files.items(), 
        key=lambda x: x[1].get('download_date', ''), 
        reverse=True
    )
    
    if limit:
        sorted_files = sorted_files[:limit]
    
    for i, (file_id, info) in enumerate(sorted_files, 1):
        print(f"\n{i}. {info.get('filename', 'Unknown')}")
        print(f"   File ID: {file_id}")
        print(f"   Message ID: {info.get('message_id', 'N/A')}")
        print(f"   Downloaded: {info.get('download_date', 'N/A')}")
        print(f"   Original date: {info.get('original_message_date', 'N/A')}")
        
        # Show file size if available
        file_size = info.get('file_size')
        if file_size:
            size_mb = file_size / (1024 * 1024)
            print(f"   Size: {size_mb:.2f} MB")
        
        # Show message text if available
        message_text = info.get('message_text', '')
        if message_text:
            preview = message_text[:80] + "..." if len(message_text) > 80 else message_text
            print(f"   📝 Message: {preview}")
    
    if limit and len(files) > limit:
        print(f"\n... and {len(files) - limit} more files")

def search_files(tracker, search_term):
    """Search for files by filename or message text."""
    files = tracker.get('downloaded_files', {})
    results = []
    
    search_term = search_term.lower()
    
    for file_id, info in files.items():
        filename = info.get('filename', '').lower()
        message_text = info.get('message_text', '').lower()
        
        if search_term in filename or search_term in message_text:
            results.append((file_id, info))
    
    if not results:
        print(f"\nNo files found matching '{search_term}'")
        return
    
    print(f"\n{'='*60}")
    print(f"SEARCH RESULTS: {len(results)} file(s) found")
    print("="*60)
    
    for i, (file_id, info) in enumerate(results, 1):
        print(f"\n{i}. {info.get('filename', 'Unknown')}")
        print(f"   Downloaded: {info.get('download_date', 'N/A')}")
        
        # Show message text if available
        message_text = info.get('message_text', '')
        if message_text:
            preview = message_text[:100] + "..." if len(message_text) > 100 else message_text
            print(f"   📝 Message: {preview}")

def reset_tracker(channel_folder):
    """Reset the download tracker (use with caution!)."""
    tracker_file = os.path.join(channel_folder, 'downloaded_files_tracker.json')
    
    confirm = input("\n⚠️  This will reset the download tracker. Files will be re-downloaded!\nAre you sure? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return
    
    new_tracker = {
        'downloaded_files': {},
        'statistics': {
            'total_downloads': 0,
            'last_download_date': None
        }
    }
    
    with open(tracker_file, 'w', encoding='utf-8') as f:
        json.dump(new_tracker, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Tracker reset! File: {tracker_file}")

def remove_file_from_tracker(tracker, channel_folder, file_id_or_name):
    """Remove a specific file from the tracker."""
    files = tracker.get('downloaded_files', {})
    tracker_file = os.path.join(channel_folder, 'downloaded_files_tracker.json')
    
    # Try to find by file ID first
    if file_id_or_name in files:
        removed = files.pop(file_id_or_name)
        print(f"✓ Removed: {removed.get('filename', 'Unknown')}")
    else:
        # Search by filename
        found = False
        for file_id, info in list(files.items()):
            if file_id_or_name.lower() in info.get('filename', '').lower():
                removed = files.pop(file_id)
                print(f"✓ Removed: {removed.get('filename', 'Unknown')}")
                found = True
                break
        
        if not found:
            print(f"File not found: {file_id_or_name}")
            return
    
    # Update statistics
    tracker['statistics']['total_downloads'] = len(files)
    
    # Save updated tracker
    with open(tracker_file, 'w', encoding='utf-8') as f:
        json.dump(tracker, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Tracker updated!")

def main():
    """Interactive tracker manager."""
    # Find channel folders
    channel_folders = [d for d in os.listdir('.') if os.path.isdir(d) and 
                      os.path.exists(os.path.join(d, 'downloaded_files_tracker.json'))]
    
    if not channel_folders:
        print("No channel folders with download tracker found.")
        print("Please run download_telegram_files.py first.")
        return
    
    print("="*60)
    print("DOWNLOAD TRACKER MANAGER")
    print("="*60)
    print("\nAvailable channels:")
    for i, folder in enumerate(channel_folders, 1):
        print(f"{i}. {folder}")
    
    if len(channel_folders) == 1:
        channel_folder = channel_folders[0]
        print(f"\nUsing channel: {channel_folder}")
    else:
        choice = input("\nSelect channel number: ")
        try:
            channel_folder = channel_folders[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return
    
    tracker = load_tracker(channel_folder)
    if not tracker:
        return
    
    while True:
        print("\n" + "="*60)
        print("OPTIONS:")
        print("="*60)
        print("1. Show statistics")
        print("2. List all downloaded files")
        print("3. List recent downloads (last 20)")
        print("4. Search files")
        print("5. Remove file from tracker")
        print("6. Reset tracker (WARNING: Files will be re-downloaded!)")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            show_statistics(tracker)
        
        elif choice == '2':
            list_downloaded_files(tracker)
        
        elif choice == '3':
            list_downloaded_files(tracker, limit=20)
        
        elif choice == '4':
            search_term = input("Enter search term: ")
            search_files(tracker, search_term)
        
        elif choice == '5':
            file_id = input("Enter file ID or filename: ")
            remove_file_from_tracker(tracker, channel_folder, file_id)
            # Reload tracker
            tracker = load_tracker(channel_folder)
        
        elif choice == '6':
            reset_tracker(channel_folder)
            # Reload tracker
            tracker = load_tracker(channel_folder)
        
        elif choice == '7':
            print("\nExiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
