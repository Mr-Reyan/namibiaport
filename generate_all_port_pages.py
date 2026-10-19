#!/usr/bin/env python3
"""
Generate 48 port pages from Excel data using bissau template structure
"""

import pandas as pd
import os
import re
from pathlib import Path

# Configuration
EXCEL_PATH = r"D:\FalconXoft Ship Chandler\Website Data\Ship_Chandler_SEO_49_Pages_FULL.xlsx"
SHEET_NAME = "SEO Pages"
OUTPUT_DIR = r"D:\FalconXoft Ship Chandler\Namibia\ports"

# Ensure output directory exists
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def sanitize_filename(page_name):
    """Convert page name to filename"""
    # Remove special characters and convert to lowercase
    filename = page_name.lower()
    # Replace spaces and special chars with hyphens
    filename = re.sub(r'[^a-z0-9]+', '-', filename)
    # Remove leading/trailing hyphens
    filename = filename.strip('-')
    return filename + '.html'

def format_seo_description_to_html(full_description):
    """Convert markdown-style SEO description to HTML with proper structure"""
    if pd.isna(full_description):
        return ""
    
    lines = str(full_description).strip().split('\n')
    html_parts = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html_parts.append('        </ul>')
                in_list = False
            continue
        
        # Check for H2 heading (## Something)
        if line.startswith('## '):
            if in_list:
                html_parts.append('        </ul>')
                in_list = False
            heading_text = line[3:].strip()
            html_parts.append(f'        <h2>{heading_text}</h2>')
        
        # Check for H1 heading (# Something) - should be rare in content
        elif line.startswith('# ') and not line.startswith('## '):
            if in_list:
                html_parts.append('        </ul>')
                in_list = False
            # Skip H1 as it's already in the hero section
            continue
        
        # Check for list item (- Something)
        elif line.startswith('- '):
            if not in_list:
                html_parts.append('        <ul>')
                in_list = True
            list_item = line[2:].strip()
            html_parts.append(f'          <li>{list_item}</li>')
        
        # Regular paragraph
        else:
            if in_list:
                html_parts.append('        </ul>')
                in_list = False
            
            # Handle bold text wrapped in **
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            html_parts.append(f'        <p>{line}</p>')
    
    # Close any open list
    if in_list:
        html_parts.append('        </ul>')
    
    return '\n'.join(html_parts)

def generate_port_page(row):
    """Generate a single port page HTML"""
    
    page_name = row['Page Name']
    h1_title = row['H1']
    meta_title = row['Meta Title']
    meta_description = row['Meta Description']
    full_seo_description = row['Full SEO Description']
    
    # Generate filename
    filename = sanitize_filename(page_name)
    
    # Convert SEO description to HTML
    content_html = format_seo_description_to_html(full_seo_description)
    
    # Extract port name for sidebar (use H1 or Page Name)
    port_display_name = h1_title if pd.notna(h1_title) else page_name
    
    # Generate complete HTML with PROPER RELATIVE PATHS (../)
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="keywords" content="ship chandler, ship supply, provisions, marine stores, bonded stores, deck stores, engine stores, vessel supply, marine procurement">
  <meta name="author" content="SHIP CHANDLER NAMIBIA CO., LTD">
  
  <!-- Open Graph Meta Tags -->
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:type" content="website">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="apple-touch-icon" href="../assets/imgs/favicon.png">

  <!-- Port Pages CSS -->
  <link rel="stylesheet" href="../assets/css/port-pages.css">
</head>
<body>

  <!-- HEADER -->
  <header class="site-header" id="site-header">
    <div class="container header-inner">
      <a class="logo" href="../index.html">
        <img src="../assets/imgs/logo-shipchandler-namibia.png" alt="Ship Chandler Namibia Logo">
      </a>

      <button class="nav-toggle" type="button" aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
      </button>

      <nav class="primary-nav" id="primary-nav">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="../about.html">About</a></li>
          
          <li class="nav-item has-dropdown">
            <a class="nav-link" href="../services.html">Services <i class="fas fa-chevron-down" style="font-size:0.7rem; margin-left:4px;"></i></a>
            <div class="dropdown-menu">
              <a href="../services.html#provisions">Provisions Supply</a>
              <a href="../services.html#bonded">Bonded Stores</a>
              <a href="../services.html#deck">Deck Stores</a>
              <a href="../services.html#engine">Engine Stores</a>
              <a href="../services.html#cabin">Cabin & Galley</a>
              <a href="../services.html#safety">Safety & PPE</a>
              <a href="../services.html#electrical">Electrical Stores</a>
              <a href="../services.html#chemicals">Marine Chemicals</a>
              <a href="../services.html#welding">Welding Equipment</a>
              <a href="../services.html#spare-parts">Spare Parts</a>
              <a href="../services.html#publications">Nautical Charts</a>
              <a href="../services.html#tools">Tools & Hardware</a>
              <a href="../services.html#urgent">Urgent Supply</a>
            </div>
          </li>
          
          <li class="nav-item has-dropdown active">
            <a class="nav-link" href="javascript:void(0)">Ports <i class="fas fa-chevron-down" style="font-size:0.7rem; margin-left:4px;"></i></a>
            <div class="mega-menu">
              <div class="mega-header">
                <div class="mega-header-title">Global Port Network</div>
                <div class="mega-search">
                  <i class="fas fa-search" style="color:var(--text-muted);"></i>
                  <input type="text" id="mega-port-search" placeholder="Search 49 ports...">
                </div>
              </div>
              <div class="mega-grid" id="mega-port-list">
                <!-- Populated via JS -->
              </div>
            </div>
          </li>
          
          <li class="nav-item"><a class="nav-link" href="../contact.html">Contact</a></li>
        </ul>
        <a class="btn btn-primary" style="padding: 10px 24px; font-size: 0.9rem;" href="../request-quote.html">Get Quote</a>
      </nav>
    </div>
  </header>

  <main>
    <!-- PORT HERO -->
    <section class="port-hero">
      <img src="https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?q=80&w=2070&auto=format&fit=crop" alt="{port_display_name} Port Background" class="port-hero-bg">
      <div class="container port-hero-content">
        <ul class="breadcrumb">
          <li><a href="../index.html">Home</a></li>
          <li><span>/</span></li>
          <li><a href="../index.html#ports">Ports</a></li>
          <li><span>/</span></li>
          <li style="color: var(--white);">{port_display_name}</li>
        </ul>
        <h1 class="port-title">{h1_title}</h1>
        <p class="port-desc">{meta_description}</p>
      </div>
    </section>

    <!-- PORT LAYOUT -->
    <section class="container port-layout">
      
      <!-- MAIN CONTENT CANVAS -->
      <article class="reading-canvas">
{content_html}
      </article>

      <!-- STICKY SIDEBAR -->
      <aside class="port-sidebar">
        <div class="sidebar-cta">
          <h3>Need Supplies for {port_display_name.replace("Ship Chandler ", "").replace(" Ship Chandler", "")}?</h3>
          <p>Send your requisition list and the team will provide a competitive quote within 2 hours.</p>
          <a href="../request-quote.html" class="btn btn-primary">Request a Quote</a>
        </div>

        <div class="sidebar-contact">
          <h4>Direct Contact</h4>
          <ul>
            <li><i class="fas fa-map-marker-alt"></i> <span>17 Rikumbi Kandanga Road, Walvis Bay, Namibia</span></li>
            <li><i class="fab fa-whatsapp"></i> <a href="https://wa.me/2482743244" target="_blank">(+248) 2 743 244</a></li>
            <li><i class="fas fa-envelope"></i> <a href="mailto:sales@shipchandlernamibia.com">sales@shipchandlernamibia.com</a></li>
            <li><i class="fas fa-user-tie"></i> <span>Petrus Johannes</span></li>
          </ul>
        </div>
      </aside>

    </section>
  </main>

  <!-- FOOTER -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <!-- Brand Column -->
        <div class="footer-brand">
          <img src="../assets/imgs/logo-shipchandler-namibia.png" alt="Ship Chandler Namibia Logo">
          <p>SHIP CHANDLER NAMIBIA CO., LTD is a licensed marine supplier providing provisions, technical stores, bonded goods, and emergency vessel supply across all Namibian ports and anchorages.</p>
        </div>

        <!-- Links Column -->
        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul class="footer-links">
            <li><a href="../index.html">Home</a></li>
            <li><a href="../about.html">About Us</a></li>
            <li><a href="../services.html">Services</a></li>
            <li><a href="../contact.html">Contact</a></li>
            <li><a href="../request-quote.html">Request a Quote</a></li>
          </ul>
        </div>

        <!-- Contact Card Column -->
        <div class="footer-col">
          <h4>Contact Details</h4>
          <ul class="footer-contact-card" style="list-style: none; padding: 0;">
            <li style="display:flex; gap:16px; margin-bottom:20px;"><i class="fas fa-map-marker-alt" style="color:var(--amber); margin-top:4px;"></i> <span style="color:var(--sand-dark);">17 Rikumbi Kandanga Road, Walvis Bay, Namibia</span></li>
            <li style="display:flex; gap:16px; margin-bottom:20px;"><i class="fas fa-envelope" style="color:var(--amber); margin-top:4px;"></i> <a href="mailto:sales@shipchandlernamibia.com" style="color:var(--sand-dark);">sales@shipchandlernamibia.com</a></li>
            <li style="display:flex; gap:16px; margin-bottom:20px;"><i class="fas fa-user-tie" style="color:var(--amber); margin-top:4px;"></i> <span style="color:var(--sand-dark);">Petrus Johannes</span></li>
            
            <!-- Custom WhatsApp Button -->
            <li style="display:block;">
              <a class="hero-whatsapp-bar" href="https://wa.me/2482743244" target="_blank" rel="noopener noreferrer" aria-label="Direct WhatsApp contact (+248) 2 743 244">
                <span class="hero-whatsapp-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
                  </svg>
                </span>
                <span class="hero-whatsapp-tag">WhatsApp:</span>
                <span class="hero-whatsapp-num">(+248) 2 743 244</span>
                <span class="hero-whatsapp-arrow" aria-hidden="true">&rarr;</span>
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div style="text-align:center; width:100%;">&copy; 2026 SHIP CHANDLER NAMIBIA CO., LTD. All rights reserved.</div>
      </div>
    </div>
  </footer>

  <script>
    // --- Port List Data for Dropdown ---
    const ports = [
      "Ship Chandler Dar Es Salaam", "Ship Chandler Apapa", "Ship Chandler Onne Port Nigeria", "San Pedro Ship Supply Chandler",
      "Ship Chandler Abidjan", "Ship Chandler Freetown", "Monrovia Ship Chandler", "Ship Chandler Maputo", "Ship Chandler Matadi",
      "Ship Chandler Beira", "Ship Chandler Angola", "Ship Chandler Lobito", "ShipChandler Lome", "Shipchandler Lome",
      "Ivory Coast Ship Chandler", "Nouadhibou Ship Chandler", "Ship Chandler Luanda", "Ship Chandler Cape Verde",
      "Ship Chandler Gabon", "Ship Chandler Namibia", "Walvis Bay Ship Chandler", "Ship Chandler Gentil Port - Gabon",
      "Ship Chandler Takoradi", "Ship Chandler Congo", "Shipchandler Lagos", "Ship Chandler Port Ambon",
      "Shipchandler Pointe Noire", "Ship Chandler Djibouti", "Ship Chandler Cabinda", "Ship Chandler Tema",
      "Ship Chandler Mindelo", "Ship Chandler Casablanca", "Ship Chandler Safi Port Morocco", "Ship Chandler Kamsar",
      "Ship Chandler Soyo", "Dakar Ship Chandler", "Ship Chandler Senegal", "Ship Chandler Dakar", "Bissau Ship Chandler - Guinea",
      "Conakry Ship Chandler", "Ship Chandler Cotonou", "Douala Ship Chandler", "Liberia Ship Chandler", "Namibia Ship Chandler",
      "Ship Chandler Dakar", "Ship Chandler Mombasa", "Ship Chandlers Saldanha Bay", "Ship Chandler Owendo", "Ship Chandlers Richards Bay"
    ];

    // Populate Mega Menu
    const megaList = document.getElementById('mega-port-list');
    if (megaList) {{
      const third = Math.ceil(ports.length / 3);
      const col1 = ports.slice(0, third);
      const col2 = ports.slice(third, third * 2);
      const col3 = ports.slice(third * 2);

      function createPortGroup(title, items) {{
        const group = document.createElement('div');
        group.className = 'mega-group';
        group.innerHTML = `<h4>${{title}}</h4>`;
        items.forEach(port => {{
          const a = document.createElement('a');
          a.href = `${{port.toLowerCase().replace(/[^a-z0-9]+/g, '-')}}.html`;
          a.textContent = port;
          group.appendChild(a);
        }});
        return group;
      }}

      megaList.appendChild(createPortGroup('African Ports (A-D)', col1));
      megaList.appendChild(createPortGroup('African Ports (E-M)', col2));
      megaList.appendChild(createPortGroup('African Ports (N-Z)', col3));

      // Mega Menu Search
      const searchInput = document.getElementById('mega-port-search');
      if (searchInput) {{
        searchInput.addEventListener('input', function (e) {{
          const query = e.target.value.toLowerCase();
          const allLinks = megaList.querySelectorAll('a');
          const groups = megaList.querySelectorAll('.mega-group');

          allLinks.forEach(link => {{
            const text = link.textContent.toLowerCase();
            link.style.display = text.includes(query) ? 'block' : 'none';
          }});

          groups.forEach(group => {{
            const hasVisible = Array.from(group.querySelectorAll('a')).some(a => a.style.display !== 'none');
            group.style.display = hasVisible ? 'block' : 'none';
          }});
        }});
      }}
    }}

    document.addEventListener('DOMContentLoaded', function () {{
      // --- Sticky Header Effect ---
      const header = document.querySelector('.site-header');
      window.addEventListener('scroll', () => {{
        if (window.scrollY > 20) {{
          header.classList.add('scrolled');
        }} else {{
          header.classList.remove('scrolled');
        }}
      }});

      // --- Mobile Nav Toggle ---
      const navToggle = document.querySelector('.nav-toggle');
      const primaryNav = document.querySelector('.primary-nav');
      const navIcon = navToggle.querySelector('i');

      navToggle.addEventListener('click', function () {{
        primaryNav.classList.toggle('open');
        if (primaryNav.classList.contains('open')) {{
          navIcon.classList.replace('fa-bars', 'fa-times');
        }} else {{
          navIcon.classList.replace('fa-times', 'fa-bars');
        }}
      }});

      // --- Mobile Dropdown Toggles ---
      const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown');
      dropdownItems.forEach(item => {{
        const link = item.querySelector('.nav-link');
        link.addEventListener('click', function (e) {{
          if (window.innerWidth <= 1024) {{
            e.preventDefault();
            item.classList.toggle('open');
          }}
        }});
      }});
    }});
  </script>
</body>
</html>'''
    
    return filename, html_content

def main():
    print("🚀 Starting port page generation...")
    print(f"📁 Reading Excel file: {EXCEL_PATH}")
    
    # Read Excel file
    df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME)
    
    print(f"📊 Found {len(df)} total ports in Excel")
    print(f"📝 Columns: {list(df.columns)}")
    
    # Skip the first row (Dar Es Salaam which is row 0, index 0)
    # Generate pages for rows 1-48 (indices 1-48, which is 48 pages)
    ports_to_generate = df.iloc[1:49]  # This gets rows with index 1 through 48 (48 rows total)
    
    print(f"\n✨ Generating {len(ports_to_generate)} port pages (skipping first row)...")
    print(f"   First page to generate: {ports_to_generate.iloc[0]['Page Name']}")
    print(f"   Last page to generate: {ports_to_generate.iloc[-1]['Page Name']}")
    
    generated_count = 0
    errors = []
    
    for idx, row in ports_to_generate.iterrows():
        try:
            filename, html_content = generate_port_page(row)
            output_path = os.path.join(OUTPUT_DIR, filename)
            
            # Write the file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            generated_count += 1
            print(f"   ✅ Generated: {filename} ({row['Page Name']})")
            
        except Exception as e:
            error_msg = f"❌ Error generating {row['Page Name']}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
    
    print(f"\n🎉 Generation complete!")
    print(f"   ✅ Successfully generated: {generated_count} pages")
    print(f"   📁 Output directory: {OUTPUT_DIR}")
    
    if errors:
        print(f"\n⚠️  Errors encountered: {len(errors)}")
        for error in errors:
            print(f"   {error}")
    else:
        print(f"\n✨ All pages generated successfully with no errors!")
    
    print(f"\n📋 Summary:")
    print(f"   - Total ports in Excel: {len(df)}")
    print(f"   - Ports to generate: {len(ports_to_generate)}")
    print(f"   - Successfully generated: {generated_count}")
    print(f"   - Failed: {len(errors)}")

if __name__ == "__main__":
    main()
