import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router'
import './App.css'
import { Navbar } from "./components/Navbar.jsx"
import { HomePage } from './pages/HomePage.jsx'
import { RecipePage } from './pages/RecipePage.jsx'
import { AddRecipeModal } from './components/AddRecipeForm.jsx'
import { AddCategoryModal } from './components/AddCategoryModal.jsx'

function App() {
  const [showAddModal, setShowAddModal] = useState(false);
  const [showAddCategoryModal, setShowAddCategoryModal] = useState(false);

  return (
    <>
      <Navbar
        onAddRecipe={() => setShowAddModal(true)}
        onAddCategory={() => setShowAddCategoryModal(true)}
      />

      <BrowserRouter>
        <Routes>
          <Route
            path='/'
            element={<HomePage />}
          />
          <Route
            path='/recipes/:recipeId'
            element={<RecipePage />}
          />
        </Routes>
      </BrowserRouter>

      <AddRecipeModal showAddModal={showAddModal} setShowAddModal={setShowAddModal} />
      <AddCategoryModal show={showAddCategoryModal}   handleClose={() => setShowAddCategoryModal(false)}
 />
    </>
  )
}

export default App