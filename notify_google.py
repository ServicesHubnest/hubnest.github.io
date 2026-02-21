import os
import json
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

def notify_google():
    # 1. Setup Google Credentials
    json_creds = os.getenv("GOOGLE_CREDENTIALS")
    if not json_creds:
        print("❌ GOOGLE_CREDENTIALS Secret is missing!")
        return

    scopes = ["https://www.googleapis.com/auth/indexing"]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(json_creds), scopes)
        http = credentials.authorize(httplib2.Http())
        endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"

        # 2. Find the files created in the 'services' folder
        if not os.path.exists('services'):
            print("❌ No services folder found.")
            return

        # Get all .html files in the services folder
        files = [f for f in os.listdir('services') if f.endswith('.html')]
        
        if not files:
            print("p❌ No HTML files found to index.")
            return

        print(f"🔍 Found {len(files)} files. Notifying Google...")

        # 3. Notify Google for each file found
        for file_name in files:
            # Match the URL structure in your main script exactly
            full_url = f"https://serviceshubnest.github.io/hubnest.github.io/services/{file_name}"
            
            content = json.dumps({"url": full_url, "type": "URL_UPDATED"})
            response, content_resp = http.request(endpoint, method="POST", body=content)
            
            if response.status == 200:
                print(f"✅ Google Notified: {full_url}")
            elif response.status == 429:
                print("🛑 Quota Limit Reached.")
                break
            else:
                print(f"⚠️ Status {response.status} for {file_name}")

    except Exception as e:
        print(f"❌ Indexing Error: {e}")

if __name__ == "__main__":
    notify_google()
