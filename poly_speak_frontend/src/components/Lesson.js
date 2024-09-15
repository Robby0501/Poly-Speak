import React, { useState } from 'react';
import axios from 'axios';

function Lesson() {
  const [username, setUsername] = useState('');
  const [lessonType, setLessonType] = useState('vocabulary');
  const [lesson, setLesson] = useState('');

  const fetchLesson = async () => {
    try {
      const response = await axios.get(`http://localhost:5001/lesson?username=${username}&lesson_type=${lessonType}`);
      setLesson(response.data.lesson);
    } catch (error) {
      console.error('Error fetching lesson:', error);
      alert('Error fetching lesson. Please try again.');
    }
  };

  return (
    <div>
      <h2>Get Lesson</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <select value={lessonType} onChange={(e) => setLessonType(e.target.value)}>
        <option value="vocabulary">Vocabulary</option>
        <option value="grammar">Grammar</option>
      </select>
      <button onClick={fetchLesson}>Get Lesson</button>
      {lesson && (
        <div>
          <h3>Lesson Content:</h3>
          <p>{lesson}</p>
        </div>
      )}
    </div>
  );
}

export default Lesson;