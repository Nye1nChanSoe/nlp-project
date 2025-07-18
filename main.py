from threading import Thread
from cron.scheduler import scrape_article_every_minute
import uvicorn
from db import database
import time
import pickle


if __name__ == "__main__":
    database.init_db()
    with open("model/categories.pkl", "rb") as f:
        categories = pickle.load(f)
        print("Model loaded. It can predict the following categories:")
        for label in categories.keys():
            print(f"  - {label}")
    time.sleep(2)

    Thread(target=scrape_article_every_minute, daemon=True).start()
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
