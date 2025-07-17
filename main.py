from threading import Thread
from cron.scheduler import scrape_article_every_minute
import uvicorn
from db import database


if __name__ == "__main__":
    Thread(target=scrape_article_every_minute, daemon=True).start()
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)
