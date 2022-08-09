import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from time import sleep


def get_page_name(soup: bs4.BeautifulSoup) -> str:

    try:
        page_name = soup.find(
            "h1", attrs={"class": "a-size-large a-spacing-medium a-text-bold"}
        ).string.strip()

    except AttributeError:
        page_name = "unidentified_page_name"

    return page_name


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

    print(f"Starting Web Scraping from: {url} ...")

    # Initialize driver
    driver = webdriver.Chrome("../../webdriver/chromedriver_win32/chromedriver")
    driver.get(url)

    # Scrolls To Bottom of Page to Load the Rest of the Page
    page_height = driver.execute_script("return document.body.scrollHeight")

    for value in range(0, page_height):
        driver.execute_script(f"window.scrollTo(0, {value});")

    # Soup Object containing all data
    soup = BeautifulSoup(driver.page_source, "lxml")

    driver.quit()

    page_name = get_page_name(soup)
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
        amazon_products["no_of_reviews"].append(
            "".join(product_reviews[i].string.strip().split(","))
        )

    print(f"Web Scraping Successful!")
    print(f"Starting to Export to CSV...")

    df = pd.DataFrame.from_dict(amazon_products)
    df.to_csv(f"{'_'.join(page_name.split(' '))}.csv")

    return


if __name__ == "__main__":
    main()
    print(f"Export Completed!")
