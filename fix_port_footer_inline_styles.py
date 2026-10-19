#!/usr/bin/env python3
"""
Fix port pages footer inline styles
Remove inline 'padding: 0' from footer-contact-card to allow CSS padding to take effect
"""

import os
import re

def fix_port_footer(file_path):
    """Remove inline padding from footer-contact-card in a port page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Track if we made changes
        original_content = content
        
        # Remove the inline style from footer-contact-card
        # Change: <ul class="footer-contact-card" style="list-style: none; padding: 0;">
        # To: <ul class="footer-contact-card">
        content = re.sub(
            r'<ul class="footer-contact-card" style="list-style: none; padding: 0;">',
            r'<ul class="footer-contact-card">',
            content
        )
        
        # Also handle if there are variations (with or without spaces)
        content = re.sub(
            r'<ul class="footer-contact-card" style="[^"]*list-style:\s*none;\s*padding:\s*0;[^"]*">',
            r'<ul class="footer-contact-card">',
            content
        )
        
        # Change individual li inline styles to remove margin-bottom:20px and add margin-bottom:24px via CSS
        # From: <li style="display:flex; gap:16px; margin-bottom:20px;">
        # To: <li style="display:flex; gap:16px;">
        # Actually, let's remove all inline styles from footer-contact-card li elements
        # The CSS already handles all the styling
        
        # Find the footer-contact-card section and update li inline styles
        content = re.sub(
            r'(<ul class="footer-contact-card">.*?<li) style="display:flex; gap:16px; margin-bottom:20px;"',
            r'\1',
            content,
            flags=re.DOTALL
        )
        
        # More general pattern for all li elements within footer-contact-card
        # This is safer - find footer-contact-card block and update within it
        def clean_footer_li_styles(match):
            """Remove inline styles from li elements in footer-contact-card"""
            footer_block = match.group(0)
            # Remove style attributes from li tags
            cleaned = re.sub(
                r'(<li)\s+style="[^"]*"',
                r'\1',
                footer_block
            )
            return cleaned
        
        # Match the entire footer-contact-card ul block
        content = re.sub(
            r'<ul class="footer-contact-card">.*?</ul>',
            clean_footer_li_styles,
            content,
            flags=re.DOTALL
        )
        
        # Check if we made any changes
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix all port pages"""
    ports_dir = "ports"
    
    if not os.path.exists(ports_dir):
        print(f"Error: {ports_dir} directory not found")
        return
    
    fixed_count = 0
    total_count = 0
    
    # Process all HTML files in ports directory
    for filename in os.listdir(ports_dir):
        if filename.endswith('.html'):
            total_count += 1
            file_path = os.path.join(ports_dir, filename)
            print(f"Processing: {filename}...", end=" ")
            
            if fix_port_footer(file_path):
                print("✓ Fixed")
                fixed_count += 1
            else:
                print("○ No changes needed")
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total port pages: {total_count}")
    print(f"  Fixed: {fixed_count}")
    print(f"  Unchanged: {total_count - fixed_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
