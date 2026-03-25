"""
Pasta Image Scraper for Food Detection Project
Collects images of various pasta types into a single 'pasta' class folder
"""

import os
import requests
import time
import hashlib
from pathlib import Path
import json
import re

class PastaScraper:
    def __init__(self, output_dir="pasta_dataset"):
        self.output_dir = Path(output_dir)
        # All images go into a single 'pasta' folder → one class
        self.pasta_folder = self.output_dir / "pasta"
        self.pasta_folder.mkdir(parents=True, exist_ok=True)

        # Different pasta types used as search queries
        # All saved under the same 'pasta' label
        self.search_queries = [
            "spaghetti pasta dish",
            "penne pasta dish",
            "fusilli pasta dish",
            "farfalle pasta dish",
            "rigatoni pasta dish",
            "fettuccine pasta dish",
            "tagliatelle pasta dish",
            "lasagna pasta dish",
            "ravioli pasta dish",
            "tortellini pasta dish",
            "gnocchi pasta dish",
            "linguine pasta dish",
        ]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Track downloaded images to avoid duplicates
        self.downloaded_hashes = set()
        self.total_downloaded = 0

    def get_image_hash(self, image_data):
        """Generate hash to detect duplicate images"""
        return hashlib.md5(image_data).hexdigest()

    def download_image(self, url, index):
        """Download a single image into the pasta folder"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            if 'image' not in content_type:
                return False

            # Skip duplicates
            img_hash = self.get_image_hash(response.content)
            if img_hash in self.downloaded_hashes:
                return False

            # Determine extension
            ext = '.png' if 'png' in content_type else '.jpg'

            filepath = self.pasta_folder / f"pasta_{index:04d}{ext}"
            with open(filepath, 'wb') as f:
                f.write(response.content)

            self.downloaded_hashes.add(img_hash)
            self.total_downloaded += 1
            return True

        except Exception as e:
            return False

    def scrape_bing(self, query, max_images=25):
        """Scrape Bing Images for a given query"""
        print(f"  Scraping: '{query}'...")

        search_url = "https://www.bing.com/images/search"
        downloaded = 0
        offset = 0

        while downloaded < max_images:
            params = {
                'q': query,
                'first': offset,
                'count': 35
            }

            try:
                response = requests.get(
                    search_url, params=params,
                    headers=self.headers, timeout=10
                )
                img_urls = re.findall(r'murl&quot;:&quot;(.*?)&quot;', response.text)

                if not img_urls:
                    break

                for img_url in img_urls:
                    if downloaded >= max_images:
                        break
                    img_url = img_url.replace('\\/', '/')
                    if self.download_image(img_url, self.total_downloaded):
                        downloaded += 1
                    time.sleep(0.3)

                offset += 35
                time.sleep(1)

            except Exception as e:
                print(f"  Error: {e}")
                break

        print(f"  → {downloaded} images downloaded")
        return downloaded

    def scrape_all(self, images_per_query=25):
        """Scrape all pasta types into the single pasta folder"""
        print("=" * 60)
        print("PASTA IMAGE SCRAPER — Single Class Mode")
        print("=" * 60)
        print(f"Target : {images_per_query} images per query")
        print(f"Queries: {len(self.search_queries)}")
        print(f"Output : {self.pasta_folder.absolute()}")
        print(f"Expected total: ~{images_per_query * len(self.search_queries)} images")
        print("=" * 60)

        for query in self.search_queries:
            self.scrape_bing(query, images_per_query)
            time.sleep(2)

        self.save_stats()
        self.print_summary()

    def save_stats(self):
        stats = {
            "total_images": self.total_downloaded,
            "output_folder": str(self.pasta_folder.absolute()),
            "queries_used": self.search_queries
        }
        with open(self.output_dir / "stats.json", 'w') as f:
            json.dump(stats, f, indent=2)

    def print_summary(self):
        print("\n" + "=" * 60)
        print("SCRAPING COMPLETE")
        print("=" * 60)
        print(f"\nTotal images collected : {self.total_downloaded}")
        print(f"Saved in              : {self.pasta_folder.absolute()}")


if __name__ == "__main__":
    scraper = PastaScraper(output_dir="pasta_dataset")
    scraper.scrape_all(images_per_query=25)