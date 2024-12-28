import React, { useState } from 'react';
import "./Form.css"
function Form({ onSummarize }) {
    const [text, setText] = useState('');
    const [language, setLanguage] = useState('en');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSummarize(text, language);
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Text:
                <textarea value={text} onChange={(e) => setText(e.target.value)} required />
            </label>
            <label>
                Language:
                <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                    <option value="en">English</option>
                    <option value="hi">Hindi</option>
                    <option value="kn">Kannada</option>
                    <option value="ta">Tamil</option>
                    <option value="te">Telugu</option>
                </select>
            </label>
            <button type="submit">Summarize</button>
        </form>
    );
}

export default Form;
