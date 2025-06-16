import re
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")
client = OpenAI(api_key=config["APIKEY"])

def generate_multilang_descriptions(official_description, temperature=0.7, tone_instruction="Write professionally and highlight key features."):

    system_prompt = f"""
You are an expert SEO copywriter generating compelling product descriptions for an Iceland-based e-commerce website (ht.is).

Steps:
1. Read the official product description.
2. Generate a SHORT description (15–30 words) in English with a tagline.
3. Generate a LONG description (100–230 words) in English, keyword-rich, engaging.
4. Then translate both descriptions to Icelandic.
5. Extract 5 English keywords.
6. Follow tone/style: "{tone_instruction}"
7. Use only given facts—no invention. Avoid markdown symbols.

Respond in this format:

[EN_SHORT]
<Short description with tagline in English>

[EN_LONG]
<Long description in English>

[IS_SHORT]
<Icelandic short description with tagline>

[IS_LONG]
<Icelandic long description>

[KEYWORDS]
keyword1, keyword2, keyword3, keyword4, keyword5
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=temperature,
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
    except:
        en_short = en_long = is_short = is_long = ""
        keywords = []

    return en_short, en_long, is_short, is_long, keywords
