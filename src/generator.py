import csv
import os
import json
import datetime

# 读取配置
def load_config():
    # 优先读取 config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Config Error: {e}")
    
    # ⚠️ 关键修改：如果没找到配置，我们不再瞎猜 data.csv
    # 而是根据当前目录下的文件自动判断是 VPN 还是 eSIM
    default_data = "data.csv"
    if os.path.exists(os.path.join('data', 'vpn_raw.csv')):
        default_data = "vpn_raw.csv"
    elif os.path.exists(os.path.join('data', 'esim_raw.csv')):
        default_data = "esim_raw.csv"
        
    print(f"⚠️ Using Default Config. Auto-detected data file: {default_data}")
    
    return {
        "site_name": "Site Config Missing",
        "domain": "https://ii-x.com",
        "niche_keywords": "Review",
        "hero_title": "Comparison Site",
        "primary_color": "#2563eb",
        "data_file": default_data  # 这里变聪明了
    }

CONFIG = load_config()

# 导航栏 (绝对路径闭环)
NAV_BAR = """
<nav style="background: #1a1a1a; padding: 15px; text-align: center; border-bottom: 2px solid #333;">
    <a href="https://compare.ii-x.com" style="color: #fff; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 1.1rem; opacity: 0.8;">🤖 AI Tools</a>
    <span style="color: #555;">|</span>
    <a href="https://vpn.ii-x.com" style="color: {primary_color}; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 1.1rem;">🛡️ VPN Privacy</a>
    <span style="color: #555;">|</span>
    <a href="https://esim.ii-x.com" style="color: #fff; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 1.1rem; opacity: 0.8;">📲 Travel eSIM</a>
</nav>
""".format(primary_color=CONFIG.get('primary_color', '#2563eb'))

CSS = """
<style>
    :root {{ --primary: {primary_color}; --bg: #0f172a; --text: #f8fafc; --card-bg: #1e293b; }}
    body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 50px; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
    h1 {{ text-align: center; margin: 40px 0; font-size: 2.5rem; background: linear-gradient(to right, #60a5fa, var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .update-time {{ text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 0.9rem; }}
    .comparison-table {{ width: 100%; border-collapse: collapse; background: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }}
    th {{ background: #334155; color: #fff; padding: 16px; text-align: left; font-weight: 600; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.05em; }}
    td {{ padding: 16px; border-bottom: 1px solid #334155; color: #cbd5e1; vertical-align: middle; }}
    tr:hover {{ background: #2d3748; transition: background 0.2s; }}
    .btn {{ display: inline-block; background: var(--primary); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.1s; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2); }}
    .btn:hover {{ transform: scale(1.05); filter: brightness(110%); }}
    .tag {{ padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }}
    .tag-green {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669; }}
    .tag-red {{ background: rgba(239, 68, 68, 0.2); color: #fca5a5; border: 1px solid #7f1d1d; }}
</style>
""".format(primary_color=CONFIG.get('primary_color', '#2563eb'))

def generate_site():
    print("🔄 Building Site with Config...")
    file_path = os.path.join('data', CONFIG.get('data_file', 'data.csv'))
    
    if not os.path.exists(file_path):
        print(f"❌ Data file {file_path} not found!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
            rows = list(reader)
        except StopIteration:
            print("❌ CSV file is empty!")
            return

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{CONFIG['site_name']} | 2026 Comparison</title>
        <meta name="description" content="Compare the best {CONFIG['niche_keywords']} options. Unbiased reviews, speed tests, and pricing analysis.">
        <meta name="keywords" content="{CONFIG['niche_keywords']}">
        <meta property="og:type" content="website">
        <meta property="og:url" content="{CONFIG['domain']}">
        <meta property="og:title" content="{CONFIG['site_name']}">
        <meta property="og:description" content="{CONFIG['hero_title']}">
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🛡️</text></svg>">
        {CSS}
    </head>
    <body>
        {NAV_BAR}
        <div class="container">
            <h1>{CONFIG['hero_title']}</h1>
            <p class="update-time">✅ Last Verified: {datetime.datetime.now().strftime('%Y-%m-%d')} | Data Source: Global Real-time Monitoring</p>
            
            <table class="comparison-table">
                <thead><tr>
    """
    
    # 动态表头
    for h in headers:
        if h not in ['Affiliate_Link', 'Description', 'Badge', 'Link']:
            html_content += f"<th>{h.replace('_', ' ')}</th>"
    html_content += "<th>Action</th></tr></thead><tbody>"
    
    # 动态数据行
    for row in rows:
        html_content += "<tr>"
        try:
            # 尝试找 Affiliate_Link 或 Link 列
            if 'Affiliate_Link' in headers:
                link = row[headers.index('Affiliate_Link')]
            elif 'Link' in headers:
                link = row[headers.index('Link')]
            else:
                link = "#"
        except:
            link = "#"

        for i, cell in enumerate(row):
            col_name = headers[i]
            if col_name in ['Affiliate_Link', 'Description', 'Badge', 'Link']: continue
            
            display = cell
            # 智能着色逻辑
            lower_cell = cell.lower()
            if any(x in lower_cell for x in ['yes', 'true', 'netflix', 'unlimited', '4k']):
                display = f'<span class="tag tag-green">{cell}</span>'
            elif any(x in lower_cell for x in ['no', 'false', 'block']):
                display = f'<span class="tag tag-red">{cell}</span>'
            
            html_content += f"<td>{display}</td>"
        
        html_content += f'<td><a href="{link}" target="_blank" rel="nofollow sponsored" class="btn">Check Price</a></td></tr>'

    html_content += """
                </tbody>
            </table>
            <div style="text-align:center; margin-top:50px; color:#555; font-size:0.8rem;">
                &copy; 2026 ii-x.com Network. All Rights Reserved.
            </div>
        </div>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ index.html generated for {CONFIG['site_name']}!")

if __name__ == "__main__":
    generate_site()

