import asyncio
from bs4 import BeautifulSoup
from time import time
from httpx import AsyncClient


import constants as csts
from async_scrap_book import scrap_book
from utils import scrap


async def scrap_urls_books(url_category: str, session: AsyncClient) -> list:
    """ retourne la liste de toutes les urls des livres de la catérorie
    dont l'url est entrée en paramètre et le nom de cette categorie """
    next_page = True
    url_category_page = url_category
    books_urls_category = []

    while next_page:
        response = await scrap(url_category_page, session=session)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")

        if url_category_page == url_category:
            category_name = soup.find('h1').text  # enregistre le nom de la catégorie

        for h3 in soup.findAll('h3'):  # balise 'h3' contient les urls des livres
            url_book = h3.find('a')['href'].replace('../../..', csts.URL_SITE + '/catalogue')
            books_urls_category.append(url_book)

        next_page = soup.find('li', {"class": "next"})
        if next_page:
            url_category_page = url_category.replace('index.html', '') + soup.find('li',
                                                                                   {"class": "next"}).find('a')['href']
    return books_urls_category, category_name


async def scrap_category(url_category: str, session: AsyncClient) -> list:
    tasks = []
    urls_books = await scrap_urls_books(url_category, session=session)
    for url in urls_books[0]:
        tasks.append(scrap_book(url, session=session))
    results = await asyncio.gather(*tasks)
    results.insert(0, urls_books[1])
    return results


async def main():
    start = time()
    async with AsyncClient() as session:
        url_category = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
        results = await scrap_category(url_category, session)
    print(results)
    print(f"finished scraping in: {time() - start:.1f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
