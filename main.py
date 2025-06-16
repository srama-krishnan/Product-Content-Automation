import os
import csv
from utils.extractor import get_raw_details, clean_raw_text, parse_raw_details
from utils.seo_writer import generate_multilang_descriptions
from utils.image_scraper import extract_images_from_all_urls
from utils.html_exporter import export_images_to_html
from utils.helpers import normalize_input

os.makedirs("output", exist_ok=True)
summary_rows = []

mode = input("Run Mode - Enter '1' for Single Product Input or '2' for CSV Batch Mode: ").strip()

def get_config():
    tone = input("Tone (default: Professional, highlight features): ").strip() or "Write professionally and highlight key features."
    temperature = float(input("Temperature (default: 0.7): ").strip() or 0.7)
    top_p = float(input("Top-p (default: 1.0): ").strip() or 1.0)
    max_tokens = int(input("Max Tokens (default: 700): ").strip() or 700)
    short_limit = int(input("Word limit for Short Description (default: 25): ").strip() or 25)
    long_limit = int(input("Word limit for Long Description (default: 200): ").strip() or 200)
    extra_keywords = input("Optional Keywords (comma separated): ").strip()
    extra_keywords = [k.strip() for k in extra_keywords.split(",") if k.strip()] if extra_keywords else []
    return tone, temperature, top_p, max_tokens, short_limit, long_limit, extra_keywords

def process_product(product, brand, sku, config):
    print(f"\n🔍 Processing: {product} ({sku})")
    try:
        raw = get_raw_details(product, brand, sku)
        cleaned = clean_raw_text(raw)
        desc, specs, urls = parse_raw_details(cleaned)

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

        images = extract_images_from_all_urls(urls, keywords, global_limit=20)
        html_filename = f"output/{product.replace(' ', '_')}.html"
        export_images_to_html(images, filename=html_filename, images_per_row=4)

        output = {
            "Product Name": product,
            "Short Description (EN)": en_short,
            "Long Description (EN)": en_long,
            "Short Description (IS)": is_short,
            "Long Description (IS)": is_long,
            "Keywords": ', '.join(keywords),
            "Image File Path": html_filename
        }

        if mode == '2':
            summary_rows.append(output)
        else:
            print("\n📦 OUTPUT:")
            for k, v in output.items():
                print(f"{k}: {v}")

    except Exception as e:
        print(f"❌ Failed for {product}: {e}")

if mode == '1':
    product = normalize_input(input("Enter Product Name: "))
    brand = normalize_input(input("Enter Brand: "))
    sku = normalize_input(input("Enter SKU: "))

    tone, temperature, top_p, max_tokens, short_limit, long_limit, extra_keywords = get_config()
    config = {
        "tone": tone,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "short_limit": short_limit,
        "long_limit": long_limit,
        "extra_keywords": extra_keywords
    }

    process_product(product, brand, sku, config)

elif mode == '2':
    tone, temperature, top_p, max_tokens, short_limit, long_limit, extra_keywords = get_config()
    config = {
        "tone": tone,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "short_limit": short_limit,
        "long_limit": long_limit,
        "extra_keywords": extra_keywords
    }

    with open("Product_info.csv", mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = normalize_input(row["Product Name"])
            brand = normalize_input(row["Brand"])
            sku = normalize_input(row["SKU"])
            process_product(product, brand, sku, config)

    with open("output/Product_Summary.csv", mode="w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Product Name",
            "Short Description (EN)",
            "Long Description (EN)",
            "Short Description (IS)",
            "Long Description (IS)",
            "Keywords",
            "Image File Path"
        ])
        writer.writeheader()
        writer.writerows(summary_rows)

    print("\n📄 Summary CSV saved as: output/Product_Summary.csv")

else:
    print("Invalid mode selected. Exiting.")
