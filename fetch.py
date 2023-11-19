import os
import sys
import urllib.request
from html.parser import HTMLParser
from datetime import datetime

class WebPageFetcher(HTMLParser):
    def __init__(self, urls):
        super().__init__()
        self.urls = urls

    def fetch(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode('utf-8')
        except urllib.error.URLError as e:
            print(f"Error fetching {url}: {e}")
            return None

    def save_page(self, url, content):
        file_name = f"{url.split('//')[1].replace('/', '_')}.html"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)

    def get_metadata(self, content):
        self.num_links = 0
        self.num_images = 0
        self.feed(content)
        return self.num_links, self.num_images

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.num_links += 1
        elif tag == 'img':
            self.num_images += 1

    def fetch_and_save(self):
        for url in self.urls:
            content = self.fetch(url)
            if content:
                self.save_page(url, content)
                num_links, num_images = self.get_metadata(content)
                self.print_metadata(url, num_links, num_images)

    def print_metadata(self, url, num_links, num_images):
        timestamp = datetime.utcnow().strftime('%a %b %d %Y %H:%M:%S UTC')
        print(f"site: {url}")
        print(f"num_links: {num_links}")
        print(f"images: {num_images}")
        print(f"last_fetch: {timestamp}")
        print("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch.py <url1> <url2> ...")
        sys.exit(1)

    urls = sys.argv[1:]
    fetcher = WebPageFetcher(urls)
    fetcher.fetch_and_save()
