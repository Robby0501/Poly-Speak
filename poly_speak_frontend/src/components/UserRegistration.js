import React, { useState } from 'react';
import axios from 'axios';

function UserRegistration() {
  const [username, setUsername] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('');
  const [proficiencyLevel, setProficiencyLevel] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5001/user', {
        username,
        target_language: targetLanguage,
        proficiency_level: proficiencyLevel
      }, {
        headers: {
          'Content-Type': 'application/json',
        }
      });
      console.log(response.data);
      alert('User created successfully!');
    } catch (error) {
      console.error('Error creating user:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
      }
      alert(`Error creating user: ${error.message}`);
    }
  };

  return (
    <div>
      <h2>User Registration</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Target Language"
          value={targetLanguage}
          onChange={(e) => setTargetLanguage(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Proficiency Level"
          value={proficiencyLevel}
          onChange={(e) => setProficiencyLevel(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default UserRegistration;