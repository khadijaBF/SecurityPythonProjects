import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

class URLCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.all_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Parse the base URL to get domain and IP information
        parsed = urlparse(base_url)
        self.base_domain = parsed.netloc
        self.base_scheme = parsed.scheme or 'http'
        
    def is_valid_url(self, url):
        """
        Check if URL is valid and belongs to the same domain/IP
        """
        if not url or url.startswith('mailto:') or url.startswith('javascript:'):
            return False
            
        parsed = urlparse(url)
        
        # Handle relative URLs
        if not parsed.netloc:
            return True
            
        # Check if URL belongs to the same domain/IP
        return parsed.netloc == self.base_domain or parsed.netloc.split(':')[0] == self.base_domain.split(':')[0]
        
    def normalize_url(self, url):
        """
        Convert relative URLs to absolute and clean up the URL
        """
        if not urlparse(url).netloc:
            url = urljoin(f"{self.base_scheme}://{self.base_domain}", url)
            
        # Remove URL fragments
        url = url.split('#')[0]
        
        # Ensure consistent scheme
        if url.startswith('http://') and self.base_scheme == 'https':
            url = url.replace('http://', 'https://', 1)
            
        return url
        
    def extract_urls(self, html_content, current_url):
        """
        Extract all URLs from HTML content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = set()
        
        # Find all links
        for tag in soup.find_all(['a', 'link', 'img', 'script', 'iframe', 'form']):
            if tag.name == 'a' and tag.get('href'):
                urls.add(tag['href'])
            elif tag.name == 'link' and tag.get('href'):
                urls.add(tag['href'])
            elif tag.name == 'img' and tag.get('src'):
                urls.add(tag['src'])
            elif tag.name == 'script' and tag.get('src'):
                urls.add(tag['src'])
            elif tag.name == 'iframe' and tag.get('src'):
                urls.add(tag['src'])
            elif tag.name == 'form' and tag.get('action'):
                urls.add(tag['action'])
                
        # Find URLs in CSS and JavaScript
        for text in [tag.string for tag in soup.find_all(['style', 'script']) if tag.string]:
            urls.update(re.findall(r'url\((.*?)\)', str(text)))
            
        # Filter and normalize URLs
        filtered_urls = set()
        for url in urls:
            if self.is_valid_url(url):
                normalized = self.normalize_url(url)
                filtered_urls.add(normalized)
                
        return filtered_urls
        
    def crawl(self, url=None, depth=1, max_depth=3):
        """
        Recursive crawling function
        """
        if depth > max_depth:
            return
            
        url = url or self.base_url
        normalized_url = self.normalize_url(url)
        
        if normalized_url in self.visited_urls:
            return
            
        try:
            response = self.session.get(normalized_url, timeout=10)
            if response.status_code == 200:
                self.visited_urls.add(normalized_url)
                content_type = response.headers.get('content-type', '')
                
                if 'text/html' in content_type:
                    urls = self.extract_urls(response.text, normalized_url)
                    new_urls = urls - self.all_urls
                    self.all_urls.update(urls)
                    
                    print(f"Crawled: {normalized_url} (found {len(urls)} URLs)")
                    
                    # Recursively crawl new URLs
                    for new_url in new_urls:
                        self.crawl(new_url, depth + 1, max_depth)
                        
        except requests.RequestException as e:
            print(f"Error crawling {normalized_url}: {e}")
            
    def get_all_urls(self):
        """
        Return all found URLs
        """
        return sorted(self.all_urls)

if __name__ == "__main__":
    # Example usage
    target_url = input("Enter URL or IP address to crawl: ").strip()
    
    # Add scheme if missing
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
        
    crawler = URLCrawler(target_url)
    print(f"Starting crawl of {target_url}...")
    crawler.crawl()
    
    print("\nFound URLs:")
    for url in crawler.get_all_urls():
        print(url)
        
    print(f"\nTotal URLs found: {len(crawler.get_all_urls())}")
