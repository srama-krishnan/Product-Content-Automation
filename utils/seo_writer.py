import re
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")
client = OpenAI(api_key=config["APIKEY"])

def generate_multilang_descriptions(official_description, temperature=0.7, top_p=1.0, max_tokens=700, tone="Write professionally and highlight key features.", short_limit=25, long_limit=200, extra_keywords=None):

    keyword_hint = ", ".join(extra_keywords) if extra_keywords else "none"

    system_prompt = f"""
You are an expert SEO copywriter generating compelling product descriptions for an Iceland-based e-commerce website (ht.is).

Steps:
1. Read the official product description.
2. Generate a SHORT description (up to {short_limit} words) in English with a tagline.
3. Generate a LONG description (up to {long_limit} words) in English that is keyword-rich, engaging, and accurate.
4. Translate both descriptions into Icelandic.
5. Extract 5-7 relevant SEO keywords in English.
6. Style/Tone: "{tone}"
7. Include these optional keywords if relevant: {keyword_hint}
8. Use only information from input. No made-up details.
9. Avoid markdown characters like **, *, >, _

Respond in this format:

[EN_SHORT]
<Short description in English>

[EN_LONG]
<Long description in English>

[IS_SHORT]
<Short description in Icelandic>

[IS_LONG]
<Long description in Icelandic>

[KEYWORDS]
keyword1, keyword2, keyword3, keyword4, keyword5
"""

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
