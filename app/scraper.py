import requests
from bs4 import BeautifulSoup
from app.utils.alert import send_alert

def scrape_product(data):
    try:
        # Validate input early
        if not data.url or not data.threshold or not data.email:
            return {"error": "Missing url, threshold, or email."}

        response = requests.get(data.url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        price_tag = soup.select_one(".price_color")
        if not price_tag or not price_tag.text:
            return {"error": "No element with class .price_color found or price text is empty."}

        raw_text = price_tag.text.strip()
        price_text = (
            raw_text
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

        alert_triggered = current_price <= float(data.threshold)
        if alert_triggered:
            try:
                send_alert(data.email, data.url, current_price)
            except Exception as alert_error:
                return {"error": f"Failed to send alert: {alert_error}"}

        return {
            "price": current_price,
            "alert_sent": alert_triggered
        }

    except Exception as e:
        return {"error": str(e)}

