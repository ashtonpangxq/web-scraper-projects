import pandas as pd
from bs4 import BeautifulSoup
import requests

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": "productTitle"})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find(
            "span",
            attrs={"class": "a-size-base a-color-price offer-price a-text-normal"},
        ).string.strip()

    except AttributeError:
        price = ""

    return price


# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find(
            "i", attrs={"class": "a-icon a-icon-star a-star-4-5"}
        ).string.strip()

    except AttributeError:

        try:
            rating = soup.find("span", attrs={"class": "a-icon-alt"}).string.strip()
        except:
            rating = ""

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find(
            "span", attrs={"id": "acrCustomerReviewText"}
        ).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={"id": "availability"})
        available = available.find("span").string.strip()

    except AttributeError:
        available = ""

    return available


if __name__ == "__main__":

    # Headers for request
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    # The webpage URL
    URL = "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # Fetch links as List of Tag Objects
    links = soup.find_all(
        "a",
        attrs={
            "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
        },
    )

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
        links_list.append(link.get("href"))

    # Loop for extracting product details from each link
    amazon_product = {
        "product_title": [],
        "product_price": [],
        "product_rating": [],
        "no_of_reviews": [],
        "get_availability": [],
    }

    for link in links_list:

        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "lxml")

        amazon_product["product_title"].append(get_title(new_soup))
        amazon_product["product_price"].append(get_price(new_soup))
        amazon_product["product_rating"].append(get_rating(new_soup))
        amazon_product["no_of_reviews"].append(get_review_count(new_soup))
        amazon_product["get_availability"].append(get_availability(new_soup))

    df = pd.DataFrame.from_dict(amazon_product)
    df.to_csv("amazon_ps4_product_information.csv")
