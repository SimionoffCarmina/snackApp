import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './RecipePage.css';

export function RecipePage() {
  const { recipeId } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [servings, setServings] = useState('1');
  const [error, setError] = useState(false);

  useEffect(() => {
    async function fetchRecipe() {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/recipes/${recipeId}`);
        if (!response.ok) {
          throw new Error('Recipe not found');
        }
        const data = await response.json();
        setRecipe(data);
        setError(false);
      } catch {
        setError(true);
      }
    }

    fetchRecipe();
  }, [recipeId]);

  if (error) {
    return <div className="recipe-error">Recipe not found.</div>;
  }

  if (!recipe) {
    return <div className="recipe-loading">Loading...</div>;
  }

  const servingsNumber = Number(servings) >= 1 ? Number(servings) : 1;

  return (
    <div className="recipe-page">
      <h1>{recipe.name}</h1>

      <div className="recipe-pictures">
        {recipe.pictures?.map((pic, index) => (
          <img
            key={index}
            src={pic}
            alt={`${recipe.name} - image ${index + 1}`}
            className="recipe-image"
            style={{ maxWidth: '300px', marginRight: '10px' }}
          />
        ))}
      </div>

      <p><strong>Duration:</strong> {recipe.duration}</p>

      <div className="categories">
        {recipe.categories.map((cat) => (
          <span
            key={cat.id}
            className="category-badge"
            style={{ backgroundColor: cat.color }}
          >
            {cat.name}
          </span>
        ))}
      </div>

      <div className="servings-control">
        <label htmlFor="servings">Servings: </label>
        <input
          type="number"
          id="servings"
          min="1"
          value={servings}
          onChange={(e) => {
            const val = e.target.value;
            if (val === '') {
              setServings('');
            } else {
              const num = Number(val);
              if (num >= 1) setServings(val);
            }
          }}
          onBlur={() => {
            if (servings === '' || Number(servings) < 1) {
              setServings('1');
            }
          }}
        />
      </div>

      <h2>Ingredients</h2>
      <ul>
        {recipe.ingredients.map((ingredient) => (
          <li key={ingredient.id}>
            {ingredient.quantity * servingsNumber}
            {ingredient.unit ? ` ${ingredient.unit}` : ''} {ingredient.name}
          </li>
        ))}
      </ul>

      <h2>Instructions</h2>
      {Array.isArray(recipe.instructions) ? (
        <ol>
          {recipe.instructions.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      ) : (
        <p>{recipe.instructions || 'No instructions available.'}</p>
      )}
    </div>
  );
}
