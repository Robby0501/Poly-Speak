import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function AuthPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    try {
      console.log('Attempting to login with:', { email, password });
      const response = await axios.post('http://localhost:5001/login', { email, password }, {
        withCredentials: true,
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log('Login response:', response.data);
      navigate('/dashboard', {
        state: {
          userId: response.data.user_id,
          language: response.data.language_to_learn,
        }
      });
    } catch (error) {
      console.error('Auth error:', error);
      if (error.response) {
        console.error('Error data:', error.response.data);
        console.error('Error status:', error.response.status);
        setErrorMessage(error.response.data.error || 'An error occurred during login');
      } else if (error.request) {
        console.error('Error request:', error.request);
        setErrorMessage('No response received from the server. Please try again.');
      } else {
        console.error('Error message:', error.message);
        setErrorMessage('An error occurred while sending the request. Please try again.');
      }
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
      <button onClick={() => navigate('/register')}>
        Need an account? Sign Up
      </button>
    </div>
  );
}

export default AuthPage;