import React, { useState, useEffect } from "react";
import "./App.css";
import SearchBar from "./components/SearchBar";
import RecipeCard from "./components/RecipeCard";
const searchApi = "https://www.themealdb.com/api/json/v1/1/search.php?s=";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [query, setQuery] = useState("");  // Initial query empty for manual search
  const [recipes, setRecipes] = useState([]);
  const [history, setHistory] = useState(
    JSON.parse(localStorage.getItem("searchHistory")) || []
  );

  // Save search history
  const addToHistory = (query) => {
    if (query && !history.includes(query)) {
      const updatedHistory = [...history, query];
      setHistory(updatedHistory);
      localStorage.setItem("searchHistory", JSON.stringify(updatedHistory));
    }
  };

  // Search for the recipe
  const searchRecipes = async () => {
    setIsLoading(true);
    const url = searchApi + query;
    const res = await fetch(url);
    const data = await res.json();
    setRecipes(data.meals);
    setIsLoading(false);
    addToHistory(query);
  };

  // This useEffect runs only if there is a query on initial load
  useEffect(() => {
    const fetchPopularRecipes = async () => {
      setIsLoading(true);
      const res = await fetch(searchApi);
      const data = await res.json();
      setRecipes(data.meals);
      setIsLoading(false);
    };

    fetchPopularRecipes();
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    searchRecipes();
  };

  const handleHistoryClick = (item) => {
    setQuery(item);
    searchRecipes();
  };

  return (
    <div className="container">
      <h2>Our Food Recipes</h2>
      <SearchBar
        isLoading={isLoading}
        query={query}
        setQuery={setQuery}
        handleSubmit={handleSubmit}
      />
      <div className="main-content">
        <div className="history">
          <h3>Search History</h3>
          {history.length > 0 ? (
            <ul>
              {history.map((item, index) => (
                <li key={index} onClick={() => handleHistoryClick(item)}>
                  {item}
                </li>
              ))}
            </ul>
          ) : (
            <p>No history available.</p>
          )}
        </div>
        <div className="recipes">
          {recipes ? (
            recipes.map((recipe) => (
              <RecipeCard key={recipe.idMeal} recipe={recipe} />
            ))
          ) : (
            "No Results."
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
