#!/usr/bin/env python3
"""
Fix footer contact card padding across all HTML files
"""
import glob

# Get all HTML files
html_files = [
    r'D:\FalconXoft Ship Chandler\Namibia\about.html',
    r'D:\FalconXoft Ship Chandler\Namibia\contact.html',
    r'D:\FalconXoft Ship Chandler\Namibia\services.html',
    r'D:\FalconXoft Ship Chandler\Namibia\request-quote.html'
]

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update padding: 0 to padding: 40px 32px
    content = content.replace(
        'class="footer-contact-card" style="list-style: none; padding: 0;">',
        'class="footer-contact-card" style="list-style: none; padding: 40px 32px;">'
    )
    
    # Update margin-bottom from 20px to 24px
    content = content.replace(
        'margin-bottom:20px;',
        'margin-bottom:24px;'
    )
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {html_file.split('\\\\')[-1]}")

print("\n✨ Footer padding fixed for all pages!")
