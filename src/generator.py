import csv
import os
import json
import datetime

# ===========================
# 1. 强壮的配置读取
# ===========================
def load_config():
    config = {
        "site_name": "Comparison Site",
        "domain": "https://ii-x.com",
        "niche_keywords": "Review",
        "hero_title": "Best Tools Compared",
        "primary_color": "#2563eb",
        "data_file": "data.csv"
    }
    
    # 尝试读取 config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                config.update(loaded)
        except Exception as e:
            print(f"⚠️ Config JSON Syntax Error (Fix config.json!): {e}")
            # 如果配置错了，这里做一个智能回退，根据文件名猜测业务
            if os.path.exists(os.path.join('data', 'vpn_raw.csv')):
                config['data_file'] = 'vpn_raw.csv'
                config['site_name'] = 'VPN Privacy Shield'
            elif os.path.exists(os.path.join('data', 'esim_raw.csv')):
                config['data_file'] = 'esim_raw.csv'
                config['site_name'] = 'Global eSIM'
    
    return config

CONFIG = load_config()

# ===========================
# 2. 样式与导航
# ===========================
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

# ===========================
# 3. 核心生成逻辑 (含防爆盾)
# ===========================
def generate_site():
    print(f"🔄 Building Site: {CONFIG['site_name']}...")
    file_path = os.path.join('data', CONFIG.get('data_file', 'data.csv'))
    
    if not os.path.exists(file_path):
        print(f"❌ Critical: Data file {file_path} NOT found.")
        # 创建一个假的 index.html 防止 404
        with open('index.html', 'w') as f: f.write("<h1>Data Pending...</h1>")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
            # 清理表头空白
            headers = [h.strip() for h in headers]
            rows = list(reader)
        except StopIteration:
            print("❌ CSV is empty.")
            return

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{CONFIG['site_name']}</title>
        <meta name="description" content="{CONFIG['hero_title']}">
        {CSS}
    </head>
    <body>
        {NAV_BAR}
        <div class="container">
            <h1>{CONFIG['hero_title']}</h1>
            <p class="update-time">✅ Verified: {datetime.datetime.now().strftime('%Y-%m-%d')} | Source: {CONFIG['data_file']}</p>
            
            <table class="comparison-table">
                <thead><tr>
    """
    
    # 动态表头 (排除不展示的列)
    hidden_cols = ['Affiliate_Link', 'Description', 'Badge', 'Link']
    display_headers = []
    for h in headers:
        if h not in hidden_cols:
            display_headers.append(h)
            html_content += f"<th>{h.replace('_', ' ')}</th>"
    html_content += "<th>Action</th></tr></thead><tbody>"
    
    # 动态数据行 (防崩溃核心逻辑)
    for row_idx, row in enumerate(rows):
        # 跳过空行
        if not row: continue

        html_content += "<tr>"
        
        # 1. 安全提取链接
        link = "#"
        if 'Affiliate_Link' in headers:
            # 安全索引，防止找不到
            try:
                idx = headers.index('Affiliate_Link')
                if idx < len(row): link = row[idx]
            except: pass
        
        # 2. 填充单元格 (防崩溃循环)
        # 我们只遍历表头，确保不会因为数据列多了而越界
        for col_idx, col_name in enumerate(headers):
            # 如果这一列是不需要显示的，跳过
            if col_name in hidden_cols: continue
            
            # 【核心修复】：防止 list index out of range
            # 如果数据列比表头短，填空；如果长，忽略多余的
            if col_idx < len(row):
                cell = row[col_idx]
            else:
                cell = "" 

            # 样式处理
            display = cell
            lower_cell = str(cell).lower()
            if any(x in lower_cell for x in ['yes', 'true', 'netflix', 'unlimited', '4k']):
                display = f'<span class="tag tag-green">{cell}</span>'
            elif any(x in lower_cell for x in ['no', 'false', 'block']):
                display = f'<span class="tag tag-red">{cell}</span>'
            
            html_content += f"<td>{display}</td>"
        
        html_content += f'<td><a href="{link}" target="_blank" class="btn">Check Price</a></td></tr>'

    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ index.html generated successfully!")

if __name__ == "__main__":
    generate_site()
