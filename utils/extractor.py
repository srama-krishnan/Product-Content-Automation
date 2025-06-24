import re
from openai import OpenAI
import os
from utils.singleton_client import get_openai_client
from utils.helpers import load_prompt_template

client = get_openai_client()

def get_raw_details(PName, Brand, SKU):
    template = load_prompt_template("text_extraction_prompt.txt")
    ip = template.format(
        PName=PName,
        Brand=Brand,
        SKU=SKU
    )
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
        input=ip
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

    spec_dict = {}
    for line in technical_specifications.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip(" -:\u2022").capitalize()
            value = value.strip(" -:")
            if key and value:
                spec_dict[key] = value

    return official_description, technical_specifications, source_links, spec_dict
