import time
from scrape.reuters import get_article_links, scrape_article
from db.database import insert_article, mark_url_seen, get_unseen_links
from scrape.utils import sleep_random
from model.prediction import predict

REUTERS_SECTIONS = {
    "WORLD": "https://www.reuters.com/world/",
    "BUSINESS": "https://www.reuters.com/business/",
    "MARKETS": "https://www.reuters.com/markets/",
    "SUBSTAINABILITY": "https://www.reuters.com/sustainability/",
    "LEGAL": "https://www.reuters.com/legal/",
    "TECHNOLOGY": "https://www.reuters.com/technology/",
}


def scrape_article_by_category():
    print("-- Starting scraping job --")

    for category, section_url in REUTERS_SECTIONS.items():
        print(f"\n Scraping section: {category}")

        try:
            all_links = get_article_links(section_url, limit=10)
            new_links = get_unseen_links(all_links, limit=2)

            for url in new_links:
                try:
                    article = scrape_article(url)
                    predicted_category = predict(article["content"])
                    article["predicted_category"] = predicted_category
                    insert_article(article)
                    mark_url_seen(url)

                    print(
                        f"Saved: {article['title']} | Predicted: {predicted_category}"
                    )
                    sleep_random()

                except Exception as e:
                    print(f"Error scraping {url}: {e}")

        except Exception as e:
            print(f"Error scraping section {category}: {e}")


def scrape_article_every_minute():
    while True:
        scrape_article_by_category()
        time.sleep(60)
