import csv
import os
import json
import datetime
import shutil
import sys

# Tiandao VPN Generator V5.1 (SEO & Content Enhanced)
# 新增：Review Schema, Long Content Rendering, Mobile Optimization

class VPNGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, 'data', 'vpn_raw.csv')
        self.config_path = os.path.join(self.base_dir, 'config.json')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.static_dir = os.path.join(self.base_dir, 'static')
        
        self.generated_urls = []
        self.config = self.load_config()

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
            "legal": {"disclosure": "Advertiser Disclosure: We may receive a commission for purchases made through these links."}
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
                    if row.get('Provider'): data.append(row)
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

    # --- CSS 生成 (增加移动端优化) ---
    def generate_css(self):
        css_content = """
        body { font-family: -apple-system, system-ui, sans-serif; background: #f8fafc; color: #334155; margin: 0; line-height: 1.6; }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .top-bar { background: #ef4444; color: white; text-align: center; padding: 10px; font-weight: bold; font-size: 14px; }
        .top-bar a { color: white; text-decoration: underline; }
        header { text-align: center; margin: 40px 0; }
        h1 { font-size: 2.5rem; color: #0f172a; margin-bottom: 10px; }
        
        /* 移动端表格优化 */
        .table-wrapper { overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .card { background: white; border-radius: 12px; padding: 25px; margin-bottom: 20px; border: 1px solid #e2e8f0; }
        
        table { width: 100%; border-collapse: collapse; min-width: 600px; } /* 最小宽度防止挤压 */
        th { text-align: left; padding: 15px; background: #f1f5f9; color: #64748b; font-size: 0.9rem; }
        td { padding: 15px; border-bottom: 1px solid #e2e8f0; }
        
        .rank { font-size: 1.5rem; font-weight: 800; color: #cbd5e1; }
        .provider-name { font-weight: bold; font-size: 1.1rem; color: #0f172a; display: block; }
        .badge { background: #dbeafe; color: #1e40af; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
        .btn { display: inline-block; background: #2563eb; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; transition: 0.2s; }
        .btn:hover { background: #1d4ed8; }
        .btn-outline { color: #64748b; text-decoration: none; font-size: 0.9rem; margin-left: 10px; }
        
        /* 详情页样式 */
        .review-content { font-size: 1.1rem; color: #334155; text-align: left; margin-top: 20px; }
        .review-content h3 { color: #0f172a; margin-top: 30px; }
        .score-box { background: #f0f9ff; border: 1px solid #bae6fd; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 30px; }
        .score-num { font-size: 3.5rem; font-weight: 800; color: #0284c7; line-height: 1; }
        
        footer { text-align: center; margin-top: 60px; color: #94a3b8; font-size: 0.9rem; padding-bottom: 40px; }
        footer a { color: #64748b; text-decoration: none; margin: 0 10px; }
        .disclosure { background: #fffbeb; color: #92400e; padding: 10px; font-size: 0.8rem; border-radius: 6px; display: inline-block; margin-top: 20px; }
        
        .exit-popup { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 999; justify-content: center; align-items: center; }
        .popup-box { background: white; padding: 40px; border-radius: 12px; text-align: center; max-width: 400px; position: relative; }
        .close-btn { position: absolute; top: 10px; right: 15px; cursor: pointer; font-size: 20px; color: #94a3b8; }
        """
        static_out = os.path.join(self.output_dir, 'static')
        if not os.path.exists(static_out): os.makedirs(static_out)
        with open(os.path.join(static_out, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)

    def get_head_html(self, title, description, schema_json=None):
        ga_script = ""
        if self.config.get('google_analytics_id'):
            ga_script = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={self.config['google_analytics_id']}"></script>
            <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{self.config['google_analytics_id']}');</script>"""
        
        schema_html = f'<script type="application/ld+json">{schema_json}</script>' if schema_json else ""

        return f"""<head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title><meta name="description" content="{description}">
            <link rel="icon" href="/static/favicon.png" type="image/png"><link rel="stylesheet" href="/static/style.css">
            {ga_script}{schema_html}
        </head>"""

    def generate_index(self, vpns):
        self.log("🏆 Generating Index Page...")
        rows_html = ""
        for index, vpn in enumerate(vpns):
            aff_link = self.get_affiliate_link(vpn['Provider'], vpn.get('Affiliate_Link', '#'))
            detail_slug = f"{str(vpn['Provider']).lower().replace(' ', '-')}-review.html"
            badge_html = f"<span class='badge'>{vpn['Badge']}</span>" if vpn.get('Badge') else ""
            
            rows_html += f"""
            <tr>
                <td class="rank">#{index + 1}</td>
                <td><span class="provider-name">{vpn['Provider']}</span>{badge_html}</td>
                <td><ul style="margin:0; padding-left:15px; font-size:0.9rem; color:#475569;">
                    <li>Servers: {vpn.get('Server_Count', 'N/A')}</li>
                    <li>Logs: {vpn.get('No_Logs', 'N/A')}</li>
                    <li>Streaming: {vpn.get('Streaming_Support', 'N/A')}</li>
                </ul></td>
                <td style="font-weight:bold; color:#ef4444;">{vpn.get('Price_Monthly', 'N/A')}</td>
                <td>
                    <a href="{aff_link}" class="btn" target="_blank" rel="nofollow">Visit Site &rarr;</a>
                    <br><br><a href="{detail_slug}" class="btn-outline">Read Review</a>
                </td>
            </tr>"""

        top_bar_html = ""
        if self.config['top_bar']['enabled']:
            top_bar_html = f'<div class="top-bar"><a href="{self.config["top_bar"]["link"]}">{self.config["top_bar"]["text"]}</a></div>'

        html = f"""<!DOCTYPE html><html lang="en">
        {self.get_head_html(f"Best VPNs for {self.config.get('year', '2026')} - Ranked & Tested", "Compare the top VPNs for speed, privacy and streaming.")}
        <body>
            {top_bar_html}
            <div class="container">
                <header>
                    <h1>🛡️ {self.config['site_name']}</h1>
                    <p style="color:#64748b; font-size:1.1rem;">We tested 50+ VPNs. Here are the winners for {self.config.get('year', '2026')}.</p>
                </header>
                <div class="table-wrapper">
                    <div class="card" style="margin:0; border:none; box-shadow:none;">
                        <table>
                            <thead><tr><th width="5%">Rank</th><th width="25%">Provider</th><th>Key Features</th><th>Price/mo</th><th>Action</th></tr></thead>
                            <tbody>{rows_html}</tbody>
                        </table>
                    </div>
                </div>
                <footer>
                    <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                    <div class="disclosure">{self.config.get('legal', {}).get('disclosure', '')}</div>
                    <p><a href="privacy.html">Privacy</a> | <a href="terms.html">Terms</a></p>
                </footer>
            </div>
            <div class="exit-popup" id="exitPopup">
                <div class="popup-box">
                    <span class="close-btn" onclick="document.getElementById('exitPopup').style.display='none'">&times;</span>
                    <h2>Wait! Don't Overpay.</h2><p>We found a secret <strong>68% OFF</strong> deal.</p>
                    <a href="#ranking" class="btn" onclick="document.getElementById('exitPopup').style.display='none'">See Deal</a>
                </div>
            </div>
            <script>
                document.addEventListener('mouseleave', (e) => {{
                    if (e.clientY < 0 && !localStorage.getItem('popupShown')) {{
                        document.getElementById('exitPopup').style.display = 'flex';
                        localStorage.setItem('popupShown', 'true');
                    }}
                }});
            </script>
        </body></html>"""
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f: f.write(html)

    def generate_details(self, vpns):
        self.log("📝 Generating Detail Pages...")
        for vpn in vpns:
            provider = vpn['Provider']
            aff_link = self.get_affiliate_link(provider, vpn.get('Affiliate_Link', '#'))
            slug = f"{str(provider).lower().replace(' ', '-')}-review.html"
            
            # --- 核心优化：长文内容回退逻辑 ---
            # 如果 CSV 里有 'Long_Review' 列且不为空，则显示；否则显示默认模板
            long_review = vpn.get('Long_Review', '')
            if not long_review or len(long_review) < 50:
                long_review = f"""
                <h3>Why we recommend {provider}</h3>
                <p>{provider} has consistently performed well in our speed and security tests. With {vpn.get('Server_Count','thousands of')} servers worldwide, it ensures you can access your favorite content from anywhere.</p>
                <h3>Streaming Capabilities</h3>
                <p>During our tests, {provider} successfully unlocked {vpn.get('Streaming_Support', 'major streaming platforms')}. The connection remained stable with no buffering.</p>
                <h3>Privacy & Security</h3>
                <p>The company adheres to a strict '{vpn.get('No_Logs', 'No Logs')}' policy. This means your browsing history is never recorded.</p>
                """

            # --- 核心优化：生成 Review Schema (JSON-LD) ---
            schema_data = {
                "@context": "https://schema.org/",
                "@type": "Product",
                "name": provider,
                "description": f"In-depth review of {provider} VPN service.",
                "review": {
                    "@type": "Review",
                    "reviewRating": {
                        "@type": "Rating",
                        "ratingValue": "4.8",
                        "bestRating": "5"
                    },
                    "author": {"@type": "Organization", "name": self.config['site_name']}
                }
            }
            schema_json = json.dumps(schema_data)

            html = f"""<!DOCTYPE html><html lang="en">
            {self.get_head_html(f"{provider} Review {self.config.get('year', '2026')} - Safe or Scam?", f"Full review of {provider}. Speed tests, pricing, and features analysis.", schema_json)}
            <body>
                <div class="container">
                    <a href="index.html" style="text-decoration:none; color:#64748b;">&larr; Back to Ranking</a>
                    <header>
                        <h1>{provider} Review</h1>
                        <p style="color:#64748b">Updated: {datetime.datetime.now().strftime('%B %Y')}</p>
                    </header>
                    
                    <div class="score-box">
                        <div class="score-num">4.8</div>
                        <div style="font-weight:bold; font-size:1.2rem; color:#0f172a; margin-top:10px;">Excellent Choice</div>
                        <a href="{aff_link}" class="btn" style="margin-top:20px; padding:15px 40px; font-size:1.1rem;" target="_blank" rel="nofollow">Get {provider} Deal &rarr;</a>
                        <p style="font-size:0.8rem; margin-top:10px; color:#64748b;">30-Day Money-Back Guarantee</p>
                    </div>

                    <div class="card">
                        <h2>🚀 Performance Specs</h2>
                        <ul style="list-style:none; padding:0; display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                            <li style="background:#f1f5f9; padding:10px; border-radius:6px;"><strong>Servers:</strong> {vpn.get('Server_Count', 'N/A')}</li>
                            <li style="background:#f1f5f9; padding:10px; border-radius:6px;"><strong>Logs:</strong> {vpn.get('No_Logs', 'N/A')}</li>
                            <li style="background:#f1f5f9; padding:10px; border-radius:6px;"><strong>Streaming:</strong> {vpn.get('Streaming_Support', 'N/A')}</li>
                            <li style="background:#f1f5f9; padding:10px; border-radius:6px;"><strong>Price:</strong> {vpn.get('Price_Monthly', 'N/A')}</li>
                        </ul>
                    </div>

                    <div class="card review-content">
                        {long_review}
                    </div>
                    
                    <footer>
                        <div class="disclosure">{self.config.get('legal', {}).get('disclosure', '')}</div>
                        <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                    </footer>
                </div>
            </body></html>"""
            with open(os.path.join(self.output_dir, slug), 'w', encoding='utf-8') as f: f.write(html)

    def generate_sitemap(self):
        self.log("🗺️ Generating Sitemap...")
        base_url = self.config.get('domain', 'https://vpn.ii-x.com')
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += f'<url><loc>{base_url}/</loc><priority>1.0</priority></url>\n'
        for url in self.generated_urls: xml += f'<url><loc>{base_url}/{url}</loc><priority>0.8</priority></url>\n'
        xml += '</urlset>'
        with open(os.path.join(self.output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f: f.write(xml)

    def generate_legal(self):
        for page in ['privacy', 'terms']:
            with open(os.path.join(self.output_dir, f'{page}.html'), 'w', encoding='utf-8') as f:
                f.write(f"<h1>{page.capitalize()} Policy</h1><p>Standard {page} text here...</p>")

    def copy_assets(self):
        with open(os.path.join(self.output_dir, 'robots.txt'), 'w') as f:
            f.write(f"User-agent: *\nAllow: /\nSitemap: {self.config.get('domain')}/sitemap.xml")
        if os.path.exists(os.path.join(self.static_dir, 'favicon.png')):
             shutil.copy(os.path.join(self.static_dir, 'favicon.png'), os.path.join(self.output_dir, 'static', 'favicon.png'))

    def run(self):
        self.log("🚀 Starting VPN Generator V5.1...")
        if os.path.exists(self.output_dir): 
            try: shutil.rmtree(self.output_dir)
            except: pass
        os.makedirs(self.output_dir)
        self.generate_css()
        vpns = self.load_data()
        if not vpns: 
            with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f: f.write("<h1>Maintenance</h1>")
            return
        try:
            self.generate_index(vpns)
            self.generate_details(vpns)
            self.generate_sitemap()
            self.generate_legal()
            self.copy_assets()
            self.log("✅ Build Complete.")
        except Exception as e: self.log(f"❌ BUILD FAILED: {e}")

if __name__ == "__main__":
    gen = VPNGenerator()
    gen.run()
