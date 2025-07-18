import { useEffect, useState } from "react";

type Article = {
  id: number;
  title: string;
  url: string;
  content: string;
  predicted_category?: string | null;
  created_at: string;
};

function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://0.0.0.0:8000/articles")
      .then((res) => res.json())
      .then((data: Article[]) => {
        console.log(data);
        setArticles(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch articles:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>📰 News Dashboard</h1>

      {!loading && articles.length === 0 && <p>No articles found.</p>}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {articles.map((article) => (
          <li
            key={article.id}
            style={{
              border: "1px solid #ddd",
              marginBottom: "1rem",
              padding: "1rem",
              borderRadius: "6px",
            }}
          >
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              <h2 style={{ margin: "0 0 0.5rem 0", color: "#0077cc" }}>
                {article.title || "[Untitled]"}
              </h2>
            </a>
            <p style={{ fontSize: "0.9rem", color: "#333" }}>
              {article.content.slice(0, 1000)}...
            </p>
            <p style={{ fontSize: "0.8rem", color: "#666" }}>
              <strong>Category:</strong>{" "}
              {article.predicted_category || "Uncategorized"} •{" "}
              {new Date(article.created_at).toLocaleString()}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
