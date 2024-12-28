import React from 'react';
import "./Result.css"
function Result({ summary }) {
    return (
        <div className="result">
            <h2>Summary</h2>
            <p>{summary}</p>
        </div>
    );
}

export default Result;
