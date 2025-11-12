# Telegram File Downloader with Auto-Categorization

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python tool for downloading, tracking, and organizing files from Telegram channels with intelligent medical file categorization.

## ✨ Features

- 📥 **Smart Download Tracking**: Files tracked by unique ID - won't re-download even if moved/renamed
- 🔄 **Automatic Categorization**: Organizes medical files into 23+ specialized categories
- 📝 **Metadata Preservation**: Captures message text, dates, and file information
- 🌐 **VPN Support**: Built-in Cloudflare WARP integration for restricted regions
- 🔒 **Data Integrity**: Backward compatibility and field preservation
- 🔍 **Search & Filter**: Search files by keywords, message text, or categories
- 📊 **Download History**: Complete tracking with statistics and reporting
## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Medical Categories](#medical-categories)
- [Utilities](#utilities)
- [Troubleshooting](#troubleshooting)

## 🚀 Installation

### Prerequisites

```bash
# Install required Python packages
pip install telethon PySocks

# Optional: Install Cloudflare WARP for VPN (if Telegram is blocked)
# See VPN Setup section below
```

### Setup

1. **Get Telegram API Credentials**
   - Visit https://my.telegram.org/auth
   - Get your `API_ID` and `API_HASH`
   
2. **Configure the script**
   ```python
   # Edit download_telegram_files.py
   API_ID = your_api_id
   API_HASH = 'your_api_hash'
   PHONE_NUMBER = '+your_phone_number'
   CHANNEL = your_channel_id
   ```

3. **Clone this repository**
   ```bash
   git clone https://github.com/pngobiro/download_telegram_files.git
   cd download_telegram_files
   ```

## 🎯 Quick Start
### Before Every Download

**ALWAYS check for running instances:**
```bash
python check_download_running.py
```

**If found, kill them:**
```bash
python check_download_running.py --kill
```

## 📥 Usage

### Basic Download Workflow1. **Connect VPN** (if needed):   ```bash   warp-cli connect   ```2. **Check no script is running**:   ```bash   python check_download_running.py   ```3. **Download files**:   ```bash   python download_telegram_files.py   ```4. **Organize into categories**:   ```bash   python organize_existing_files.py   ```---## 🔧 Utility Commands### Verify Tracker Health```bashpython test_tracker_fields.py```### Restore Message Fields (if needed)```bashpython update_tracker_with_messages.py```### View Download History```bashpython manage_download_tracker.py```### Search and Categorize```bashpython categorize_files.py```---## 📊 What Gets Tracked```json{  "file_unique_id": {    "filename": "example.pdf",    "message_id": 123,    "download_date": "2025-11-11 13:07:03",    "original_message_date": "2025-11-09 08:57:02",    "message_text": "Message caption here",    "file_size": 8547715  }}```Files tracked by **unique file ID** - won't re-download even if moved/renamed!---## 🏥 Medical CategoriesFiles auto-organized into 23 categories:- Microbiology, Clinical Chemistry, Hematology- Histopathology, Immunology, EMS- Orthopedics, Surgery, Medicine- Community Health, Leadership, Research- And more...---## ⚠️ Important1. **Never run multiple download scripts at once**2. **Always use `check_download_running.py` first**3. **Backup tracker before major changes**---## 🐛 Quick Fixes**Fields missing?**```bashpython update_tracker_with_messages.py```**Files re-downloading?**```bashpython test_tracker_fields.py  # Check health```**Can't connect?**```bashwarp-cli connect  # Enable VPN```**Script stuck?**```bashpython check_download_running.py --kill```---**✅ System Status**: All tracker fields preserved!**Last Updated**: November 11, 2025