import os
import csv
from utils.extractor import get_raw_details, clean_raw_text, parse_raw_details
from utils.seo_writer import generate_seo_descriptions
from utils.image_scraper import extract_images_from_all_urls
from utils.html_exporter import export_images_to_html
from utils.helpers import normalize_input

os.makedirs("output", exist_ok=True)
summary_rows = []

mode = input("Run Mode - Enter '1' for Single Product Input or '2' for CSV Batch Mode: ").strip()

def process_product(product, brand, sku):
    print(f"\n🔍 Processing: {product} ({sku})")
    try:
        raw = get_raw_details(product, brand, sku)
        cleaned = clean_raw_text(raw)
        desc, specs, urls = parse_raw_details(cleaned)
        short, long, keywords = generate_seo_descriptions(desc)
        print(f"✅ SEO descriptions generated for {product}")
        images = extract_images_from_all_urls(urls, keywords, global_limit=20)
        print(f"✅ Images collected: {len(images)}")
        html_filename = f"output/{product.replace(' ', '_')}.html"
        export_images_to_html(images, filename=html_filename, images_per_row=4)
        summary_rows.append({
            "Product Name": product,
            "Short Description": short,
            "Long Description": long,
            "Keywords": ', '.join(keywords),
            "Image File Path": html_filename
        })
    except Exception as e:
        print(f"❌ Failed for {product}: {e}")

if mode == '1':
    product = normalize_input(input("Enter Product Name: "))
    brand = normalize_input(input("Enter Brand: "))
    sku = normalize_input(input("Enter SKU: "))
    process_product(product, brand, sku)

elif mode == '2':
    with open("Product_info.csv", mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = normalize_input(row["Product Name"])
            brand = normalize_input(row["Brand"])
            sku = normalize_input(row["SKU"])
            process_product(product, brand, sku)

else:
    print("Invalid mode selected. Exiting.")
    exit()

with open("output/Product_Summary.csv", mode="w", newline='', encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["Product Name", "Short Description", "Long Description", "Keywords", "Image File Path"])
    writer.writeheader()
    writer.writerows(summary_rows)

print("\n📄 Summary CSV saved as: output/Product_Summary.csv")
