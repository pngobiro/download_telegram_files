#!/usr/bin/env python3
"""
Script to download files from a Telegram channel.
Requires telethon library and Telegram API credentials.
"""

import asyncio
import os
import json
import socks
from telethon import TelegramClient
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from datetime import datetime

# Replace with your own values
API_ID = 20314147  # Get from https://my.telegram.org/auth
API_HASH = '0a0ff38efcb5d331c398d64389597d47'  # Get from https://my.telegram.org/auth
PHONE_NUMBER = '+254718952129'  # Your Telegram phone number

# Channel username or ID
CHANNEL = -1002128927866  # The channel ID

# Proxy settings (set to None if not using proxy)
# For SOCKS5 proxy: ('socks5', 'proxy_ip', proxy_port)
# For SOCKS5 with auth: ('socks5', 'proxy_ip', proxy_port, True, 'username', 'password')
# For HTTP proxy: ('http', 'proxy_ip', proxy_port)
# For MTProto proxy: ('mtproto', 'proxy_ip', proxy_port, 'secret')

# Option 1: Manual proxy configuration
PROXY = None  # Example: ('socks5', '127.0.0.1', 1080)

# Option 2: Try some popular free proxy services (uncomment to test)
# Warning: Free proxies are often unreliable and may not work
# PROXY = ('socks5', '47.88.3.19', 8080)  # Example free proxy
# PROXY = ('http', '8.219.97.248', 80)  # Example free proxy

# Uncomment and configure one of these if you have a proxy:
# PROXY = ('socks5', '127.0.0.1', 1080)  # SOCKS5 without auth
# PROXY = ('socks5', 'proxy.server.com', 1080, True, 'username', 'password')  # SOCKS5 with auth
# PROXY = ('http', 'proxy.server.com', 8080)  # HTTP proxy

# DOWNLOAD_DIR will be set dynamically

async def main():
    # Create the client with alternative connection and retry settings
    print("Initializing Telegram client...")
    if PROXY:
        print(f"Using proxy: {PROXY[0]}://{PROXY[1]}:{PROXY[2]}")
    
    client = TelegramClient(
        'session_name', 
        API_ID, 
        API_HASH,
        proxy=PROXY,
        connection=ConnectionTcpAbridged,
        connection_retries=5,
        retry_delay=3,
        timeout=30
    )

    try:
        # Connect and sign in
        print("Connecting to Telegram...")
        await client.start(phone=PHONE_NUMBER)
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Try using a VPN if Telegram is blocked in your region")
        print("3. Verify your API credentials are correct")
        await client.disconnect()
        return

    # Get the channel entity
    channel = await client.get_entity(CHANNEL)
    
    # Get channel title for folder name
    channel_title = channel.title
    main_folder = channel_title
    DOWNLOAD_DIR = os.path.join(main_folder, 'downloads')
    
    # Ensure download directory exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # Create a metadata file to store message context
    metadata_file = os.path.join(main_folder, 'file_metadata.json')
    
    # Create a tracking file to store downloaded file IDs (prevents re-downloading moved files)
    download_tracker_file = os.path.join(main_folder, 'downloaded_files_tracker.json')
    
    # Load existing metadata if it exists
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    else:
        metadata = {}
    
    # Load download tracker (stores message_id + file_id to prevent re-downloads)
    if os.path.exists(download_tracker_file):
        with open(download_tracker_file, 'r', encoding='utf-8') as f:
            download_tracker = json.load(f)
        
        # Ensure all existing entries have message_text field (add empty if missing)
        # This prevents losing fields if tracker was created before we added this feature
        for file_id, info in download_tracker.get('downloaded_files', {}).items():
            if 'message_text' not in info:
                info['message_text'] = ''
            if 'file_size' not in info:
                info['file_size'] = 0
    else:
        download_tracker = {
            'downloaded_files': {},  # {file_unique_id: {filename, message_id, date}}
            'statistics': {
                'total_downloads': 0,
                'last_download_date': None
            }
        }

    print(f"Downloading files from '{channel_title}'...")
    print(f"Files will be saved to: {DOWNLOAD_DIR}")
    print(f"Metadata will be saved to: {metadata_file}")
    print(f"Download tracker: {download_tracker_file}")
    print(f"Already tracked: {len(download_tracker['downloaded_files'])} files")

    # Get messages (adjust limit as needed)
    file_count = 0
    skipped_count = 0
    
    async for message in client.iter_messages(channel):
        if message.media:
            # Get file unique identifier to track downloads
            file_unique_id = None
            file_name = None
            
            if hasattr(message.media, 'document') and message.media.document:
                # Get unique file ID (this stays the same even if file is moved/renamed)
                file_unique_id = str(message.media.document.id)
                
                # Get the file name
                for attr in message.media.document.attributes:
                    if hasattr(attr, 'file_name'):
                        file_name = attr.file_name
                        break
            elif hasattr(message.media, 'photo'):
                # For photos, use photo ID
                file_unique_id = str(message.media.photo.id)
                file_name = f"photo_{message.id}.jpg"
            
            # Check if this file was already downloaded (by unique ID, not filename)
            if file_unique_id and file_unique_id in download_tracker['downloaded_files']:
                skipped_count += 1
                tracked_info = download_tracker['downloaded_files'][file_unique_id]
                if skipped_count <= 5:  # Show first 5 skipped
                    print(f'⏭️  Already downloaded: {tracked_info.get("filename", "unknown")} (ID: {message.id})')
                elif skipped_count == 6:
                    print(f'⏭️  ... skipping more already-downloaded files ...')
                continue
            
            # Extract message text and context
            message_text = message.text or ""
            message_date = message.date.strftime("%Y-%m-%d %H:%M:%S") if message.date else ""
            message_id = message.id
            
            # Download the file
            print(f'📥 Downloading: {file_name or "unnamed file"}...')
            file_path = await client.download_media(message, DOWNLOAD_DIR)
            
            if file_path:
                file_count += 1
                downloaded_file_name = os.path.basename(file_path)
                
                # Store metadata about this file
                metadata[downloaded_file_name] = {
                    "message_id": message_id,
                    "message_text": message_text,
                    "date": message_date,
                    "file_size": os.path.getsize(file_path),
                    "mime_type": message.media.document.mime_type if hasattr(message.media, 'document') else None,
                    "file_unique_id": file_unique_id
                }
                
                # Track this download to prevent re-downloading
                if file_unique_id:
                    # Check if entry already exists (shouldn't happen but just in case)
                    if file_unique_id in download_tracker['downloaded_files']:
                        # Update existing entry, preserving fields that might have been added
                        existing = download_tracker['downloaded_files'][file_unique_id]
                        existing.update({
                            "filename": downloaded_file_name,
                            "message_id": message_id,
                            "download_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "original_message_date": message_date,
                            "message_text": message_text,
                            "file_size": os.path.getsize(file_path)
                        })
                    else:
                        # Create new entry
                        download_tracker['downloaded_files'][file_unique_id] = {
                            "filename": downloaded_file_name,
                            "message_id": message_id,
                            "download_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "original_message_date": message_date,
                            "message_text": message_text,
                            "file_size": os.path.getsize(file_path)
                        }
                
                # Update statistics
                download_tracker['statistics']['total_downloads'] = len(download_tracker['downloaded_files'])
                download_tracker['statistics']['last_download_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f'✓ Downloaded ({file_count}): {downloaded_file_name}')
                if message_text:
                    # Show first 100 chars of message text
                    preview = message_text[:100] + "..." if len(message_text) > 100 else message_text
                    print(f'  📝 Message: {preview}')
                
                # Save metadata and tracker after each download
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
                
                with open(download_tracker_file, 'w', encoding='utf-8') as f:
                    json.dump(download_tracker, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"✓ Download complete!")
    print(f"{'='*60}")
    print(f"New files downloaded: {file_count}")
    print(f"Files skipped (already downloaded): {skipped_count}")
    print(f"Total tracked files: {len(download_tracker['downloaded_files'])}")
    print(f"✓ Metadata saved to: {metadata_file}")
    print(f"✓ Download tracker saved to: {download_tracker_file}")

    # Disconnect
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
