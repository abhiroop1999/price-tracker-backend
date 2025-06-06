import requests
from bs4 import BeautifulSoup
from app.utils.alert import send_alert

def scrape_product(data):
    try:
        response = requests.get(data.url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')

        price_tag = soup.select_one(".price")
        if not price_tag:
            return {"error": "No element with class .price found on the page."}

        price_text = price_tag.text.strip().replace("$", "")
        current_price = float(price_text)

        if current_price <= data.threshold:
            send_alert(data.email, data.url, current_price)

        return {"price": current_price, "alert_sent": current_price <= data.threshold}

    except Exception as e:
        return {"error": str(e)}
