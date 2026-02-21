import os
import json
import random
import time
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CONFIGURATION ---
BRAND_NAME = "ServicesHubnest"
BASE_URL = "https://serviceshubnest.github.io" # Update this to your final URL

# SEO SEED DATA
CITIES = ["London", "Manchester", "New York", "Chicago", "Los Angeles", "Toronto"]
SERVICES = [
    {"slug": "emergency-plumber", "title": "24/7 Emergency Plumber", "desc": "Urgent leak and burst pipe repair."},
    {"slug": "drain-cleaning", "title": "Professional Drain Cleaning", "desc": "Clearing stubborn clogs and main line blockages."},
    {"slug": "water-heater", "title": "Water Heater Repair & Install", "desc": "Fast service for gas and electric heaters."}
]

def human_sync_delay():
    """Safety: Random delay between 1-5 mins to avoid Google bot-detection."""
    wait = random.randint(60, 300)
    print(f"[*] System Sync: Pausing for {wait}s to maintain natural update patterns...")
    time.sleep(wait)

def notify_google_indexing(url):
    """Pings Google Indexing API using GitHub Secrets."""
    try:
        if 'GOOGLE_CREDENTIALS' not in os.environ:
            print("[!] Skip Indexing: Secret 'GOOGLE_CREDENTIALS' not found.")
            return
        
        info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=["https://www.googleapis.com/auth/indexing"]
        )
        service = build("indexing", "v3", credentials=creds)
        body = {"url": url, "type": "URL_UPDATED"}
        service.urlNotifications().publish(body=body).execute()
        print(f"[✓] Google Search Index notified: {url}")
    except Exception as e:
        print(f"[!] Indexing Error: {e}")

def build_resource_library():
    """Generates a new service page and a downloadable resource."""
    # Pick a random city and service for this hour's update
    city = random.choice(CITIES)
    service = random.choice(SERVICES)
    
    # Create folder structure
    for folder in ['services', 'downloads']:
        if not os.path.exists(folder): os.makedirs(folder)

    slug = f"{service['slug']}-{city.lower().replace(' ', '-')}"
    page_title = f"{service['title']} in {city}"
    
    # 1. Generate SEO Web Page
    page_path = f"services/{slug}.html"
    with open(page_path, "w") as f:
        f.write(f"<html><head><title>{page_title}</title></head><body>")
        f.write(f"<h1>{page_title}</h1><p>{service['desc']} Available now in {city}.</p>")
        f.write(f"<footer>© 2026 {BRAND_NAME}</footer></body></html>")

    # 2. Generate Downloadable TXT Resource
    with open(f"downloads/{slug}-guide.txt", "w") as f:
        f.write(f"{BRAND_NAME} Official Resource\n")
        f.write(f"Topic: {page_title}\nDate: {datetime.now()}\n")
        f.write(f"Summary: This document outlines emergency protocols for {service['title']}.")

    # 3. Notify Google
    notify_google_indexing(f"{BASE_URL}/{page_path}")

if __name__ == "__main__":
    human_sync_delay()
    build_resource_library()
