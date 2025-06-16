import re
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("APIKEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_raw_details(PName, Brand, SKU):
    response = client.responses.create(
        model="gpt-4.1",
        tools=[{
            "type": "web_search_preview",
            "user_location": {
                "type": "approximate",
                "country": "IS",
                "city": "Reykjavik",
                "region": "Capital Region"
            },
            "search_context_size": "medium" 
        }],
        input=f"""
You are a product data retriever for an Iceland-based e-commerce website (ht.is).
Your job is to collect raw factual data from the web about the following product (There can be similar products with the name, be specific only to the product with SKU that is mentioned). 
This includes official product descriptions in more than 150 words and complete technical specifications. Do not summarize. Align and beautify the content (but don't include any markdown symbols or asteriks while returning the result.
Product Name: {PName}
Brand: {Brand}
SKU: {SKU}

Search through:
1. The official website of the manufacturer to retrieve the full official description and all technical specifications.
2. At least 2-3 reputable e-commerce or review websites (e.g., Amazon, Best Buy, TechRadar, Trusted Reviews, etc.) to cross-check and supplement with additional verified technical data.
3. If Iceland-specific domains are not found, general international websites are acceptable.

Ensure your response contains:

Official Description: (at the beginning)
(verbatim from the official manufacturer website) '
(if it is less than 100 words, you can browse other reputed sites with this product and include their content too)
(Include a Tag line about the product or of the brand, whichever is more suitable)
[Do not use markdown or formatting symbols like * or **]

Technical Specifications:
(full list, as complete as possible in the below format):
- Aspect: Details

Source Links:
Please provide clickable links for:
- Official Manufacturer Page (with exact match)
- 4 reputable third-party sites (with brief title or site name)

Output Rules:
- Do NOT summarize any data.
- Do NOT include formatting characters like **, *, _, or >.
- Keep raw text clean and structured.
- Do NOT add SEO output or marketing language.
- Ensure the product matches exactly with the SKU and product name.

"""

    )
    return response.output_text

def clean_raw_text(raw_text):
    return re.sub(r'[\*_>`]', '', raw_text)

def parse_raw_details(raw_text):
    try:
        official_description = re.search(
            r'Official Description\s*(.*?)\s*Technical Specifications',
            raw_text,
            re.DOTALL
        ).group(1).strip()
    except:
        official_description = ""

    try:
        technical_specifications = re.search(
            r'Technical Specifications\s*(.*?)\s*Source Links',
            raw_text,
            re.DOTALL
        ).group(1).strip()
    except:
        technical_specifications = ""

    try:
        source_links = re.findall(r'https?://[^\)\s]+', raw_text)
    except:
        source_links = []

    return official_description, technical_specifications, source_links
