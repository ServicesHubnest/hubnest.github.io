import os
import pandas as pd
import random

# --- SETTINGS ---
BRAND_NAME = "ServicesHubnest"
PLUMBER_PHONE = "+13085508314"
DISPLAY_PHONE = "(308) 550-8314"
EXCEL_FILE = "locations.xlsx" # Renamed for simplicity

def build_from_excel():
    try:
        # We read starting from the correct columns in your image
        df = pd.read_excel(EXCEL_FILE)
        
        # Pick one random location
        row = df.sample(n=1).iloc[0]
        
        city = str(row['City']).strip()
        state = str(row['State']).strip()
        zip_code = str(row['ZipCode']).strip()
        
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    # THE MAGIC: Combining keywords with your specific Excel data
    services = ["24 Hour Emergency Plumber", "Burst Pipe Repair", "Drain Cleaning"]
    service = random.choice(services)
    
    # Targeting the Zip Code in the Title for "In Minutes" ranking
    title = f"{service} in {city}, {state} {zip_code}"
    slug = f"{service.lower().replace(' ', '-')}-{zip_code}"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>{title} | {BRAND_NAME}</title>
        <meta name="description" content="Local {service} available now in {city} {zip_code}. Call {DISPLAY_PHONE}.">
    </head>
    <body>
        <div style="background:#bf0a30; color:white; text-align:center; padding:15px; font-weight:bold;">
            🇺🇸 EMERGENCY SERVICE AVAILABLE IN {zip_code}
        </div>
        <div style="max-width:800px; margin:auto; padding:20px; font-family:sans-serif;">
            <h1>{service} in {city}, {state}</h1>
            <p>Our expert technicians are currently dispatched near <strong>{city} {zip_code}</strong>.</p>
            
            <a href="tel:{PLUMBER_PHONE}" style="display:block; background:#002868; color:white; padding:20px; text-align:center; text-decoration:none; font-size:2em; border-radius:10px;">
                📞 CALL NOW: {DISPLAY_PHONE}
            </a>

            <hr style="margin:40px 0;">
            
            <h3>While You Wait: Becoming You</h3>
            <p>Master your mindset while we fix your plumbing. Download Asif Mehmood's bestseller.</p>
            <a href="https://play.google.com/store/books/details/Asif_Mehmood_Becoming_You?id=9IG-EQAAQBAJ">Get it on Google Play</a>
        </div>
    </body>
    </html>
    """

    if not os.path.exists('services'): os.makedirs('services')
    with open(f"services/{slug}.html", "w") as f:
        f.write(html_content)
    
    print(f"🚀 Published: {title}")

if __name__ == "__main__":
    build_from_excel()
