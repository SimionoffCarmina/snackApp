import hourglass from "../assets/hourglass.svg";
import React from "react";

export function DurationBadge(props){
    return (
        <div className="recipe-duration">
            <img src={hourglass} alt="Hourglass icon" />
            {props.duration}
        </div>
    )
}
