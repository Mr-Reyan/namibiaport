#!/usr/bin/env python3
"""
Update service images in services.html and optimize images
"""
import os
import re

# Service image mapping (service ID -> image filename)
service_images = {
    'provisions': 'service-provisions.jpg',
    'bonded': 'service-provisions.jpg',  # No specific bonded image, use provisions
    'deck': 'service-deck-stores.jpg',
    'engine': 'service-engine-stores.jpg',
    'cabin': 'service-cabin.jpg',
    'safety': 'service-safety.jpg',
    'electrical': 'service-spares.jpg',  # No electrical.jpg, use spares
    'chemicals': 'service-marine-chemicals.jpg',
    'welding': 'service-welding.jpg',
    'spare-parts': 'service-spares.jpg',
    'publications': 'service-nautical.jpg',
    'tools': 'service-hardwares-tools.jpg',
    'urgent': 'service-urgent.jpg'
}

# Path to services.html
services_file = r'D:\FalconXoft Ship Chandler\Namibia\services.html'

print("🖼️  Updating service images in services.html...")

# Read the file
with open(services_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Count updates
updated_count = 0

# Update each service image
for service_id, image_name in service_images.items():
    # Pattern to match the image in the service section
    # Look for: id="service_id" ... <img src="./assets/imgs/service-*.avif"
    pattern = rf'(id="{service_id}".*?<img\s+src=")(\.\/assets\/imgs\/service-[^"]+\.avif)(")'
    
    def replace_image(match):
        global updated_count
        updated_count += 1
        return f'{match.group(1)}./assets/imgs/{image_name}{match.group(3)}'
    
    content = re.sub(pattern, replace_image, content, flags=re.DOTALL)

# Also update any standalone .avif references to .jpg
content = content.replace('service-provisions.avif', 'service-provisions.jpg')
content = content.replace('service-deck.avif', 'service-deck-stores.jpg')
content = content.replace('service-engine.avif', 'service-engine-stores.jpg')
content = content.replace('service-cabin.avif', 'service-cabin.jpg')
content = content.replace('service-safety.avif', 'service-safety.jpg')
content = content.replace('service-electrical.avif', 'service-spares.jpg')
content = content.replace('service-marine.avif', 'service-marine-chemicals.jpg')
content = content.replace('service-welding.avif', 'service-welding.jpg')
content = content.replace('service-spares.avif', 'service-spares.jpg')
content = content.replace('service-publications.avif', 'service-nautical.jpg')
content = content.replace('service-tools.avif', 'service-hardwares-tools.jpg')
content = content.replace('service-urgent.avif', 'service-urgent.jpg')
content = content.replace('service-bonded.avif', 'service-provisions.jpg')

# Write back
with open(services_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Updated {updated_count} service images in services.html")
print("✨ All .avif references replaced with .jpg")
