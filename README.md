# Product Content Automation

A modular Python automation tool that generates SEO-optimized content and visual previews for international products — including those with Icelandic names. Given a product name, it extracts raw product data, generates descriptions, and scrapes relevant images to produce a simple HTML preview for each product.

---

## Features

- 🛍️ **Supports Icelandic product names**
- 🧠 **Generates short and long SEO descriptions** using keyword-enhanced templates
- 🌐 **Scrapes 20 relevant product images** from trusted sources
- 📄 **Exports preview HTML pages** for visual inspection or catalog generation
- 🗃️ **CSV input support** for bulk product processing
- 📦 Modular structure with reusable components

---

## 📂 Folder Structure

```
HT_CONTENT_GEN_PROJECT/
├── output/                   # Generated HTML files (1 per product)
│   ├── Aqara_Pro_Öryggismyndavél_með_brú_Grá_(Ethernet).html
│   └── images_preview.html
├── utils/                    # All functional Python modules
│   ├── extractor.py          # Extracts and cleans raw product data
│   ├── seo_writer.py         # Generates short and long SEO descriptions
│   ├── image_scraper.py      # Web scraping logic for images
│   ├── html_exporter.py      # Converts results into previewable HTML pages
│   ├── helpers.py            # Utility functions
│   └── __init__.py
├── Product_info.csv          # Input file containing product names
├── main.py                   # Pipeline execution script
├── requirements.txt          # List of dependencies
├── .gitignore
└── README.md
```

---

### 💡 Use Cases
- Auto-generating content for product listings in e-commerce websites
- Visual merchandising
- Data preparation for catalogues in regional markets like Iceland
- B2B data integration and enrichment

---

## Sample Output (Preview)

### 📌 Product:
**Aqara Pro Öryggismyndavél með brú Grá (Ethernet)**

### 📝 Short Description:
> Enhance home security with the Aqara G5 Pro camera featuring AI analysis, Zigbee hub, and 4MP resolution for indoor and outdoor use.

### 📖 Long Description:
> The Aqara G5 Pro is a top-tier security camera designed to seamlessly integrate into your smart home while providing exceptional protection for your property. This versatile camera is suitable for both indoor and outdoor installations, ensuring comprehensive coverage with its wide 133° field of view and superior 4MP resolution (2688x1520). Engineered to deliver unmatched image quality, the G5 Pro utilizes advanced night vision with True Full-Color technology, allowing it to capture vivid color images even in low-light environments, enhancing your surveillance capabilities around the clock.

> One of the standout features of the Aqara G5 Pro is its smart home integration capabilities. Equipped with a built-in Zigbee hub, Matter Controller, and Thread Border Router, it effortlessly connects with popular ecosystems like HomeKit Secure Video, Google Home, and Amazon Alexa, offering you flexible control and access to your security system. The camera's PoE version ensures robust end-to-end encryption, safeguarding your data against unauthorized access.

> Moreover, the Aqara G5 Pro is designed to withstand harsh weather conditions, operating effectively in temperatures ranging from -30°C to 50°C. Its built-in 32GB eMMC storage allows for reliable local storage, while also supporting connections to NAS boxes and RTSP streaming for broader storage and accessibility options. Whether you’re upgrading your security system or integrating with an existing setup, the Aqara G5 Pro is the ideal choice for a smart, secure, and connected home.

### 🖼️ Image Sample Preview
![Screenshot 2025-06-15 184402](https://github.com/user-attachments/assets/dc4707c4-1195-4d4c-8c29-11ec350e098a)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/srama-krishnan/Product-Content-Automation.git
cd Product-Content-Automation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the tool
```bash
python main.py
```
You can edit Product_info.csv with your own product names for batch processing.


### 🤝 Contributing
Pull requests and suggestions are welcome. For major changes, please open an issue first to discuss what you would like to change.
