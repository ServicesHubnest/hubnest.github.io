import os
import json
import random
import pandas as pd
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

# ==========================================
# 🔥 1. MASSIVE KEYWORD LISTS (12,500+ Combos)
# ==========================================
problem_intent = ["Fix", "Repair", "Emergency Repair", "24/7 Repair", "Immediate Fix", "Stop Leak Now", "Call Now for Repair"]
service_types = ["Plumber", "Drain Cleaning", "Burst Pipe Repair", "Water Heater Installation", "Sewer Line Replacement", "Slab Leak Repair", "Toilet Repair"]
location_modifiers = ["{city}", "{zip_code}", "Near Me", "Local", "Available Now"]

ULTRA_PLUMBING_KEYWORDS = [f"{i} {s} {l}" for i in problem_intent for s in service_types for l in location_modifiers]

book_title = "Becoming You: Confidence, Connection, and Growth"
problem_intent_book = ["Overcoming Self-Doubt", "Stop Overthinking", "Build Confidence", "Improve Social Skills"]
buyer_modifiers = ["Book", "Guide", "Blueprint", "Practical Guide"]
audience_modifiers = ["for Professionals", "for Introverts", "for Leaders", "for Career Growth"]

# Change 'for l in audience_modifiers' to 'for a in audience_modifiers'
ALL_EXPANDED_BOOK_KEYWORDS = [
    f"{b} {p} {a}" 
    for b in buyer_modifiers 
    for p in problem_intent_book 
    for a in audience_modifiers
]

# ==========================================
# 🚀 2. THE INDEXING API LOGIC
# ==========================================
def notify_google_indexing(url):
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return

    scopes = ["https://www.googleapis.com/auth/indexing"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(json_creds), scopes)
        http = credentials.authorize(httplib2.Http())
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        
        content = json.dumps({"url": url, "type": "URL_UPDATED"})
        response, content_resp = http.request(endpoint, method="POST", body=content)
        
        if response.status == 200:
            print(f"✅ Google Notified: {url}")
        elif response.status == 429:
            print("🛑 Quota Limit (200) Reached. Stopping for today.")
            exit(0)
        else:
            print(f"⚠️ Status {response.status}: {content_resp}")
    except Exception as e:
        print(f"❌ Indexing Error: {e}")

# ==========================================
# 🚀 2. THE INDEXING API LOGIC
# ==========================================
def notify_google_indexing(url):
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return

    scopes = ["https://www.googleapis.com/auth/indexing"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(json_creds), scopes)
        http = credentials.authorize(httplib2.Http())
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        
        content = json.dumps({"url": url, "type": "URL_UPDATED"})
        response, content_resp = http.request(endpoint, method="POST", body=content)
        
        if response.status == 200:
            print(f"✅ Google Notified: {url}")
        elif response.status == 429:
            print("🛑 Quota Limit (200) Reached. Stopping for today.")
            exit(0)
        else:
            print(f"⚠️ Status {response.status}: {content_resp}")
    except Exception as e:
        print(f"❌ Indexing Error: {e}")

# ==========================================
# 🛠️ 3. PAGE BUILDER LOGIC
# ==========================================
def build_and_index():
    try:
        df = pd.read_excel("locations.xlsx")
    except Exception as e:
        print(f"Excel Error: {e}")
        return

    # Define your Brand Identity
    company_name = "Hubnest"
    tagline = "Essential Services, Expert Solutions"
    book_title = "Becoming You: Confidence, Connection, and Growth"

    # 🔥 Runs TWICE: 1 Plumbing Page + 1 Book Page per execution
    for category in ["plumbing", "book"]:
        row = df.sample(n=1).iloc[0]
        city, zip_code = str(row['City']), str(row['ZipCode'])

        if category == "plumbing":
            keyword = random.choice(ULTRA_PLUMBING_KEYWORDS).format(city=city, zip_code=zip_code)
            slug = f"plumber-{city.lower().replace(' ', '-')}-{zip_code}"
        else:
            keyword = random.choice(ALL_EXPANDED_BOOK_KEYWORDS)
            slug = f"book-{keyword.lower().replace(' ', '-')}-{zip_code}"

        file_path = f"services/{slug}.html"
        full_url = f"https://serviceshubnest.github.io/hubnest.github.io/{file_path}"

        # THE UPDATED PAGE DESIGN
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{keyword} | {company_name}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "{company_name}",
      "description": "{keyword}",
      "telephone": "(308) 550-8314",
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "{city}",
        "postalCode": "{zip_code}",
        "addressCountry": "US"
      }}
    }}
    </script>
</head>
<body style='font-family: sans-serif; padding: 0; margin: 0; line-height: 1.6; background: #fdfdfd; color: #333;'>
    
    <div style='background: #fff; border-bottom: 3px solid #007bff; padding: 25px; text-align: center;'>
        <h1 style='margin: 0; color: #222; font-size: 28px; letter-spacing: -1px;'>{company_name}</h1>
        <p style='margin: 5px 0 0 0; color: #555; font-weight: 600; font-size: 15px;'>{tagline}</p>
    </div>

    <div style='max-width: 700px; margin: 30px auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);'>
        <h2 style='color: #0056b3; border-bottom: 1px solid #eee; padding-bottom: 10px;'>{keyword}</h2>
        <p>Looking for reliable support in <b>{city} ({zip_code})</b>? <b>{company_name}</b> delivers <i>{tagline}</i> for every client. Our local team is ready to assist you with professional care and efficiency.</p>
        
        <div style='background: #e7f3ff; border-left: 5px solid #007bff; padding: 15px; margin: 20px 0; border-radius: 0 5px 5px 0;'>
            <strong style='color: #0056b3;'>📞 Contact Support:</strong> 
            <a href="tel:3085508314" style="color:#222; text-decoration:none; font-weight: bold; font-size: 1.1em;">(308) 550-8314</a>
        </div>

        <hr style='border: 0; border-top: 1px solid #eee; margin: 40px 0;'>

        <div style='text-align: center; background: #f8f9fa; padding: 30px; border-radius: 15px; border: 1px solid #e9ecef;'>
            <h3 style='margin-top: 0; color: #343a40;'>Verified Professional Resource</h3>
            <p style='color: #666;'>We highly recommend this guide on confidence and connection by author <b>Asif Mehmood</b>.</p>
            <p style='font-weight: bold; font-size: 1.2em; color: #000;'>{book_title}</p>
            
            <div style='margin-top: 25px;'>
                <a href="https://play.google.com/store/books/details?id=9IG-EQAAQBAJ" target="_blank">
                    <img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png' style='width: 190px;'/>
                </a>
                <div style='margin-top: 15px;'>
                    <a href="https://play.google.com/store/audiobooks/details?id=AQAAAEAaNSp1IM" style="color: #28a745; text-decoration: none; font-weight: bold; font-size: 0.95em;">
                        🎧 Also available as an Audiobook
                    </a>
                </div>
            </div>
            
            <p style='margin-top: 20px; font-size: 0.85em; color: #999;'>✓ Safe Link | Verified via Google Play Console</p>
        </div>
    </div>

    <footer style='text-align: center; padding: 30px; font-size: 13px; color: #888;'>
        &copy; 2026 <b>{company_name}</b><br>
        {tagline}<br>
        Serving {city}, {zip_code}
    </footer>
</body>
</html>"""

        if not os.path.exists('services'): 
            os.makedirs('services')
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        # Notify Google of the new professional page
        notify_google_indexing(full_url)

if __name__ == "__main__":
    build_and_index()
