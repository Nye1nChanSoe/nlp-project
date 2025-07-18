from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from db.database import get_all_articles

app = FastAPI(title="api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/articles", response_model=List[ArticleOut], tags=["Articles"])
def get_scraped_results():
    rows = get_all_articles()
    return [
        ArticleOut(
            id=row[0],
            url=row[1],
            title=row[2],
            content=row[3],
            predicted_category=row[4],
            created_at=row[5],
        )
        for row in rows
    ]
