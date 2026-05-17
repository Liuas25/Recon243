import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from rich.console import Console
import re

console = Console()

class WebCrawler:
    def __init__(self, target: str, recursive=False, stealth=False, threads=50):
        self.target = target
        self.recursive = recursive
        self.stealth = stealth
        self.threads = threads
        self.visited = set()
        self.urls = []
        self.js_files = []
        self.params = set()
    
    async def fetch(self, session, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            async with session.get(url, headers=headers, timeout=10) as resp:
                return await resp.text()
        except:
            return ""
    
    async def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            if self.is_same_domain(full_url):
                self.urls.append(full_url)
        for script in soup.find_all('script', src=True):
            js_url = urljoin(base_url, script['src'])
            if js_url.endswith('.js'):
                self.js_files.append(js_url)
        param_pattern = r'[\?&]([^=]+)='
        matches = re.findall(param_pattern, html)
        self.params.update(matches)
    
    def is_same_domain(self, url):
        parsed = urlparse(url)
        target_parsed = urlparse(self.target)
        return parsed.netloc == target_parsed.netloc
    
    async def crawl_url(self, session, url):
        if url in self.visited:
            return
        self.visited.add(url)
        html = await self.fetch(session, url)
        if html:
            await self.extract_links(html, url)
    
    async def crawl(self):
        console.print("🕷️ Starting web crawler...")
        connector = aiohttp.TCPConnector(limit=self.threads)
        timeout = aiohttp.ClientTimeout(total=30)
        semaphore = asyncio.Semaphore(10 if self.stealth else self.threads)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            await self.crawl_url(session, self.target)
            queue = list(set(self.urls[:100]))
            while queue and (not self.stealth or len(self.visited) < 50):
                batch = queue[:20]
                queue = queue[20:]
                tasks = [self.crawl_url(session, url) for url in batch if url not in self.visited]
                if tasks:
                    await asyncio.gather(*tasks)
        return {
            "urls": list(set(self.urls)),
            "js_files": list(set(self.js_files)),
            "parameters": list(self.params),
            "total_endpoints": len(set(self.urls))
        }
