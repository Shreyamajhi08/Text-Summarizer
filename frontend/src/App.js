import React, { useState } from "react";
import axios from "axios";
import "./styles/App.css";
import Form from "./components/Form";
import Result from "./components/Result";
import Spinner from "./components/Spinner";
function App() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const handleSummarize = async (text, language) => {
    setLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/summarize", {
        text,
        language,
      });
      setSummary(response.data.summary);
    } catch (error) {
      console.error("Error summarizing text:", error);
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className="App">
      <h1>Text Summarizer</h1>
      <Form onSummarize={handleSummarize} />
      {loading ? <Spinner /> : summary && <Result summary={summary} />}
    </div>
  );
}

export default App;
