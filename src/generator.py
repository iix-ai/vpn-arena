import csv
import os
import json
import datetime
import shutil

# Tiandao VPN Generator V4.1 (Stable Fix)
# 修复了 f-string 与 CSS/JS 大括号冲突的问题
# 增强了 CSV 读取的兼容性 (utf-8-sig)

# ================= 配置区 (CSS & JS) =================
# 将样式和脚本剥离，防止 Python 报错
CSS_STYLES = """
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; line-height: 1.6; }
    .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
    /* Top Bar */
    .top-bar { background: #ef4444; color: white; text-align: center; padding: 10px; font-weight: bold; font-size: 14px; }
    .top-bar a { color: white; text-decoration: underline; }
    /* Header */
    header { text-align: center; margin: 40px 0; }
    h1 { font-size: 2.5rem; color: #0f172a; margin-bottom: 10px; }
    /* Cards & Tables */
    .card { background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 25px; margin-bottom: 20px; border: 1px solid #e2e8f0; }
    table { width: 100%; border-collapse: collapse; }
    th { text-align: left; padding: 15px; background: #f1f5f9; color: #64748b; font-size: 0.9rem; }
    td { padding: 15px; border-bottom: 1px solid #e2e8f0; }
    .rank { font-size: 1.5rem; font-weight: 800; color: #cbd5e1; }
    .provider-name { font-weight: bold; font-size: 1.1rem; color: #0f172a; display: block; }
    .badge { background: #dbeafe; color: #1e40af; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
    /* Buttons */
    .btn { display: inline-block; background: #2563eb; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; transition: 0.2s; }
    .btn:hover { background: #1d4ed8; }
    .btn-outline { color: #64748b; text-decoration: none; font-size: 0.9rem; margin-left: 10px; }
    /* Footer */
    footer { text-align: center; margin-top: 60px; color: #94a3b8; font-size: 0.9rem; padding-bottom: 40px; }
    footer a { color: #64748b; text-decoration: none; margin: 0 10px; }
    .disclosure { background: #fffbeb; color: #92400e; padding: 10px; font-size: 0.8rem; border-radius: 6px; display: inline-block; margin-top: 20px; }
    /* Popup */
    .exit-popup { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 999; justify-content: center; align-items: center; }
    .popup-box { background: white; padding: 40px; border-radius: 12px; text-align: center; max-width: 400px; position: relative; }
    .close-btn { position: absolute; top: 10px; right: 15px; cursor: pointer; font-size: 20px; color: #94a3b8; }
"""

JS_SCRIPTS = """
    // Exit Intent Logic
    const popup = document.getElementById('exitPopup');
    const closeBtn = document.querySelector('.close-btn');
    if (popup && closeBtn) {
        closeBtn.onclick = function() { popup.style.display = 'none'; };
        document.addEventListener('mouseleave', (e) => {
            if (e.clientY < 0 && !localStorage.getItem('popupShown')) {
                popup.style.display = 'flex';
                localStorage.setItem('popupShown', 'true');
            }
        });
    }
"""

class VPNGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, 'data', 'vpn_raw.csv')
        self.config_path = os.path.join(self.base_dir, 'config.json')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.static_dir = os.path.join(self.base_dir, 'static')
        
        self.generated_urls = []
        self.config = self.load_config()

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
            except: pass
        return config

    def load_data(self):
        print(f"📂 Loading data from {self.data_path}...")
        if not os.path.exists(self.data_path):
            print("❌ Data file missing!")
            return []
        
        data = []
        try:
            # 使用 utf-8-sig 自动处理 Excel 可能产生的 BOM 头
            with open(self.data_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Provider'):
                        data.append(row)
            return data
        except Exception as e:
            print(f"❌ CSV Error: {e}")
            return []

    def get_affiliate_link(self, provider, original_link):
        clean_name = str(provider).strip().lower()
        mapping = self.config.get('affiliate_map', {})
        for key, link in mapping.items():
            if key.lower() in clean_name and link:
                return link
        return original_link

    def get_head_html(self, title, description):
        ga_script = ""
        if self.config.get('google_analytics_id'):
            ga_script = f"""
            <script async src="https://www.googletagmanager.com/gtag/js?id={self.config['google_analytics_id']}"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){{dataLayer.push(arguments);}}
              gtag('js', new Date());
              gtag('config', '{self.config['google_analytics_id']}');
            </script>"""

        return f"""
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <meta name="description" content="{description}">
            <link rel="icon" href="/static/favicon.png" type="image/png">
            {ga_script}
            <style>{CSS_STYLES}</style>
        </head>
        """

    def generate_index(self, vpns):
        print("🏆 Generating Index Page...")
        
        rows_html = ""
        for index, vpn in enumerate(vpns):
            aff_link = self.get_affiliate_link(vpn['Provider'], vpn.get('Affiliate_Link', '#'))
            detail_slug = f"{str(vpn['Provider']).lower().replace(' ', '-')}-review.html"
            badge_html = f"<span class='badge'>{vpn['Badge']}</span>" if vpn.get('Badge') else ""
            
            rows_html += f"""
            <tr>
                <td class="rank">#{index + 1}</td>
                <td>
                    <span class="provider-name">{vpn['Provider']}</span>
                    {badge_html}
                </td>
                <td>
                    <ul style="margin:0; padding-left:15px; font-size:0.9rem; color:#475569;">
                        <li>Servers: {vpn.get('Server_Count', 'N/A')}</li>
                        <li>Logs: {vpn.get('No_Logs', 'N/A')}</li>
                        <li>Streaming: {vpn.get('Streaming_Support', 'N/A')}</li>
                    </ul>
                </td>
                <td style="font-weight:bold; color:#ef4444;">{vpn.get('Price_Monthly', 'N/A')}</td>
                <td>
                    <a href="{aff_link}" class="btn" target="_blank" rel="nofollow">Visit Site &rarr;</a>
                    <br><br>
                    <a href="{detail_slug}" class="btn-outline">Read Review</a>
                </td>
            </tr>
            """

        top_bar_html = ""
        if self.config['top_bar']['enabled']:
            top_bar_html = f'<div class="top-bar"><a href="{self.config["top_bar"]["link"]}">{self.config["top_bar"]["text"]}</a></div>'

        disclosure_text = self.config.get('legal', {}).get('disclosure', '')

        html = f"""<!DOCTYPE html>
        <html lang="en">
        {self.get_head_html(f"Best VPNs for {self.config.get('year', '2026')} - Ranked & Tested", "Compare top VPNs.")}
        <body>
            {top_bar_html}
            <div class="container">
                <header>
                    <h1>🛡️ {self.config['site_name']}</h1>
                    <p style="color:#64748b; font-size:1.1rem;">Top VPNs for {self.config.get('year', '2026')}</p>
                </header>
                
                <div class="card">
                    <table>
                        <thead>
                            <tr>
                                <th width="5%">Rank</th>
                                <th width="25%">Provider</th>
                                <th>Key Features</th>
                                <th>Price/mo</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>

                <footer>
                    <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                    <div class="disclosure">{disclosure_text}</div>
                    <p><a href="privacy.html">Privacy</a> | <a href="terms.html">Terms</a></p>
                </footer>
            </div>
            
            <div class="exit-popup" id="exitPopup">
                <div class="popup-box">
                    <span class="close-btn">&times;</span>
                    <h2>Wait! Don't Overpay.</h2>
                    <p>We found a secret <strong>68% OFF</strong> deal.</p>
                    <a href="#ranking" class="btn" onclick="document.getElementById('exitPopup').style.display='none'">See Deal</a>
                </div>
            </div>
            <script>{JS_SCRIPTS}</script>
        </body>
        </html>
        """
        
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def generate_details(self, vpns):
        print("📝 Generating Detail Pages...")
        for vpn in vpns:
            aff_link = self.get_affiliate_link(vpn['Provider'], vpn.get('Affiliate_Link', '#'))
            slug = f"{str(vpn['Provider']).lower().replace(' ', '-')}-review.html"
            disclosure_text = self.config.get('legal', {}).get('disclosure', '')
            
            # 简单的模板内容 (后续需升级为真实评测)
            html = f"""<!DOCTYPE html>
            <html lang="en">
            {self.get_head_html(f"{vpn['Provider']} Review - Is it Safe?", f"Review of {vpn['Provider']}.")}
            <body>
                <div class="container">
                    <a href="index.html" style="text-decoration:none; color:#64748b;">&larr; Back to Ranking</a>
                    <header>
                        <h1>{vpn['Provider']} Review</h1>
                        <span class="badge" style="font-size:1rem;">Verdict: Recommended</span>
                    </header>
                    
                    <div class="card" style="text-align:center;">
                        <div style="font-size:3rem; font-weight:800; color:#2563eb;">4.8/5.0</div>
                        <p>Excellent choice for <strong>{vpn.get('Streaming_Support', 'Privacy')}</strong></p>
                        <a href="{aff_link}" class="btn" target="_blank" rel="nofollow">Get {vpn['Provider']} Deal &rarr;</a>
                    </div>

                    <div class="card">
                        <h2>🚀 Performance Specs</h2>
                        <ul>
                            <li><strong>Server Count:</strong> {vpn.get('Server_Count', 'N/A')}</li>
                            <li><strong>Logging Policy:</strong> {vpn.get('No_Logs', 'N/A')}</li>
                            <li><strong>Money-Back:</strong> {vpn.get('Money_Back', '30 Days')}</li>
                            <li><strong>Best Price:</strong> {vpn.get('Price_Monthly', 'N/A')}</li>
                        </ul>
                    </div>
                    
                    <footer>
                        <div class="disclosure">{disclosure_text}</div>
                        <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                    </footer>
                </div>
            </body>
            </html>
            """
            with open(os.path.join(self.output_dir, slug), 'w', encoding='utf-8') as f:
                f.write(html)
            self.generated_urls.append(slug)

    def generate_sitemap(self):
        print("🗺️ Generating Sitemap...")
        base_url = self.config.get('domain', 'https://vpn.ii-x.com')
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += f'<url><loc>{base_url}/</loc><priority>1.0</priority></url>\n'
        for url in self.generated_urls:
            xml += f'<url><loc>{base_url}/{url}</loc><priority>0.8</priority></url>\n'
        xml += '</urlset>'
        with open(os.path.join(self.output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
            f.write(xml)

    def generate_legal(self):
        for page in ['privacy', 'terms']:
            with open(os.path.join(self.output_dir, f'{page}.html'), 'w', encoding='utf-8') as f:
                f.write(f"<h1>{page.capitalize()} Policy</h1><p>Standard {page} text here...</p>")

    def copy_assets(self):
        if os.path.exists(self.static_dir):
            target = os.path.join(self.output_dir, 'static')
            if os.path.exists(target): shutil.rmtree(target)
            shutil.copytree(self.static_dir, target)
        with open(os.path.join(self.output_dir, 'robots.txt'), 'w') as f:
            f.write(f"User-agent: *\nAllow: /\nSitemap: {self.config.get('domain')}/sitemap.xml")

    def run(self):
        print("🚀 Starting VPN Generator V4.1...")
        if os.path.exists(self.output_dir): shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        
        try:
            vpns = self.load_data()
            if not vpns: 
                print("⚠️ Warning: No VPN data found. Generating empty site.")
            
            self.generate_index(vpns)
            self.generate_details(vpns)
            self.generate_sitemap()
            self.generate_legal()
            self.copy_assets()
            print("✅ Build Complete.")
        except Exception as e:
            print(f"❌ FATAL ERROR: {e}")
            raise e

if __name__ == "__main__":
    gen = VPNGenerator()
    gen.run()
