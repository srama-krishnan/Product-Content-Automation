import os
import json
from datetime import datetime
from utils.helpers import normalize_input, slugify_url
from utils.extractor import get_raw_details, clean_raw_text, parse_raw_details
from utils.seo_writer import generate_multilang_descriptions, generate_image_search_links
from utils.image_scraper import extract_images_from_all_urls
from utils.html_exporter import export_images_to_html

os.makedirs("output", exist_ok=True)
os.makedirs("output/json", exist_ok=True)

def get_config():
    tone = input("Tone (default: Professional, highlight features): ").strip() or "Write professionally and highlight key features."
    temperature = float(input("Temperature (default: 0.7): ").strip() or 0.7)
    top_p = float(input("Top-p (default: 1.0): ").strip() or 1.0)
    max_tokens = int(input("Max Tokens (default: 800): ").strip() or 700)
    short_limit = int(input("Word limit for Short Description (default: 25): ").strip() or 25)
    long_limit = int(input("Word limit for Long Description (default: 200): ").strip() or 200)
    extra_keywords = input("Optional Keywords (comma separated): ").strip()
    extra_keywords = [k.strip() for k in extra_keywords.split(",") if k.strip()] if extra_keywords else []
    return {
        "tone": tone,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "short_limit": short_limit,
        "long_limit": long_limit,
        "extra_keywords": extra_keywords
    }

def save_json(data, sku):
    json_path = f"output/json/{sku}.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(data, jf, indent=4, ensure_ascii=False)

def process_product(product, brand, sku, config):
    print(f"\n🔍 Processing: {product} ({sku})")
    try:
        raw = get_raw_details(product, brand, sku)
        cleaned = clean_raw_text(raw)
        desc, specs, urls, spec_dict = parse_raw_details(cleaned)

        en_short, en_long, is_short, is_long, keywords = generate_multilang_descriptions(
            desc,
            temperature=config["temperature"],
            top_p=config["top_p"],
            max_tokens=config["max_tokens"],
            tone=config["tone"],
            short_limit=config["short_limit"],
            long_limit=config["long_limit"],
            extra_keywords=config["extra_keywords"]
        )

        image_search_urls = generate_image_search_links(product, brand, sku, en_long, spec_dict)
        images = extract_images_from_all_urls(image_search_urls, keywords)

        html_filename = f"output/{product.replace(' ', '_')}.html"
        export_images_to_html(images, filename=html_filename, images_per_row=4)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_data = {
            "product_name": product,
            "brand": brand,
            "sku": sku,
            "short_description_en": en_short,
            "long_description_en": en_long,
            "short_description_is": is_short,
            "long_description_is": is_long,
            "keywords": keywords,
            "technical_specifications": spec_dict,
            "image_file_path": html_filename,
            "image_urls": images,
            "generated_at": now
        }

        save_json(json_data, sku)

        print("\n📦 OUTPUT:")
        for k, v in json_data.items():
            if k != "image_urls":
                print(f"{k}: {v}")
        print(f"📝 JSON saved to: output/json/{sku}.json")

    except Exception as e:
        print(f"❌ Failed for {product}: {e}")

# ---- Main Entry ----
product = normalize_input(input("Enter Product Name: "))
brand = normalize_input(input("Enter Brand: "))
sku = normalize_input(input("Enter SKU: "))
config = get_config()

process_product(product, brand, sku, config)
