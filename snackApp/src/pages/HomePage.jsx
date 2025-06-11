import React, { useEffect, useState } from 'react';
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import './HomePage.css';
import hourglass from '../assets/hourglass.svg';
import { CategoryList } from '../components/CategoryList.jsx';
import { DurationBadge } from "../components/DurationBadge.jsx";

export function HomePage() {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/recipes`)
      .then((response) => response.json())
      .then((data) => setRecipes(data));
  }, []);

  return (
    <>
      <h1>My recipes</h1>
      <div>Recipe count: {recipes.length}</div>
      <div className='recipes-container'>
        {recipes.map((recipe) => (
          <Link
            to={`/recipes/${recipe.id}`}
            key={`recipe-${recipe.id}`}
            style={{ textDecoration: 'none', color: 'inherit' }}
          >
            <Card>
              <Card.Img src={recipe.pictures[0]} height={300} />
              <Card.Body>
                <Card.Title>{recipe.name}</Card.Title>
                <CategoryList categories={recipe.categories} />
                <DurationBadge duration={recipe.duration} />
              </Card.Body>
            </Card>
          </Link>
        ))}
      </div>
    </>
  );
}