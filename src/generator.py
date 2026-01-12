import os
import pandas as pd
import json
from jinja2 import Environment, FileSystemLoader
import datetime
import shutil

# Tiandao VPN Generator v2.0 (Ported from Compare v8.0)
class SiteGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, 'data', 'vpn_raw.csv') # 注意文件名
        self.config_path = os.path.join(self.base_dir, 'config.json')
        self.template_dir = os.path.join(self.base_dir, 'templates')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.static_dir = os.path.join(self.base_dir, 'static')
        self.generated_urls = []
        
        # 加载配置
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {}

    def load_data(self):
        print(f"📂 Loading VPN data...")
        if not os.path.exists(self.data_path):
            print("❌ Data file missing!")
            return []
        try:
            # 适配 VPN CSV 格式
            df = pd.read_csv(self.data_path, header=0, on_bad_lines='skip', encoding='utf-8')
            df = df.fillna("Pending")
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ CSV Error: {e}")
            return []

    # 核心：佣金拦截器 (复用 Compare 逻辑)
    def get_affiliate_link(self, provider_name, original_link):
        if not self.config or 'affiliate_map' not in self.config:
            return original_link
        clean_name = str(provider_name).strip()
        for key, link in self.config.get('affiliate_map', {}).items():
            if key.lower() in clean_name.lower() and link: # 只有link不为空才替换
                return link
        return original_link

    def generate_review_pages(self, vpns):
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('review.html') # 需要新建这个模板

        print(f"📝 Generating {len(vpns)} review pages...")
        for vpn in vpns:
            # 替换链接
            vpn['Affiliate_Link'] = self.get_affiliate_link(vpn.get('Provider'), vpn.get('Affiliate_Link', '#'))
            
            # 生成 Slug
            name = str(vpn.get('Provider', 'unknown')).strip()
            slug = f"{name.lower().replace(' ', '-')}-review"
            filename = f"{slug}.html"
            
            # 渲染
            html = template.render(
                vpn=vpn,
                config=self.config,
                date=datetime.datetime.now().strftime("%B %Y")
            )
            
            with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(html)
            self.generated_urls.append(filename)

    def generate_index(self, vpns):
        print("🏆 Generating Ranking Index...")
        env = Environment(loader=FileSystemLoader(self.template_dir))
        template = env.get_template('index.html')
        
        # 处理链接
        for vpn in vpns:
            vpn['Affiliate_Link'] = self.get_affiliate_link(vpn.get('Provider'), vpn.get('Affiliate_Link', '#'))

        html = template.render(
            vpns=vpns,
            config=self.config,
            date=datetime.datetime.now().strftime("%B %Y")
        )
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)

    def generate_sitemap(self):
        print("🗺️ Generating Sitemap...")
        base_url = self.config.get('site_domain', 'https://vpn.ii-x.com')
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += f'<url><loc>{base_url}/</loc><priority>1.0</priority></url>\n'
        for url in self.generated_urls:
            xml += f'<url><loc>{base_url}/{url}</loc><priority>0.8</priority></url>\n'
        xml += '</urlset>'
        with open(os.path.join(self.output_dir, "sitemap.xml"), 'w', encoding='utf-8') as f:
            f.write(xml)

    def copy_assets(self):
        # 简单复制
        if os.path.exists(self.static_dir):
            target = os.path.join(self.output_dir, 'static')
            if os.path.exists(target): shutil.rmtree(target)
            shutil.copytree(self.static_dir, target)
        # 生成 robots.txt
        with open(os.path.join(self.output_dir, "robots.txt"), 'w') as f:
            f.write("User-agent: *\nAllow: /")

    def run(self):
        if os.path.exists(self.output_dir): shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        
        vpns = self.load_data()
        if not vpns: return
            
        self.generate_review_pages(vpns)
        self.generate_index(vpns)
        self.generate_sitemap()
        self.copy_assets()
        print("✅ VPN Build Complete.")

if __name__ == "__main__":
    generator = SiteGenerator()
    generator.run()
