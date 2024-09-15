import React, { useState } from 'react';
import axios from 'axios';

function Quiz() {
  const [username, setUsername] = useState('');
  const [topic, setTopic] = useState('');
  const [quiz, setQuiz] = useState('');

  const fetchQuiz = async () => {
    try {
      const response = await axios.get(`http://localhost:5001/quiz?username=${username}&topic=${topic}`);
      setQuiz(response.data.quiz);
    } catch (error) {
      console.error('Error fetching quiz:', error);
      alert('Error fetching quiz. Please try again.');
    }
  };

  return (
    <div>
      <h2>Get Quiz</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="text"
        placeholder="Topic"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      />
      <button onClick={fetchQuiz}>Get Quiz</button>
      {quiz && (
        <div>
          <h3>Quiz Content:</h3>
          <p>{quiz}</p>
        </div>
      )}
    </div>
  );
}

export default Quiz;