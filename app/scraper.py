import requests
from bs4 import BeautifulSoup
from app.utils.alert import send_alert

def scrape_product(data):
    try:
        response = requests.get(data.url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = 'utf-8'  # Ensures proper text encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        price_tag = soup.select_one(".price_color")  # Change selector based on site
        if not price_tag:
            return {"error": "No element with class .price_color found on the page."}

        price_text = (
            price_tag.text
            .strip()
            .replace("£", "")     # Remove pound sign
            .replace("Â", "")     # Remove unicode junk
            .replace(",", "")     # Handle thousand separators if any
        )

        current_price = float(price_text)

        if current_price <= data.threshold:
            send_alert(data.email, data.url, current_price)

        return {"price": current_price, "alert_sent": current_price <= data.threshold}

    except Exception as e:
        return {"error": str(e)}


