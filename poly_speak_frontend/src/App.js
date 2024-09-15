import React from 'react';
import UserRegistration from './components/UserRegistration';
import Lesson from './components/Lesson';
import Quiz from './components/Quiz';
import './App.css';

function App() {
  return (
    <div className="App">
      <h1>LangChain Language Learning App</h1>
      <UserRegistration />
      <Lesson />
      <Quiz />
    </div>
  );
}

export default App;
