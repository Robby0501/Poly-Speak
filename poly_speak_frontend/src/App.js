import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AuthPage from './components/AuthPage';
import UserRegistration from './components/UserRegistration';
import StepByStepSignup from './components/StepByStepSignup';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>Poly Speak Language Learning App</h1>
        <Routes>
          <Route path="/" element={<AuthPage />} />
          <Route path="/register" element={<UserRegistration />} />
          <Route path="/signup" element={<StepByStepSignup />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;