import csv
import os
import datetime

# 1. 资源配置 (注意：导航栏使用绝对链接，打通三个站点)
NAV_BAR = """
<nav style="background: #1a1a1a; padding: 15px; text-align: center; border-bottom: 2px solid #333;">
    <a href="https://compare.ii-x.com" style="color: #fff; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 1.1rem;">🤖 AI Tools</a>
    <span style="color: #555;">|</span>
    <a href="https://vpn.ii-x.com" style="color: #d946ef; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 1.1rem;">🛡️ VPN Privacy</a>
    <span style="color: #555;">|</span>
    <a href="https://esim.ii-x.com" style="color: #fff; text-decoration: none; margin: 0 15px; font-weight: bold; font-size: 1.1rem;">📲 Travel eSIM</a>
</nav>
"""

CSS = """
<style>
    :root { --primary: #2563eb; --bg: #0f172a; --text: #f8fafc; --card-bg: #1e293b; }
    body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 50px; }
    .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
    h1 { text-align: center; margin: 40px 0; font-size: 2.5rem; background: linear-gradient(to right, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .update-time { text-align: center; color: #94a3b8; margin-bottom: 30px; font-size: 0.9rem; }
    .comparison-table { width: 100%; border-collapse: collapse; background: var(--card-bg); border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    th { background: #334155; color: #fff; padding: 16px; text-align: left; font-weight: 600; text-transform: uppercase; font-size: 0.85rem; }
    td { padding: 16px; border-bottom: 1px solid #334155; color: #cbd5e1; vertical-align: middle; }
    tr:hover { background: #2d3748; }
    .btn { display: inline-block; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; }
    .tag { padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }
    .tag-green { background: #064e3b; color: #34d399; }
    .tag-red { background: #450a0a; color: #fca5a5; }
</style>
"""

def generate_vpn_site():
    print("🔄 Building VPN Site...")
    # 路径指向 data/vpn_raw.csv
    file_path = os.path.join('data', 'vpn_raw.csv')
    
    # 简单的容错读取
    if not os.path.exists(file_path):
        print("❌ Data file not found!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    # 动态生成 HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Top VPN Services Compared | Privacy Shield</title>
        {CSS}
    </head>
    <body>
        {NAV_BAR}
        <div class="container">
            <h1>🛡️ The Best Log-Free VPNs (2025)</h1>
            <p class="update-time">Last Verified: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} UTC</p>
            
            <table class="comparison-table">
                <thead><tr>
    """
    
    # 生成表头 (过滤掉 Link 和 Description)
    for h in headers:
        if h not in ['Affiliate_Link', 'Description', 'Badge']:
            html_content += f"<th>{h.replace('_', ' ')}</th>"
    html_content += "<th>Action</th></tr></thead><tbody>"
    
    # 生成行
    for row in rows:
        html_content += "<tr>"
        # 假设倒数第2列是链接 (根据标准CSV结构: Provider,Price,Server,Logs,Stream,MoneyBack,Link,Badge)
        # 安全起见，我们通过查找 Affiliate_Link 的索引来定位
        try:
            link_idx = headers.index('Affiliate_Link')
            link = row[link_idx]
        except:
            link = "#"

        for i, cell in enumerate(row):
            col_name = headers[i]
            if col_name in ['Affiliate_Link', 'Description', 'Badge']: continue
            
            # 渲染 Tag
            display = cell
            if cell.lower() in ['yes', 'true', 'netflix', 'disney+']:
                display = f'<span class="tag tag-green">{cell}</span>'
            elif cell.lower() in ['no', 'false']:
                display = f'<span class="tag tag-red">{cell}</span>'
            
            html_content += f"<td>{display}</td>"
        
        html_content += f'<td><a href="{link}" target="_blank" class="btn">Check Deal</a></td></tr>'

    html_content += "</tbody></table></div></body></html>"
    
    # 核心修正：输出文件名必须是 index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ VPN index.html generated!")

if __name__ == "__main__":
    generate_vpn_site()
