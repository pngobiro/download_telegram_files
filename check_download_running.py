#!/usr/bin/env python3
"""
Check if download script is running and optionally stop it.
"""

import subprocess
import sys

def check_running():
    """Check if download_telegram_files.py is running."""
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True
        )
        
        processes = []
        for line in result.stdout.split('\n'):
            if 'download_telegram_files.py' in line and 'grep' not in line:
                processes.append(line)
        
        return processes
    except Exception as e:
        print(f"Error checking processes: {e}")
        return []

def main():
    print("="*60)
    print("DOWNLOAD SCRIPT STATUS CHECKER")
    print("="*60)
    
    processes = check_running()
    
    if not processes:
        print("\n✅ No download script is currently running")
        print("   Safe to run download_telegram_files.py")
        return
    
    print(f"\n⚠️  Found {len(processes)} instance(s) running:")
    for i, proc in enumerate(processes, 1):
        print(f"\n{i}. {proc[:100]}...")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--kill':
        confirm = input("\n⚠️  Kill all instances? (yes/no): ")
        if confirm.lower() == 'yes':
            subprocess.run(['pkill', '-f', 'download_telegram_files.py'])
            print("✅ All instances killed")
        else:
            print("Operation cancelled")
    else:
        print("\nTo kill these processes, run:")
        print("  python check_download_running.py --kill")
        print("Or manually:")
        print("  pkill -f download_telegram_files.py")

if __name__ == '__main__':
    main()
