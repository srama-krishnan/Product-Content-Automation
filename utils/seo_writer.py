import re
from openai import OpenAI
from dotenv import dotenv_values
import unicodedata
from utils.helpers import slugify_url
from utils.helpers import load_prompt_template

config = dotenv_values(".env")
client = OpenAI(api_key=config["APIKEY"])

def generate_multilang_descriptions(official_description, temperature=0.7, top_p=1.0, max_tokens=800, tone="Write professionally and highlight key features.", short_limit=25, long_limit=200, extra_keywords=None):

    keyword_hint = ", ".join(extra_keywords) if extra_keywords else "none"
    template = load_prompt_template("seo_prompt.txt")
    system_prompt = template.format(
        short_limit=short_limit,
        long_limit=long_limit,
        tone=tone,
        keyword_hint=keyword_hint
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": official_description}
        ]
    )

    content = response.choices[0].message.content

    try:
        en_short = re.search(r'\[EN_SHORT\](.*?)\[EN_LONG\]', content, re.DOTALL).group(1).strip()
        en_long = re.search(r'\[EN_LONG\](.*?)\[IS_SHORT\]', content, re.DOTALL).group(1).strip()
        is_short = re.search(r'\[IS_SHORT\](.*?)\[IS_LONG\]', content, re.DOTALL).group(1).strip()
        is_long = re.search(r'\[IS_LONG\](.*?)\[KEYWORDS\]', content, re.DOTALL).group(1).strip()
        keywords = re.search(r'\[KEYWORDS\](.*)', content, re.DOTALL).group(1).strip().split(",")
        keywords = [k.strip().lower() for k in keywords if k.strip()]
        if extra_keywords:
            keywords = list(set(keywords + [k.lower() for k in extra_keywords]))
    except:
        en_short = en_long = is_short = is_long = ""
        keywords = []

    return en_short, en_long, is_short, is_long, keywords



def generate_image_search_links(product, brand, sku, desc, specs):
    product_name = re.sub(r"\(.*?\)", "", product).strip()
    english_product = unicodedata.normalize('NFKD', product_name).encode('ascii', 'ignore').decode('ascii')
    slug = slugify_url(english_product)
    guessed_link = f"https://ht.is/{slug}.html"
    template = load_prompt_template("image_links_prompt.txt")
    prompt = template.format(
        product=product,
        brand=brand,
        sku=sku,
        slug=slug
    )
    
    # prompt = f"""
    # Search the Web eaxctly for: "{product} {sku}" and return the first three links that is been retrieved exactly as it is, do not shorten or do something with the URL. Just search and provide the three URLS."""

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a smart assistant returning only web page links of the specified product."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_response = response.choices[0].message.content.strip()
    #print(f"\n🧠 GPT Response for URLs:\n{raw_response}")

    urls = re.findall(r'https?://[^\s]+', raw_response)
    if guessed_link not in urls:
        urls.insert(0, guessed_link)
    print(f"Final URL list: {urls}")
    return urls
