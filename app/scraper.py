import requests
from bs4 import BeautifulSoup
from app.utils.alert import send_alert

def scrape_product(data):
    try:
        response = requests.get(data.url, headers={"User-Agent": "Mozilla/5.0"})
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        price_tag = soup.select_one(".price_color")
        if not price_tag or not price_tag.text:
            return {"error": "Price element found but no text inside it."}

        price_text = (
            price_tag.text
            .strip()
            .replace("£", "")
            .replace("Â", "")
            .replace(",", "")
        )

        if not price_text or not price_text.replace(".", "").isdigit():
            return {"error": f"Unable to extract valid numeric price from text: '{price_tag.text}'"}

        current_price = float(price_text)

        if current_price <= data.threshold:
            send_alert(data.email, data.url, current_price)

        return {"price": current_price, "alert_sent": current_price <= data.threshold}

    except Exception as e:
        return {"error": str(e)}


