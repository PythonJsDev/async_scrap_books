import asyncio
from bs4 import BeautifulSoup
from time import time
from httpx import AsyncClient

import constants as csts
from utils import scrap


async def scrap_book(url_book: str, session) -> dict:
    """ retourne dans un dictionnaire, les données du livre dont l'url est passée en paramètre.
        Données : title, product_description, universal_product_code (upc),
                  price_including_tax, price_excluding_tax, number_available,
                  review_rating, product_page_url, image_url """

    book_data = {}
    response = await scrap(url_book, session=session)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")

    # titre du livre
    book_data["title"] = soup.find('h1').text

    # description du livre
    book_data["product_description"] = soup.find(attrs={'name': 'description'}).attrs["content"].strip()

    # infos du tableau
    book_data["universal_product_code (upc)"] = soup.findAll('td')[0].text
    book_data["price_excluding_tax"] = soup.findAll('td')[2].text
    book_data["price_including_tax"] = soup.findAll('td')[3].text
    book_data["number_available"] = soup.findAll('td')[5].text

    # review_rating
    letter_number = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    book_data["review_rating"] = letter_number[soup.find('p', {'class': 'star-rating'}).attrs['class'][1]]

    # url du produit
    book_data["product_page_url"] = url_book

    # url de l'image
    book_data["image_url"] = soup.find("img")["src"].replace('../..', csts.URL_SITE)
    return book_data


async def main():
    start = time()
    async with AsyncClient() as session:
        url = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
        await scrap_book(url, session=session)
    print(f"finished scraping in: {time() - start:.1f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
