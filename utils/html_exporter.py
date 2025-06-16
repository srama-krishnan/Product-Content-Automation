# utils/html_exporter.py

def export_images_to_html(image_urls, filename="images_preview.html", images_per_row=5):
    html = """
    <html>
    <head><title>Product Images Preview</title></head>
    <body>
    <h2>🖼️ Product Images Preview</h2>
    <div style='display: flex; flex-wrap: wrap;'>
    """

    for img_url in image_urls:
        html += f"""
        <div style='flex: 1 0 {100/images_per_row}%; padding: 10px; box-sizing: border-box; text-align: center;'>
            <img src="{img_url}" style="width: 100%; max-width: 250px; height: auto; border: 1px solid #ccc; border-radius: 8px;" />
        </div>
        """

    html += "</div></body></html>"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Image preview exported → {filename}")
