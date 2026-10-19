#!/usr/bin/env python3
"""
Update all images across the website - services, homepage, and about page
"""
import re

# Service image mapping
service_images = {
    'provisions': 'service-provisions.jpg',
    'bonded': 'service-provisions.jpg',
    'deck': 'service-deck-stores.jpg',
    'engine': 'service-engine-stores.jpg',
    'cabin': 'service-cabin.jpg',
    'safety': 'service-safety.jpg',
    'electrical': 'service-spares.jpg',
    'chemicals': 'service-marine-chemicals.jpg',
    'welding': 'service-welding.jpg',
    'spare-parts': 'service-spares.jpg',
    'publications': 'service-nautical.jpg',
    'tools': 'service-hardwares-tools.jpg',
    'urgent': 'service-urgent.jpg'
}

def update_services_page():
    """Add/update images for all services"""
    services_file = r'D:\FalconXoft Ship Chandler\Namibia\services.html'
    
    with open(services_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # For each service, ensure it has an image section
    for service_id, image_name in service_images.items():
        # Check if this service already has a content-image-full section
        pattern = rf'(id="{service_id}".*?</details>)'
        
        def add_or_update_image(match):
            section = match.group(0)
            
            # If it already has content-image-full, update the image source
            if 'content-image-full' in section:
                # Update existing image
                section = re.sub(
                    r'(<img\s+src=")[^"]+(".*?alt="[^"]*")',
                    rf'\1./assets/imgs/{image_name}\2',
                    section
                )
            else:
                # Add image section before </details>
                image_html = f'''
                            <div class="content-image-full">
                                <img src="./assets/imgs/{image_name}" alt="{service_id.replace("-", " ").title()} Supply">
                            </div>
                        </div>
                    </details>'''
                # Replace the closing tags
                section = section.replace('</div>\n                    </details>', image_html)
            
            return section
        
        content = re.sub(pattern, add_or_update_image, content, flags=re.DOTALL)
    
    with open(services_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated all service images")

def update_index_page():
    """Update homepage images"""
    index_file = r'D:\FalconXoft Ship Chandler\Namibia\index.html'
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update hero/main image
    content = re.sub(
        r'(src=")[^"]*hero[^"]*\.jpg',
        r'\1assets/imgs/ship-picture-main.jpg',
        content
    )
    
    # Update any background images
    content = re.sub(
        r'(background-image:\s*url\()["\']?[^"\']*hero[^"\']*\.jpg',
        r'\1"assets/imgs/ship-picture-main.jpg"',
        content
    )
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated homepage images")

def update_about_page():
    """Update about page images"""
    about_file = r'D:\FalconXoft Ship Chandler\Namibia\about.html'
    
    with open(about_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update main about image
    content = re.sub(
        r'(src=")[^"]*(?:img-1|header1)[^"]*\.jpg',
        r'\1assets/imgs/main-namibia-port-portrait-image.jpg',
        content,
        count=1
    )
    
    # Update secondary image if exists
    content = re.sub(
        r'(src=")[^"]*(?:img-2|bg-img)[^"]*\.jpg',
        r'\1assets/imgs/another-image-ship-2nd-main.jpg',
        content,
        count=1
    )
    
    with open(about_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Updated about page images")

if __name__ == "__main__":
    print("🖼️  Starting image updates...\n")
    
    update_services_page()
    update_index_page()
    update_about_page()
    
    print("\n✨ All images updated successfully!")
    print("\n📋 Updated files:")
    print("   - services.html (13 service images)")
    print("   - index.html (hero images)")
    print("   - about.html (portrait and secondary images)")
