import './NavBar.css';

export function NavBar(props) {
    return (
        <nav>
            <div>
                SnackApp
            </div>
            <div>
                <button onClick={() => {props.handleOpenCategoryModal()}}>+ Add category </button>
                <button>+ Add recipe </button>
            </div>
        </nav>
    );
}