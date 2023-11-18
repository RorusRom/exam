import requests
from bs4 import BeautifulSoup

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)

headers = {"User-agent": user_agent}
session = requests.Session()


def extract_discounted_product_info(product):
    title = product.find('a', class_="product-card__title").text.strip()
    review_element = product.find('a', class_="review-button__link")
    reviews = review_element.text.strip() if review_element else "No reviews"
    price_element = product.find('div', class_="v-pb__cur discount")
    price = price_element.text.strip() if price_element else "Price not available"

    return title, price, reviews


def scrape_discounted_products(page_number, file):
    url = f"https://allo.ua/ua/products/mobile/{page_number}"
    response = session.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        discounted_products = soup.find_all('div', class_="product-card")

        for product in discounted_products:
            product_info = extract_discounted_product_info(product)
            print(*product_info)
            file.write(f"Page {page_number} {' '.join(product_info)}\n")


def main():
    with open("discounted_products_with_reviews.txt", "a", encoding="utf-8") as file:
        for page_number in range(1, 25):
            print(f"Scraping Page {page_number}")
            scrape_discounted_products(page_number, file)


if __name__ == "__main__":
    main()