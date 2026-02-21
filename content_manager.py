import os
import random
import pandas as pd
import requests
from oauth2client.service_account import ServiceAccountCredentials

# ==========================================
# 1. PASTE YOUR KEYWORD LISTS HERE
# ==========================================
# [Paste ULTRA_PLUMBING_KEYWORDS here]
# [Paste ALL_EXPANDED_BOOK_KEYWORDS here]

BRAND_NAME = "ServicesHubnest"
PLUMBER_PHONE = "+13085508314"

# ==========================================
# 2. THE INDEXING API FUNCTION
# ==========================================
def ping_google_indexing(url):
    SCOPES = ["https://www.googleapis.com/auth/indexing"]
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    
    # service_account.json is the file you get from Google Cloud
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPES)
        access_token = creds.get_access_token().access_token
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        body = {"url": url, "type": "URL_UPDATED"}
        response = requests.post(ENDPOINT, json=body, headers=headers)
        print(f"Index Request: {response.status_code} for {url}")
    except Exception as e:
        print(f"Indexing Error: {e}")

# ==========================================
# 3. THE PAGE BUILDER
# ==========================================
def build_and_index():
    # Load your Excel
    df = pd.read_excel("locations.xlsx")
    row = df.sample(n=1).iloc[0]
    
    city = str(row['City'])
    zip_code = str(row['ZipCode'])

    # Pick random keywords from your massive lists
    p_key = random.choice(ULTRA_PLUMBING_KEYWORDS).format(city=city, zip_code=zip_code)
    b_key = random.choice(ALL_EXPANDED_BOOK_KEYWORDS)

    slug = f"emergency-repair-{zip_code}-{random.randint(100,999)}"
    file_path = f"services/{slug}.html"
    full_url = f"https://serviceshubnest.github.io/{file_path}"

    # Generate HTML content
    html = f"<html><head><title>{p_key}</title></head><body><h1>{p_key}</h1><p>{b_key}</p></body></html>"

    # Save File
    if not os.path.exists('services'): os.makedirs('services')
    with open(file_path, "w") as f:
        f.write(html)

    # PUSH TO GOOGLE IMMEDIATELY
    ping_google_indexing(full_url)

if __name__ == "__main__":
    build_and_index()
