from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from db.database import init_db, get_all_articles

app = FastAPI(title="api")
init_db()


# -------------------------------
# Models
# -------------------------------


class ArticleIn(BaseModel):
    title: str
    content: str


class ScrapeURLIn(BaseModel):
    url: str


class ArticleOut(BaseModel):
    id: Optional[int]
    url: str
    title: str
    content: str
    predicted_category: Optional[str] = None
    created_at: Optional[str]


# -------------------------------
# Endpoints
# -------------------------------


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get("/results", response_model=List[ArticleOut], tags=["Results"])
def get_scraped_results():
    """Stub: return all scraped articles."""
    # TODO: query DB for articles
    return []


@app.get("/predict/{article_id}", tags=["Predict"])
def predict_from_db(article_id: int):
    """Stub: predict category for article by ID and update DB."""
    # TODO: fetch article, predict, save result
    return {"id": article_id, "predicted_category": "stub-category"}
