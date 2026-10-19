#!/usr/bin/env python3
"""
Update favicon references in all port pages
"""
import os
import glob

# Get all HTML files in ports directory
port_files = glob.glob(r"D:\FalconXoft Ship Chandler\Namibia\ports\*.html")

old_favicon = '''  <!-- Favicon -->
  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="apple-touch-icon" href="../assets/imgs/favicon.png">'''

new_favicon = '''  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="apple-touch-icon" href="../assets/imgs/favicon.png">'''

updated_count = 0
for file_path in port_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_favicon in content:
            content = content.replace(old_favicon, new_favicon)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            updated_count += 1
            print(f"✅ Updated: {os.path.basename(file_path)}")
        else:
            print(f"⏭️  Skipped: {os.path.basename(file_path)} (already updated or different format)")
    
    except Exception as e:
        print(f"❌ Error updating {os.path.basename(file_path)}: {str(e)}")

print(f"\n✨ Updated {updated_count} port pages with enhanced favicon references")
