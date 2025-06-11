import './CategoryList.css'

export function CategoryList(props){
    return (
        <div className='recipe-categories'>
            {props.categories.map((cat) => {
                return (
                    <div
                        className="category-badge"
                        style = {{backgroundColor: cat.color}}
                        key={`category-${cat.id}`}
                    >
                        {cat.name}
                    </div>
                );
            })}
        </div>
    )
}

//deci trimitem in cazul asta categoria prin props si iteram prin ea folosind map, iteratorul e cat, in cazul duration badge e obv doar un string so no iteration