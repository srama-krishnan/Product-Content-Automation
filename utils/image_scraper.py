import re
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import dotenv_values
from utils.helpers import slugify_url
from urllib.parse import urljoin

config = dotenv_values(".env")
client = OpenAI(api_key=config["APIKEY"])

def generate_source_links_prompt(product_name, brand, sku):
    return f"""
Given the following product details, return 3 to 5 direct URLs to official product pages or trusted retailer listings that show clear product images.

Only return URLs that:
- Lead directly to a product detail page (not a search, category, or homepage)
- Are valid and accessible
- Contain relevant images for scraping

Product Name: {product_name}
Brand: {brand}
SKU: {sku}

Respond only with plain links separated by newlines.
"""

def get_valid_product_links(product_name, brand, sku, max_links=5):
    prompt = generate_source_links_prompt(product_name, brand, sku)
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a product research agent returning valid product detail links."},
            {"role": "user", "content": prompt},
        ]
    )
    raw_links = response.choices[0].message.content.strip().splitlines()
    valid_links = []

    for url in raw_links:
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200 and (sku.lower() in r.text.lower() or brand.lower() in r.text.lower() or product_name.lower().split()[0] in r.text.lower()):
                valid_links.append(url)
            if len(valid_links) >= max_links:
                break
        except Exception:
            continue
    return valid_links

def extract_images_from_all_urls(urls, keywords=None, global_limit=20):
    all_images = []

    print(f"\n🔍 Processing: {urls}")

    # Filters
    block_if_contains = ["facebook.com/tr", "datocms-assets.com", "logo", "sprite", "icon", "tracking"]
    allowed_ext = (".jpg", ".jpeg", ".png", ".webp")

    for url in urls:
        print(f"🔎 Scanning {url}")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code != 200:
                continue
            soup = BeautifulSoup(res.text, 'html.parser')
            imgs = soup.find_all('img')
            found = 0

            for tag in imgs:
                src = (
                    tag.get('src') or
                    tag.get('data-src') or
                    tag.get('data-original') or
                    tag.get('data-lazy') or
                    tag.get('data-srcset')
                )
                if not src:
                    continue
                src = src.strip()
                src = urljoin(url, src)  # Handle relative URLs
                if not src.lower().endswith(allowed_ext):
                    continue
                if any(bad in src.lower() for bad in block_if_contains):
                    continue
                if len(src) < 10:
                    continue

                all_images.append(src)
                found += 1
                if len(all_images) >= global_limit:
                    break

            print(f"✅ Found {found} images from {url}")

        except Exception as e:
            print(f"❌ Error fetching from {url}: {e}")
            continue

        if len(all_images) >= global_limit:
            break

    return all_images[:global_limit]