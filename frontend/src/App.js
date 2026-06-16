import { useState } from "react";
import axios from "axios";

function App() {
  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  // Process Video
  const processVideo = async () => {
    try {
      console.log("Sending URL:", url);

      const res = await axios.post(
        "http://localhost:8000/process-video",
        {
          youtube_url: url,
        }
      );

      console.log("SUCCESS:", res.data);

      alert(res.data.message);

    } catch (error) {

      console.log("FULL ERROR:", error);

      if (error.response) {
        console.log("BACKEND ERROR:", error.response.data);
      }

      alert("Error processing video");
    }
  };

  // Ask Question
  const askQuestion = async () => {
    try {

      const res = await axios.post(
        "http://localhost:8000/ask",
        {
          question: question,
        }
      );

      console.log("FULL RESPONSE:", res.data);
      console.log("ANSWER:", res.data.answer);

      setAnswer(res.data.answer);

    } catch (error) {

      console.log("FULL ERROR:", error);

      if (error.response) {
        console.log("BACKEND ERROR:", error.response.data);
      }

      alert("Error getting answer");
    }
  };

  return (
    <div
      style={{
        width: "60%",
        margin: "50px auto",
        textAlign: "center",
      }}
    >
      <h1>YouTube Video Q&A Assistant</h1>

      <input
        type="text"
        placeholder="Enter YouTube URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
        }}
      />

      <button onClick={processVideo}>
        Process Video
      </button>

      <br />
      <br />

      <input
        type="text"
        placeholder="Ask a Question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px",
        }}
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <br />
      <br />

      <div
        style={{
          border: "1px solid gray",
          padding: "20px",
          minHeight: "150px",
          textAlign: "left",
        }}
      >
        <h3>Answer:</h3>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default App;