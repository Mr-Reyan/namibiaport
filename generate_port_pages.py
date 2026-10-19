import json
import re

# Read ports data
with open(r'Website Data\ports_data.json', 'r', encoding='utf-8') as f:
    ports_data = json.load(f)

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def markdown_to_html(markdown_text):
    """Convert markdown to HTML with proper structure"""
    lines = markdown_text.split('\n')
    html_output = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_list:
                html_output.append('          </ul>')
                in_list = False
            continue
        
        # H1
        if line.startswith('# ') and not line.startswith('## '):
            if in_list:
                html_output.append('          </ul>')
                in_list = False
            continue  # Skip H1 as it's already in the hero
        
        # H2
        elif line.startswith('## '):
            if in_list:
                html_output.append('          </ul>')
                in_list = False
            html_output.append(f'          <h2>{line[3:]}</h2>')
        
        # List item
        elif line.startswith('- '):
            if not in_list:
                html_output.append('          <ul>')
                in_list = True
            html_output.append(f'            <li>{line[2:]}</li>')
        
        # Bold text (markdown **text**)
        elif line.startswith('**') and line.endswith('**'):
            if in_list:
                html_output.append('          </ul>')
                in_list = False
            html_output.append(f'          <p><strong>{line[2:-2]}</strong></p>')
        
        # Regular paragraph
        else:
            if in_list:
                html_output.append('          </ul>')
                in_list = False
            html_output.append(f'          <p>{line}</p>')
    
    if in_list:
        html_output.append('          </ul>')
    
    return '\n'.join(html_output)

# Generate each port page
for port in ports_data:
    port_name = port['Page Name']
    slug = slugify(port_name)
    h1 = port['H1']
    meta_title = port['Meta Title']
    meta_description = port['Meta Description']
    full_seo = port['Full SEO Description']
    
    # Convert markdown to HTML
    content_html = markdown_to_html(full_seo)
    
    # Create the HTML page
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{meta_title}</title>
  <meta name="description" content="{meta_description}">
  <meta name="keywords" content="ship chandler, ship supply, provisions, marine stores, bonded stores, deck stores, engine stores, vessel supply, marine procurement">
  <meta name="author" content="Ship Chandler Libya CO., LTD">
  
  <!-- Open Graph Meta Tags -->
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:type" content="website">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="apple-touch-icon" href="../assets/imgs/favicon.png">

  <!-- Port Pages CSS -->
  <link rel="stylesheet" href="../assets/css/port-pages.css">
</head>
<body>

  <!-- HEADER / NAVBAR -->
  <header class="site-header" id="site-header">
    <div class="header-inner">
      <a class="logo" href="../index.html">
        <img src="../assets/imgs/logo-shipchandler-libya.png" alt="ShipChandler Libya Logo" width="40" height="40">
        <span class="logo-text">
          <strong>ShipChandler</strong>
          <span>Libya</span>
        </span>
      </a>

      <button class="nav-toggle" type="button" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>

      <nav class="primary-nav" id="primary-nav">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="../about.html">About</a></li>
          <li class="nav-item has-dropdown">
            <a class="nav-link" href="../services.html">Services <span class="nav-arrow"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg></span></a>
            <div class="dropdown-menu">
              <a href="../services.html#provisions">Provisions Supply</a>
              <a href="../services.html#deck">Deck Stores</a>
              <a href="../services.html#cabin">Cabin & Galley</a>
              <a href="../services.html#engine">Engine Stores</a>
              <a href="../services.html#bonded">Bonded Stores</a>
              <a href="../services.html#safety">Safety & PPE</a>
            </div>
          </li>
          <li class="nav-item has-dropdown">
            <a class="nav-link" href="javascript:void(0)">Ports <span class="nav-arrow"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg></span></a>
            <div class="mega-menu">
              <div class="mega-header">
                <div class="mega-header-title">Global Port Network</div>
                <div class="mega-search">
                  <i class="fas fa-search" style="color:var(--gray-500);"></i>
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
    <!-- SUBPAGE HERO -->
    <section class="subpage-hero">
      <img src="https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?q=80&w=2070&auto=format&fit=crop" alt="{port_name}" class="subpage-hero-bg">
      <div class="container">
        <div class="hero-content">
          <ul class="breadcrumb">
            <li><a href="../index.html">Home</a></li>
            <li><span>/</span></li>
            <li><a href="../index.html#ports">Ports</a></li>
            <li><span>/</span></li>
            <li>{port_name}</li>
          </ul>
          <h1 class="hero-title">{h1}</h1>
          <p class="hero-desc">Professional ship supply, provisions, bonded stores, deck and engine stores, safety equipment, spare parts and marine procurement services.</p>
        </div>
      </div>
    </section>

    <!-- PORT CONTENT SECTION -->
    <section class="port-content">
      <div class="container">
        <article class="prose">
{content_html}
        </article>
      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="logo" href="../index.html">
            <img src="../assets/imgs/logo-shipchandler-libya.png" alt="Logo" width="40" height="40">
            <span class="logo-text">
              <strong>ShipChandler</strong>
              <span style="color: var(--yellow);">Libya</span>
            </span>
          </a>
          <p>SHIP CHANDLER LIBYA CO., LTD is a licensed marine supplier providing provisions, technical stores, bonded goods and emergency vessel supply across all Libyan ports and anchorages.</p>
        </div>

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

        <div class="footer-col">
          <h4>Services</h4>
          <ul class="footer-links">
            <li><a href="../services.html#provisions">Provisions Supply</a></li>
            <li><a href="../services.html#bonded">Bonded Stores</a></li>
            <li><a href="../services.html#deck">Deck Stores</a></li>
            <li><a href="../services.html#engine">Engine Stores</a></li>
            <li><a href="../services.html#safety">Safety & PPE</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Contact Us</h4>
          <ul class="footer-contact">
            <li><i class="fas fa-map-marker-alt"></i> Misurata Seaport, Qasr Ahmed, Misurata, Libya</li>
            <li><i class="fab fa-whatsapp"></i> <a href="https://wa.me/2482743244" style="color:inherit;">+248 2 743 244</a></li>
            <li><i class="fas fa-envelope"></i> <a href="mailto:sales@shipchandlerlibya.com" style="color:inherit;">sales@shipchandlerlibya.com</a></li>
            <li><i class="fas fa-user-tie"></i> Omar Ali (Operations Manager)</li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div style="text-align:center; width:100%;">&copy; 2026 SHIP CHANDLER LIBYA CO., LTD. All rights reserved.</div>
      </div>
    </div>
  </footer>

  <!-- FLOATING WHATSAPP -->
  <a href="https://wa.me/2482743244" class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">
    <i class="fab fa-whatsapp"></i>
  </a>

  <!-- Port Pages JS -->
  <script src="../assets/js/port-pages.js"></script>
</body>
</html>'''
    
    # Write the file
    filename = f'ports/{slug}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f'Created: {filename}')

print(f'\n✓ Successfully generated {len(ports_data)} port pages!')
