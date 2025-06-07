import requests
from bs4 import BeautifulSoup
from app.utils.alert import send_alert

def scrape_product(data):
    try:
        response = requests.get(data.url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        price_tag = soup.select_one(".price_color")
        if not price_tag:
            return {"error": "No element with class .price_color found on the page."}

        raw_text = price_tag.text if price_tag.text else ""
        price_text = (
            raw_text
            .strip()
            .replace("£", "")
            .replace("Â", "")
            .replace(",", "")
        )

        # Validate price_text is a number
        try:
            current_price = float(price_text)
        except ValueError:
            return {"error": f"Could not convert '{price_text}' to float."}

        if current_price <= data.threshold:
            send_alert(data.email, data.url, current_price)

        return {"price": current_price, "alert_sent": current_price <= data.threshold}

    except Exception as e:
        return {"error": str(e)}
