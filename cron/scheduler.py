import time
from scrape.reuters import get_article_links, scrape_article
from db.database import insert_article, mark_url_seen, get_unseen_links
from scrape.utils import sleep_random
import os
import random


def scrape_article_every_minute():

    while True:
        print("-- job running --")
        BASE_URL = os.getenv("REUTERS_BASE")
        all_links = get_article_links(BASE_URL, limit=10)
        new_links = get_unseen_links(all_links, limit=10)

        for url in new_links:
            try:
                article = scrape_article(url)
                insert_article(article)
                mark_url_seen(url)
                print(f"saved: {article['title']}")
                sleep_random()
            except Exception as e:
                print(f"error scraping {url}: {e}")

        time.sleep(60)
