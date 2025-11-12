#!/usr/bin/env python3
"""
Script to search and categorize downloaded Telegram files based on their message context.
"""

import json
import os
import re
import shutil
from pathlib import Path

def load_metadata(channel_folder):
    """Load the metadata file from a channel folder."""
    metadata_file = os.path.join(channel_folder, 'file_metadata.json')
    if not os.path.exists(metadata_file):
        print(f"Error: Metadata file not found at {metadata_file}")
        return None
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_files(metadata, search_term, search_in='text'):
    """
    Search for files based on message text or filename.
    
    Args:
        metadata: Dictionary of file metadata
        search_term: Term to search for (case-insensitive)
        search_in: 'text', 'filename', or 'both'
    
    Returns:
        List of matching files with their metadata
    """
    results = []
    search_term = search_term.lower()
    
    for filename, data in metadata.items():
        match = False
        
        if search_in in ['text', 'both']:
            message_text = data.get('message_text', '').lower()
            if search_term in message_text:
                match = True
        
        if search_in in ['filename', 'both']:
            if search_term in filename.lower():
                match = True
        
        if match:
            results.append({
                'filename': filename,
                **data
            })
    
    return results

def categorize_files_by_keywords(metadata, categories):
    """
    Categorize files based on keyword mapping.
    
    Args:
        metadata: Dictionary of file metadata
        categories: Dict of {category_name: [keywords]}
    
    Returns:
        Dict of {category_name: [files]}
    """
    categorized = {cat: [] for cat in categories.keys()}
    categorized['uncategorized'] = []
    
    for filename, data in metadata.items():
        message_text = data.get('message_text', '').lower()
        file_text = filename.lower()
        combined_text = f"{message_text} {file_text}"
        
        matched = False
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in combined_text:
                    categorized[category].append({
                        'filename': filename,
                        **data
                    })
                    matched = True
                    break
            if matched:
                break
        
        if not matched:
            categorized['uncategorized'].append({
                'filename': filename,
                **data
            })
    
    return categorized

def organize_files_into_folders(channel_folder, categorized_files, copy=True):
    """
    Organize files into category folders.
    
    Args:
        channel_folder: Base folder containing downloads
        categorized_files: Dict from categorize_files_by_keywords
        copy: If True, copy files; if False, move files
    """
    downloads_dir = os.path.join(channel_folder, 'downloads')
    
    for category, files in categorized_files.items():
        if not files:
            continue
        
        # Create category folder
        category_dir = os.path.join(channel_folder, 'categorized', category)
        os.makedirs(category_dir, exist_ok=True)
        
        for file_info in files:
            filename = file_info['filename']
            src_path = os.path.join(downloads_dir, filename)
            dst_path = os.path.join(category_dir, filename)
            
            if os.path.exists(src_path):
                if copy:
                    shutil.copy2(src_path, dst_path)
                    print(f"Copied: {filename} -> {category}/")
                else:
                    shutil.move(src_path, dst_path)
                    print(f"Moved: {filename} -> {category}/")

def print_search_results(results):
    """Print search results in a readable format."""
    if not results:
        print("No files found matching your search.")
        return
    
    print(f"\nFound {len(results)} matching file(s):\n")
    for i, file_info in enumerate(results, 1):
        print(f"{i}. {file_info['filename']}")
        print(f"   Date: {file_info.get('date', 'N/A')}")
        if file_info.get('message_text'):
            preview = file_info['message_text'][:150]
            if len(file_info['message_text']) > 150:
                preview += "..."
            print(f"   Message: {preview}")
        print()

def main():
    """Interactive mode for searching and categorizing files."""
    import sys
    
    # Find channel folders
    channel_folders = [d for d in os.listdir('.') if os.path.isdir(d) and 
                      os.path.exists(os.path.join(d, 'file_metadata.json'))]
    
    if not channel_folders:
        print("No channel folders with metadata found in current directory.")
        print("Please run download_telegram_files.py first.")
        return
    
    print("Available channels:")
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
    
    metadata = load_metadata(channel_folder)
    if not metadata:
        return
    
    print(f"\nLoaded metadata for {len(metadata)} files.\n")
    print("Options:")
    print("1. Search files by keyword")
    print("2. Categorize files automatically")
    print("3. List all files")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '1':
        search_term = input("Enter search term: ")
        search_in = input("Search in (text/filename/both) [both]: ").strip() or 'both'
        results = search_files(metadata, search_term, search_in)
        print_search_results(results)
    
    elif choice == '2':
        # Example categories - customize these based on your needs
        categories = {
            'Microbiology': ['microbiology', 'bacteria', 'virus', 'vibrionaceae', 'escherichia'],
            'Clinical Chemistry': ['chemistry', 'clinical chemistry', 'kidney', 'blood gases'],
            'Histopathology': ['histopathology', 'pathology'],
            'Immunology': ['immunology', 'immune', 'HIV'],
            'EMS': ['ems', 'emergency', 'trauma', 'medical emergencies'],
            'Leadership': ['leadership', 'management'],
            'Health and Safety': ['health and safety', 'HSM'],
            'Imaging': ['imaging', 'radiography', 'equipment technology'],
        }
        
        print("\nCategorizing files...")
        categorized = categorize_files_by_keywords(metadata, categories)
        
        for category, files in categorized.items():
            if files:
                print(f"\n{category}: {len(files)} file(s)")
                for file_info in files[:5]:  # Show first 5
                    print(f"  - {file_info['filename']}")
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more")
        
        organize = input("\nOrganize files into folders? (y/n): ")
        if organize.lower() == 'y':
            copy_or_move = input("Copy or move files? (copy/move) [copy]: ").strip() or 'copy'
            organize_files_into_folders(channel_folder, categorized, copy=(copy_or_move == 'copy'))
            print("\n✓ Files organized!")
    
    elif choice == '3':
        print(f"\nAll files ({len(metadata)}):\n")
        for i, (filename, data) in enumerate(metadata.items(), 1):
            print(f"{i}. {filename}")
            if data.get('message_text'):
                preview = data['message_text'][:100]
                if len(data['message_text']) > 100:
                    preview += "..."
                print(f"   {preview}")
            print()
    
    else:
        print("Exiting...")

if __name__ == '__main__':
    main()
