import os
import json
import random
import time
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# --- CONFIGURATION ---
BRAND_NAME = "ServicesHubnest"
BASE_URL = "https://serviceshubnest.github.io"

# --- YOUR OFFICIAL BOOKS ---
BOOKS = [
    {
        "name": "Becoming You: Confidence, Connection, and Growth",
        "type": "Ebook",
        "price": "9.99",
        "link": "https://play.google.com/store/books/details/Asif_Mehmood_Becoming_You?id=9IG-EQAAQBAJ",
        "desc": "Master the art of confidence and personal growth."
    },
    {
        "name": "Becoming You (Audiobook)",
        "type": "Audiobook",
        "price": "14.95",
        "link": "https://play.google.com/store/audiobooks/details?id=AQAAAEAaNSp1IM",
        "desc": "Listen and grow. The immersive audio experience of Becoming You."
    }
]

CITIES = ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool"]
SERVICES = [
    {"slug": "emergency-plumber", "title": "Emergency Plumber"},
    {"slug": "drain-cleaning", "title": "Drain Cleaning Specialist"},
    {"slug": "boiler-repair", "title": "Boiler Repair & Service"}
]

def generate_schema(book, city):
    """Creates Google Search 'Rich Snippets' for your book."""
    schema = {
        "@context": "https://schema.org/",
        "@type": "Book",
        "name": f"{book['name']} - {city} Readers Choice",
        "author": {"@type": "Person", "name": "Asif Mehmood"},
        "offers": {
            "@type": "Offer",
            "price": book['price'],
            "priceCurrency": "USD",
            "url": book['link']
        }
    }
    return json.dumps(schema)

def build_page():
    city = random.choice(CITIES)
    service = random.choice(SERVICES)
    book = random.choice(BOOKS) # Promotes one of your books
    
    slug = f"{service['slug']}-{city.lower()}"
    if not os.path.exists('services'): os.makedirs('services')

    html_content = f"""
    <html>
    <head>
        <title>{service['title']} in {city} | {BRAND_NAME}</title>
        <script type="application/ld+json">{generate_schema(book, city)}</script>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; color: #333; }}
            .book-card {{ border: 2px solid #007bff; padding: 20px; border-radius: 10px; margin-top: 30px; background: #f0f7ff; }}
            .btn {{ background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <h1>{service['title']} Services in {city}</h1>
        <p>Looking for expert help in {city}? Our local team is ready to assist with {service['title']}.</p>
        
        <div class="book-card">
            <h2>Featured Resource: {book['name']}</h2>
            <p>By Author Asif Mehmood</p>
            <p>{book['desc']}</p>
            <a href="{book['link']}" class="btn">Get it on Google Play (${book['price']})</a>
        </div>
        
        <footer><p>© 2026 {BRAND_NAME}</p></footer>
    </body>
    </html>
    """
    
    with open(f"services/{slug}.html", "w") as f:
        f.write(html_content)
    print(f"Created: {slug}.html promoting {book['type']}")

if __name__ == "__main__":
    build_page()
