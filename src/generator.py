import csv
import os
import json
import datetime
import shutil
import sys
import base64

# Tiandao VPN Generator V5.0 (SEO Enhanced & Schema Markup)
# 核心升级：适配 n8n V7.0 数据结构，注入 Google 星级评分与富文本摘要

class VPNGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, 'data', 'vpn_raw.csv')
        self.config_path = os.path.join(self.base_dir, 'config.json')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.static_dir = os.path.join(self.base_dir, 'static')
        self.generated_urls = []
        self.config = self.load_config()

        # VPN 域名修正字典
        self.domain_map = {
            "Private Internet Access": "privateinternetaccess.com",
            "PIA": "privateinternetaccess.com",
            "PureVPN": "purevpn.com",
            "IPVanish": "ipvanish.com",
            "ProtonVPN": "protonvpn.com",
            "Windscribe": "windscribe.com",
            "TunnelBear": "tunnelbear.com",
            "Hide.me": "hide.me",
            "Mullvad": "mullvad.net",
            "Atlas VPN": "atlasvpn.com",
            "StrongVPN": "strongvpn.com",
            "PrivadoVPN": "privadovpn.com",
            "NordVPN": "nordvpn.com",
            "ExpressVPN": "expressvpn.com",
            "Surfshark": "surfshark.com",
            "CyberGhost": "cyberghostvpn.com"
        }

    def log(self, message):
        print(f"[VPN-GEN] {message}")

    def load_config(self):
        config = {
            "site_name": "Privacy Shield VPN",
            "domain": "https://vpn.ii-x.com",
            "year": "2026",
            "google_analytics_id": "",
            "affiliate_map": {}, 
            "top_bar": {"enabled": True, "text": "🔥 Limited Time: Get 68% OFF Top VPNs!", "link": "#ranking"},
            "legal": {"disclosure": "Advertiser Disclosure: We are reader-supported. We may receive a commission for purchases made through these links."}
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    config.update(loaded)
                self.log("✅ Config loaded.")
            except: pass
        return config

    def load_data(self):
        self.log(f"📂 Loading data from {self.data_path}...")
        if not os.path.exists(self.data_path): return []
        data = []
        try:
            with open(self.data_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Provider'): 
                        # 数据清洗：处理 CSV 可能存在的空格
                        clean_row = {k.strip(): v for k, v in row.items() if k}
                        data.append(clean_row)
            self.log(f"✅ Loaded {len(data)} VPNs.")
            return data
        except Exception as e:
            self.log(f"❌ CSV Error: {e}")
            return []

    def get_affiliate_link(self, provider, original_link):
        clean_name = str(provider).strip().lower()
        mapping = self.config.get('affiliate_map', {})
        for key, link in mapping.items():
            if key.lower() in clean_name and link: return link
        return original_link
    
    def get_real_domain(self, provider_name):
        clean = str(provider_name).strip()
        if clean in self.domain_map:
            return self.domain_map[clean]
        return f"{clean.lower().replace(' ', '')}.com"

    # --- Schema Markup 生成器 (让 Google 显示星星) ---
    def generate_schema_json(self, vpn):
        provider = vpn['Provider']
        rating = vpn.get('star_rating', '4.5')
        try:
            rating_val = float(rating)
        except:
            rating_val = 4.5
            
        schema = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": provider,
            "description": vpn.get('seo_meta_desc', f"Review of {provider}"),
            "review": {
                "@type": "Review",
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": str(rating_val),
                    "bestRating": "5"
                },
                "author": {
                    "@type": "Organization",
                    "name": self.config['site_name']
                }
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": str(rating_val),
                "reviewCount": "1280"
            }
        }
        return json.dumps(schema)

    def get_common_script(self):
        return """
        <script>
            function triggerExitPopup() {
                if (localStorage.getItem('hasSeenExitPopup') === 'yes') return;
                var popup = document.getElementById('exitPopup');
                if (popup) {
                    popup.style.display = 'flex';
                    localStorage.setItem('hasSeenExitPopup', 'yes');
                }
            }
            document.addEventListener('mouseleave', function(e) {
                if (e.clientY < 0) triggerExitPopup();
            });
            function closePopup() { document.getElementById('exitPopup').style.display = 'none'; }
            function topBarClick() { triggerExitPopup(); }
        </script>
        """

    def generate_css(self):
        css_content = """
        :root { --primary: #2563eb; --secondary: #1e40af; --accent: #ef4444; --bg: #f8fafc; --text: #1e293b; --star: #f59e0b; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); margin: 0; line-height: 1.6; display: flex; flex-direction: column; min-height: 100vh; }
        .container { max-width: 1100px; margin: 0 auto; padding: 20px; width: 100%; box-sizing: border-box; flex: 1; }
        
        /* Top Bar */
        .top-bar { position: sticky; top: 0; z-index: 9000; background: var(--accent); color: white; text-align: center; padding: 12px; font-weight: 700; font-size: 14px; cursor: pointer; transition: background 0.2s; user-select: none; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .top-bar:hover { background: #dc2626; text-decoration: underline; }
        
        /* Headers */
        header { text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: white; border-radius: 0 0 20px 20px; margin-bottom: 40px; }
        h1 { font-size: 2.5rem; margin: 0 0 15px 0; letter-spacing: -1px; }
        .subtitle { font-size: 1.2rem; color: #94a3b8; max-width: 600px; margin: 0 auto; }
        
        /* Champion Card */
        .champion-card { background: white; border: 2px solid var(--primary); border-radius: 16px; padding: 30px; margin-bottom: 40px; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.2); position: relative; overflow: hidden; }
        .ribbon { position: absolute; top: 0; right: 0; background: var(--primary); color: white; padding: 8px 15px; border-bottom-left-radius: 12px; font-weight: bold; font-size: 0.9rem; }
        
        /* Tables */
        .card { background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; overflow: hidden; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th { text-align: left; padding: 18px; background: #f8fafc; color: #64748b; font-size: 0.85rem; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; }
        td { padding: 20px 18px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }
        tr:hover { background-color: #f8fafc; }
        
        /* New Elements (Stars & Badges) */
        .star-rating { color: var(--star); font-weight: 800; letter-spacing: 1px; white-space: nowrap; }
        .rank-circle { width: 32px; height: 32px; background: #f1f5f9; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #94a3b8; }
        .rank-1 { background: #fef3c7; color: #d97706; border: 2px solid #fcd34d; }
        .badge { background: #dbeafe; color: var(--primary); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; white-space: nowrap; display: inline-block; margin-top: 5px; }
        .badge-green { background: #dcfce7; color: #166534; }
        
        /* Pros & Cons Box */
        .pros-cons { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px; background: #f8fafc; padding: 20px; border-radius: 12px; }
        .pros h3 { color: #166534; margin-top: 0; font-size: 1.1rem; }
        .cons h3 { color: #991b1b; margin-top: 0; font-size: 1.1rem; }
        .pro-item, .con-item { margin-bottom: 8px; font-size: 0.95rem; }
        .pro-item:before { content: "✅ "; }
        .con-item:before { content: "❌ "; }

        /* Buttons */
        .btn { display: inline-block; background: var(--primary); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; transition: 0.2s; white-space: nowrap; text-align: center; cursor: pointer; }
        .btn:hover { background: var(--secondary); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }
        .btn-outline { color: #475569; text-decoration: none; font-size: 0.9rem; margin-top: 10px; display: inline-block; border: 1px solid #cbd5e1; padding: 8px 16px; border-radius: 6px; transition: 0.2s; background: white; cursor: pointer; }
        .btn-outline:hover { border-color: var(--primary); color: var(--primary); background: #eff6ff; }
        
        .breadcrumbs { font-size: 0.9rem; color: #64748b; margin-bottom: 20px; }
        .breadcrumbs a { color: var(--primary); text-decoration: none; }
        .breadcrumbs span { margin: 0 8px; color: #cbd5e1; }

        /* Mobile */
        @media (max-width: 768px) {
            header { padding: 30px 20px; }
            h1 { font-size: 1.8rem; }
            thead { display: none; }
            tr { display: flex; flex-direction: column; padding: 20px; border-bottom: 8px solid #f8fafc; }
            td { padding: 5px 0; border: none; }
            .pros-cons { grid-template-columns: 1fr; }
            .btn, .btn-outline { display: block; width: 100%; margin-top: 10px; box-sizing: border-box; }
        }

        footer { text-align: center; margin-top: auto; color: #94a3b8; font-size: 0.9rem; padding: 40px 0; background: #fff; border-top: 1px solid #f1f5f9; }
        .disclosure { background: #fffbeb; color: #92400e; padding: 12px; font-size: 0.85rem; border-radius: 8px; display: inline-block; margin-top: 20px; max-width: 600px; }
        
        .exit-popup { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 99999; justify-content: center; align-items: center; backdrop-filter: blur(5px); }
        .popup-box { background: white; padding: 40px; border-radius: 16px; text-align: center; max-width: 400px; position: relative; animation: popIn 0.3s ease; }
        @keyframes popIn { from {transform: scale(0.9); opacity: 0;} to {transform: scale(1); opacity: 1;} }
        .close-btn { position: absolute; top: 15px; right: 20px; cursor: pointer; font-size: 24px; color: #cbd5e1; }
        """
        static_out = os.path.join(self.output_dir, 'static')
        if not os.path.exists(static_out): os.makedirs(static_out)
        with open(os.path.join(static_out, 'style.css'), 'w', encoding='utf-8') as f: f.write(css_content)

    def get_head_html(self, title, description, schema_json=None):
        ga_script = ""
        if self.config.get('google_analytics_id') and self.config['google_analytics_id'].startswith("G-"):
            ga_script = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={self.config['google_analytics_id']}"></script>
            <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{self.config['google_analytics_id']}');</script>"""
        
        schema_html = f'<script type="application/ld+json">{schema_json}</script>' if schema_json else ""
        favicon_base64 = "data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛡️</text></svg>"

        return f"""<head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title><meta name="description" content="{description}">
            <link rel="icon" href="{favicon_base64}">
            <link rel="stylesheet" href="/static/style.css">
            {ga_script}{schema_html}
        </head>"""

    def generate_index(self, vpns):
        self.log("🏆 Generating Index Page...")
        
        champion = vpns[0] if vpns else None
        champion_html = ""
        if champion:
            aff_link = self.get_affiliate_link(champion['Provider'], champion.get('Affiliate_Link', '#'))
            slug = f"{str(champion['Provider']).lower().replace(' ', '-')}-review.html"
            logo_url = f"https://www.google.com/s2/favicons?domain={self.get_real_domain(champion['Provider'])}&sz=128"
            
            # 使用新字段
            rating = champion.get('star_rating', '4.9')
            best_for = champion.get('best_for', 'All-Rounder')
            
            champion_html = f"""
            <div class="champion-card">
                <div class="ribbon">🏆 #1 RANKED</div>
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
                    <div style="flex:1;">
                        <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                            <img src="{logo_url}" style="width:48px; height:48px; border-radius:50%; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                            <h2 style="margin:0; font-size:1.8rem;">{champion['Provider']}</h2>
                        </div>
                        <p style="margin:0; color:#64748b;">The best overall VPN for speed, security, and streaming in 2026.</p>
                        <div style="margin-top:15px;">
                            <span class="badge">🚀 Fastest</span>
                            <span class="badge badge-green">🏆 {best_for}</span>
                            <span class="star-rating" style="margin-left:10px;">⭐⭐⭐⭐⭐ {rating}</span>
                        </div>
                    </div>
                    <div style="text-align:center; min-width:150px;">
                        <div class="price">{champion.get('Price_Monthly', 'N/A')}</div>
                        <div class="period">per month</div>
                        <a href="{aff_link}" class="btn" style="width:100%; box-sizing:border-box; margin-top:10px; background:#ef4444;">Get Deal &rarr;</a>
                        <a href="{slug}" class="btn-outline">📖 Read Review</a>
                    </div>
                </div>
            </div>"""

        rows_html = ""
        for index, vpn in enumerate(vpns):
            aff_link = self.get_affiliate_link(vpn['Provider'], vpn.get('Affiliate_Link', '#'))
            detail_slug = f"{str(vpn['Provider']).lower().replace(' ', '-')}-review.html"
            logo_url = f"https://www.google.com/s2/favicons?domain={self.get_real_domain(vpn['Provider'])}&sz=64"
            rank_class = "rank-1" if index == 0 else ""
            rating = vpn.get('star_rating', '4.5')
            
            rows_html += f"""
            <tr onclick="window.location='{detail_slug}'" style="cursor:pointer;">
                <td width="5%"><div class="rank-circle {rank_class}">#{index + 1}</div></td>
                <td width="30%">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <img src="{logo_url}" style="width:24px; height:24px; border-radius:4px;">
                        <div>
                            <div style="font-weight:bold; color:#0f172a;">{vpn['Provider']}</div>
                            <div class="star-rating" style="font-size:0.8rem;">⭐⭐⭐⭐⭐ {rating}</div>
                        </div>
                    </div>
                </td>
                <td><ul style="margin:0; padding-left:15px; font-size:0.85rem; color:#64748b;">
                    <li><b>Best For:</b> {vpn.get('best_for', 'Privacy')}</li>
                    <li>Streaming: {vpn.get('Streaming_Support', 'N/A')}</li>
                </ul></td>
                <td width="15%"><div style="font-weight:800; font-size:1.1rem; color:#0f172a;">{vpn.get('Price_Monthly', 'N/A')}</div></td>
                <td width="20%">
                    <a href="{aff_link}" class="btn" onclick="event.stopPropagation();" target="_blank" rel="nofollow">Visit Site</a>
                    <a href="{detail_slug}" class="btn-outline" onclick="event.stopPropagation();">Review</a>
                </td>
            </tr>"""

        top_bar_html = f'''<div class="top-bar" onclick="topBarClick()">{self.config["top_bar"]["text"]}</div>''' if self.config['top_bar']['enabled'] else ""

        html = f"""<!DOCTYPE html><html lang="en">
        {self.get_head_html(f"Best VPNs for {self.config.get('year', '2026')} - Speed & Privacy Tested", "Compare top VPNs used by experts. Find the fastest, most secure VPN for streaming and gaming.")}
        <body>
            {top_bar_html}
            <header>
                <div class="container">
                    <h1>🛡️ {self.config['site_name']}</h1>
                    <p class="subtitle">Trusted by 2M+ users. We tested 50+ VPNs for speed & security.</p>
                </div>
            </header>
            <div class="container" style="margin-top:-60px;">
                {champion_html}
                <div class="card">
                    <table>
                        <thead><tr><th>Rank</th><th>Provider</th><th>Verdict</th><th>Price</th><th>Action</th></tr></thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>
                <footer>
                    <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                    <div class="disclosure">{self.config.get('legal', {}).get('disclosure', 'Advertiser Disclosure: We are reader-supported.')}</div>
                    <p style="margin-top:20px;"><a href="privacy.html">Privacy Policy</a> • <a href="terms.html">Terms</a></p>
                </footer>
            </div>
            <div class="exit-popup" id="exitPopup">
                <div class="popup-box">
                    <span class="close-btn" onclick="closePopup()">&times;</span>
                    <div style="font-size:3rem; margin-bottom:10px;">🎁</div>
                    <h2>Wait! Don't Overpay.</h2>
                    <p>We found a secret <strong>68% OFF</strong> deal.</p>
                    <a href="#ranking" class="btn" onclick="closePopup()" style="width:100%; box-sizing:border-box; margin-top:15px; background:#ef4444;">Claim Discount</a>
                </div>
            </div>
            {self.get_common_script()}
        </body></html>"""
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f: f.write(html)

    def generate_details(self, vpns):
        self.log("📝 Generating Detail Pages...")
        for vpn in vpns:
            provider = vpn['Provider']
            aff_link = self.get_affiliate_link(provider, vpn.get('Affiliate_Link', '#'))
            slug = f"{str(provider).lower().replace(' ', '-')}-review.html"
            logo_url = f"https://www.google.com/s2/favicons?domain={self.get_real_domain(provider)}&sz=128"
            long_review = vpn.get('Long_Review', '')
            if not long_review or len(long_review) < 50:
                long_review = f"<h3>Why {provider}?</h3><p>Detailed review coming soon...</p>"

            # SEO 字段
            seo_title = vpn.get('seo_title', f"{provider} Review 2026 - Is It Safe?")
            seo_desc = vpn.get('seo_meta_desc', f"Read our honest review of {provider}. Speed test results and security analysis.")
            rating = vpn.get('star_rating', '4.5')
            
            # 优缺点处理
            pros = vpn.get('pros_list', '').split('|')
            cons = vpn.get('cons_list', '').split('|')
            pros_html = "".join([f'<div class="pro-item">{p.strip()}</div>' for p in pros if p.strip()])
            cons_html = "".join([f'<div class="con-item">{p.strip()}</div>' for p in cons if p.strip()])
            
            pros_cons_box = ""
            if pros_html or cons_html:
                pros_cons_box = f"""
                <div class="pros-cons">
                    <div class="pros"><h3>What We Like</h3>{pros_html}</div>
                    <div class="cons"><h3>What Could Be Better</h3>{cons_html}</div>
                </div>
                """

            top_bar_html = f'''<div class="top-bar" onclick="topBarClick()">🔥 Limited Time: Get 68% OFF {provider}!</div>'''
            disclaimer = self.config.get('legal', {}).get('disclosure', 'Advertiser Disclosure: We are reader-supported.')
            
            # 生成 Schema
            schema_json = self.generate_schema_json(vpn)

            html = f"""<!DOCTYPE html><html lang="en">
            {self.get_head_html(seo_title, seo_desc, schema_json)}
            <body>
                {top_bar_html}
                <div class="container" style="margin-top:20px;">
                    <div class="breadcrumbs">
                        <a href="index.html">Home</a> <span>/</span> Reviews <span>/</span> {provider}
                    </div>
                    <div class="card" style="padding:40px; text-align:center;">
                        <img src="{logo_url}" style="width:64px; height:64px; border-radius:50%; margin-bottom:20px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                        <h1 style="margin:0;">{provider} Review</h1>
                        <div class="star-rating" style="margin:10px 0; font-size:1.2rem;">⭐⭐⭐⭐⭐ {rating}/5.0</div>
                        <a href="{aff_link}" class="btn" style="margin-top:20px; font-size:1.1rem; padding:15px 30px;" target="_blank" rel="nofollow">Get 68% OFF {provider} &rarr;</a>
                    </div>
                    
                    <div class="card" style="margin-top:20px; padding:40px;">
                        {pros_cons_box}
                        <div style="max-width:800px; margin:20px auto; line-height:1.8;">
                            {long_review}
                        </div>
                    </div>
                    
                    <footer>
                        <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                        <div class="disclosure">{disclaimer}</div>
                        <p style="margin-top:20px;"><a href="privacy.html">Privacy</a> • <a href="terms.html">Terms</a></p>
                    </footer>
                </div>
                <div class="exit-popup" id="exitPopup">
                    <div class="popup-box">
                        <span class="close-btn" onclick="closePopup()">&times;</span>
                        <div style="font-size:3rem; margin-bottom:10px;">🎁</div>
                        <h2>Wait! Don't Overpay.</h2>
                        <p>We found a secret <strong>68% OFF</strong> deal.</p>
                        <a href="{aff_link}" class="btn" style="width:100%; box-sizing:border-box; margin-top:15px; background:#ef4444;">Claim Discount</a>
                    </div>
                </div>
                {self.get_common_script()}
            </body></html>"""
            with open(os.path.join(self.output_dir, slug), 'w', encoding='utf-8') as f: f.write(html)

    def generate_legal(self):
        for page in ['privacy', 'terms']:
            title = f"{page.capitalize()} Policy"
            content = "<p>Your privacy is important to us. We use Google Analytics to improve user experience.</p>" if page == 'privacy' else "<p>By using this site, you agree to our terms.</p>"
            html = f"""<!DOCTYPE html><html lang="en">
            {self.get_head_html(title, title)}
            <body>
                <div class="container">
                    <header style="padding:40px; margin-bottom:20px;"><h1>{title}</h1></header>
                    <div class="card legal-content" style="padding:40px;">{content}</div>
                    <footer><p><a href="index.html">Back to Home</a></p></footer>
                </div>
            </body></html>"""
            with open(os.path.join(self.output_dir, f'{page}.html'), 'w', encoding='utf-8') as f: f.write(html)

    def generate_sitemap(self):
        base_url = self.config.get('domain', 'https://vpn.ii-x.com')
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += f'<url><loc>{base_url}/</loc><priority>1.0</priority></url>\n'
        for url in self.generated_urls: xml += f'<url><loc>{base_url}/{url}</loc><priority>0.8</priority></url>\n'
        xml += '</urlset>'
        with open(os.path.join(self.output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f: f.write(xml)
        with open(os.path.join(self.output_dir, 'robots.txt'), 'w') as f: f.write(f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml")

    def run(self):
        self.log("🚀 Starting VPN Generator V5.0 (SEO & Schema)...")
        if os.path.exists(self.output_dir): 
            try: shutil.rmtree(self.output_dir)
            except: pass
        os.makedirs(self.output_dir)
        self.generate_css()
        vpns = self.load_data()
        if not vpns:
            self.log("⚠️ No VPN data found. Generating placeholder.")
            with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f: f.write("<h1>Coming Soon</h1>")
            return
        try:
            self.generate_index(vpns)
            self.generate_details(vpns)
            self.generate_legal()
            self.generate_sitemap()
            self.log("✅ Build Complete.")
        except Exception as e: self.log(f"❌ BUILD FAILED: {e}")

if __name__ == "__main__":
    gen = VPNGenerator()
    gen.run()
