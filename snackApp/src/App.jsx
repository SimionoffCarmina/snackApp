import {useState, useEffect} from 'react'
import {BrowserRouter, Routes, Route} from 'react-router';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {HomePage} from './pages/HomePage.jsx'
import {NavBar} from './components/NavBar.jsx'
import {AddCategoryModal} from "./components/AddCategoryModal.jsx";

function App() {
    const [showCategoryModal, setShowCategoryModal] = useState(false)
    return (
        <>
            <NavBar
                handleOpenCategoryModal = {() => setShowCategoryModal(true)}
            />
            <BrowserRouter>
                <Routes>
                    <Route
                        path='/'
                        element={<HomePage/>}
                    />
                </Routes>
            </BrowserRouter>
            <AddCategoryModal show={showCategoryModal} handleClose={() => { setShowCategoryModal(false)}}/>
        </>
    )
}

export default App
