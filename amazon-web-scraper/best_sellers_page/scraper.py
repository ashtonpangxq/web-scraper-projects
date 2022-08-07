import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_product_placings(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:

    try:
        product_placing = soup.find_all("span", attrs={"class": "zg-bdg-text"})

    except AttributeError:
        product_placing = ""

    return product_placing


def get_product_names(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:

    try:
        product_name = soup.find_all(
            "div", attrs={"class": "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"}
        )

    except AttributeError:
        product_name = ""

    return product_name


def get_product_ratings(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:

    try:
        product_ratings = soup.find_all("span", attrs={"class": "a-icon-alt"})

    except AttributeError:
        product_ratings = ""

    return product_ratings


def get_product_reviews(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:

    try:
        product_reviews = soup.find_all("span", attrs={"class": "a-size-small"})

    except AttributeError:
        product_reviews

    return product_reviews


def main() -> None:
    # The Webpage URL
    url = str(input("URL to Scrape: "))
    filename = str(input("Saved File Name: "))

    print(f"Starting Web Scraping from: {url} ...")

    # Headers for request
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    # HTTP Request
    webpage = requests.get(url, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    product_placing = get_product_placings(soup)
    product_names = get_product_names(soup)
    product_ratings = get_product_ratings(soup)
    product_reviews = get_product_reviews(soup)

    # Loop for extracting product details from each link
    amazon_products = {
        "product_placing": [],
        "product_names": [],
        "product_ratings": [],
        "no_of_reviews": [],
    }

    for i in range(len(product_placing)):
        amazon_products["product_placing"].append(product_placing[i].string.strip())
        amazon_products["product_names"].append(product_names[i].string.strip())
        amazon_products["product_ratings"].append(product_ratings[i].string.strip())
        amazon_products["no_of_reviews"].append(product_reviews[i].string.strip())

    print(f"Web Scraping Successful!")
    print(f"Starting to Export to CSV...")

    df = pd.DataFrame.from_dict(amazon_products)
    df.to_csv(f"{filename}.csv")

    return


if __name__ == "__main__":
    main()
    print(f"Export Completed!")
