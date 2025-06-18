from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("APIKEY"))

def generate_image_source_links_with_openai(product_name, brand, sku, description):
    # Convert Icelandic to English first
    translation_prompt = f"""Translate this Icelandic product name to English:
    '{product_name}'
    Only respond with the translated English phrase. No quotes or extra text."""

    translation_resp = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a translator for Icelandic to English"},
            {"role": "user", "content": translation_prompt}
        ]
    )

    english_product_name = translation_resp.choices[0].message.content.strip()

    # Then perform search using English name
    search_prompt = f"""
You are a product researcher. Your task is to find accurate product page URLs where the product is actually sold and where images are present.

Translated Product Name: {english_product_name}
Brand: {brand}
SKU: {sku}
Description: {description}

Find 3 to 5 direct product page URLs from trusted e-commerce websites like:
- https://www.amazon.com
- https://www.ebay.com
- https://www.walmart.com
- the brand's official site (e.g., samsung.com)

Requirements:
- Only return working product pages (not category pages, not broken links).
- Do NOT include any extra text or markdown, just one URL per line.
- Start output directly with URLs.

Important: Output must be raw links, nothing else.
"""

    search_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert web assistant that returns accurate product page links only."},
            {"role": "user", "content": search_prompt}
        ],
        temperature=0.2
    )

    urls = search_response.choices[0].message.content.strip().splitlines()
    urls = [u.strip() for u in urls if u.strip().startswith("http")]
    return list(dict.fromkeys(urls))
