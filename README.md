#### Réalisation d'un "scrapeur" asynchrone sur le site Books to Scrape  https://books.toscrape.com/


># Installation : 
1. Télécharger depuis GitHub l'ensemble des fichiers fichiers. 
2. Dans un environnement virtuel, installer les packages: requests, lxml, BeautifulSoup et httpx     
commandes:    
`pip install requests`,   
`pip install lxml`,   
`pip install beautifulsoup4`,   
`pip install httpx`

># Exécution :
- Pour lancer le programme taper la commande: `python async_scrap.py` 

- Les données sont stockées dans des fichiers csv (un fichier par catégorie de livres) dans l'arborescence : `data/csv` créée lors de l'exécution du programme.
- Les images de couverture des livres sont stockées dans le dossier : `data/img`

* Remarque: la tabulation est utilisée comme séparateur dans les fichiers csv





