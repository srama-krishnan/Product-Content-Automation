import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def is_large_enough_image(img_url, min_kb=5):
    try:
        head = requests.head(img_url, timeout=5)
        size = int(head.headers.get("Content-Length", 0))
        return size > min_kb * 1024
    except:
        return False
    
def extract_images_from_single_url(url, keywords=None, max_imgs=25):
    headers = {"User-Agent": "Mozilla/5.0"}

    if not keywords:
        keywords = []

    fallback_keywords = ['product', 'smart', 'uhd', 'tv', 'display', 'feature']
    keywords = [k.lower() for k in keywords]
    if len(keywords) < 3:
        keywords += fallback_keywords

    def normalize(src, base):
        if src.startswith("//"):
            return "https:" + src
        elif src.startswith("/"):
            return urljoin(base, src)
        elif not src.startswith("http"):
            return urljoin(base, src)
        return src

    def is_valid_filename(src):
        return not any(ext in src for ext in ['.svg', '.gif', 'icon', 'avatar', 'emoji', 'logo', 'flag'])

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        imgs = []

        for img in soup.find_all("img"):
            src = (
                img.get("src") or
                img.get("data-src") or
                img.get("data-lazy")
            )

            if not src:
                srcset_val = img.get("srcset", "")
                if srcset_val.strip():
                    src = srcset_val.strip().split()[0]

            if not src or len(src) < 5:
                continue

            src = normalize(src, url)

            if not is_valid_filename(src):
                continue

            alt = img.get("alt") or ""
            match_text = f"{src.lower()} {alt.lower()}"

            if any(k in match_text for k in keywords) or len(imgs) < max_imgs:
                if is_large_enough_image(src):
                    imgs.append(src)

            if len(imgs) >= max_imgs:
                break

        return imgs

    except Exception as e:
        print(f"⚠️ Skipping {url} → {e}")
        return []
    
def extract_images_from_all_urls(url_list, keywords, global_limit=20):
    all_images = []

    for url in url_list:
        print(f"🔍 Scanning {url}")
        imgs = extract_images_from_single_url(url, keywords, max_imgs=global_limit)
        for img in imgs:
            if img not in all_images and len(all_images) < global_limit:
                all_images.append(img)

        if len(all_images) >= global_limit:
            break

    return all_images