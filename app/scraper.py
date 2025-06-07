import requests
from bs4 import BeautifulSoup
from app.utils.alert import send_alert

def scrape_product(data):
    try:
        # Validate incoming request payload
        if data.url is None or data.threshold is None or data.email is None:
            return {"error": "Missing required input: url, threshold, or email."}

        response = requests.get(data.url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        price_tag = soup.select_one(".price_color")
        if not price_tag or not price_tag.text:
            return {"error": "No element with class .price_color found or price text is empty."}

        raw_text = price_tag.text
        price_text = (
            raw_text
            .strip()
            .replace("£", "")
            .replace("Â", "")
            .replace(",", "")
        )

        if not price_text:
            return {"error": "Price text was empty after cleaning."}

        try:
            current_price = float(price_text)
        except ValueError:
            return {"error": f"Could not convert cleaned price '{price_text}' to float."}

        if current_price <= float(data.threshold):
            send_alert(data.email, data.url, current_price)

        return {"price": current_price, "alert_sent": current_price <= float(data.threshold)}

    except Exception as e:
        return {"error": str(e)}
