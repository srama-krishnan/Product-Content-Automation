import re
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values(".env")
client = OpenAI(api_key=config["APIKEY"])

def generate_seo_descriptions(official_description, temperature=0.7, tone_instruction="Write professionally and highlight key features."):

    system_prompt = f"""
You are an expert SEO copywriter generating compelling product descriptions for an Iceland-based e-commerce website (ht.is).

Follow these steps:
1. Read the official product description.
2. Generate a SHORT description optimized for Google search (15 to 30 words) with keywords in English.
3. Generate a LONG description (150-300 words) in English that is engaging, keyword-rich, and informative for Icelandic customers.
4. The style/tone should follow: "{tone_instruction}"
5. Do not invent technical details — use only those mentioned in the input.
6. Avoid markdown symbols like **, *, >, etc.

Respond in this format:

[SHORT DESCRIPTION]
<Insert the tagline, followed by the short description in English here>

[LONG DESCRIPTION]
<Insert Long Description in English here>

[KEYWORDS]
keyword1, keyword2, keyword3, keyword4, keyword5
(Keywords alone should always be in English)
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
        short = re.search(r'\[SHORT DESCRIPTION\](.*?)\[LONG DESCRIPTION\]', content, re.DOTALL).group(1).strip()
        long = re.search(r'\[LONG DESCRIPTION\](.*?)\[KEYWORDS\]', content, re.DOTALL).group(1).strip()
        keywords = re.search(r'\[KEYWORDS\](.*)', content, re.DOTALL).group(1).strip().split(",")
        keywords = [k.strip().lower() for k in keywords if k.strip()]
    except:
        short, long, keywords = "", "", []

    return short, long, keywords