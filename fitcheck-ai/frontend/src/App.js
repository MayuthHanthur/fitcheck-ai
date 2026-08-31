import { useState, useEffect } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [items, setItems] = useState([]);
  const [outfit, setOutfit] = useState(null);

  const loadItems = () => {
    fetch(`${API}/items`)
      .then((res) => res.json())
      .then((data) => setItems(data));
  };

  useEffect(() => {
    loadItems();
  }, []);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    await fetch(`${API}/upload`, {
      method: "POST",
      body: formData,
    });

    loadItems();
  };

  const getRecommendation = () => {
    fetch(`${API}/recommend`)
      .then((res) => res.json())
      .then((data) => setOutfit(data));
  };

  return (
    <div className="app">
      <header>
        <h1>
          FitCheck<span className="accent">.ai</span>
        </h1>
        <p>Your AI-powered virtual wardrobe</p>
      </header>

      <section className="upload-section">
        <label className="upload-btn">
          Upload Clothing Item
          <input type="file" onChange={handleUpload} hidden />
        </label>
      </section>

      <section className="wardrobe-grid">
        {items.map((item, i) => (
          <div className="item-card" key={i}>
            <img src={`${API}/uploads/${item.filename}`} alt={item.category} />
            <p>{item.category}</p>
          </div>
        ))}
      </section>

      <section className="recommend-section">
        <button className="recommend-btn" onClick={getRecommendation}>
          Suggest an Outfit
        </button>

        {outfit && !outfit.error && (
          <div className="outfit-result">
            <img src={`${API}/uploads/${outfit.top}`} alt="top" />
            <img src={`${API}/uploads/${outfit.bottom}`} alt="bottom" />
            <img src={`${API}/uploads/${outfit.shoes}`} alt="shoes" />
          </div>
        )}

        {outfit?.error && <p className="error">{outfit.error}</p>}
      </section>
    </div>
  );
}

export default App;