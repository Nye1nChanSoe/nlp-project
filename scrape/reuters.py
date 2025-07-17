from bs4 import BeautifulSoup
from .config import BASE_URL, get_headers
from .utils import get_retry_session, sleep_random
from db.database import insert_article, mark_url_seen, get_unseen_links

session = get_retry_session()


def get_sections():
    """Scrape the Reuters homepage and extract main section URLs."""
    res = session.get(BASE_URL, headers=get_headers())
    soup = BeautifulSoup(res.text, "lxml")
    sections = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if (
            href.startswith("/")
            and href.count("/") == 2
            and "/video" not in href
            and "/pictures" not in href
        ):
            sections.add(BASE_URL + href)

    return list(sections)


def get_article_links(section_url, limit=30):
    """Scrape article links from a section page."""
    res = session.get(section_url, headers=get_headers())
    print(res)
    soup = BeautifulSoup(res.text, "lxml")
    anchors = soup.find_all("a", href=True)

    links = []
    for a in anchors:
        href = a["href"]
        if href.startswith("/"):
            full_url = BASE_URL.rstrip("/") + href
            if full_url not in links and "/video/" not in full_url:
                links.append(full_url)
        if len(links) >= limit:
            break
    return links


def scrape_article(url):
    """Scrape the title and full content from a single article."""
    res = session.get(url, headers=get_headers())
    soup = BeautifulSoup(res.text, "lxml")
    title_tag = soup.find("h1")
    paragraphs = soup.find_all("p")

    title = title_tag.text.strip() if title_tag else "No title"
    content = " ".join(p.text.strip() for p in paragraphs)

    return {"url": url, "title": title, "content": content}
