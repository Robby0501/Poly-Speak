import React, { useState } from 'react';
import axios from 'axios';

function UserRegistration() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [languageToLearn, setLanguageToLearn] = useState('');
  const [proficiencyLevel, setProficiencyLevel] = useState('');
  const [dailyGoal, setDailyGoal] = useState('');
  const [startOption, setStartOption] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    try {
      const response = await axios.post('http://localhost:5001/user', {
        name,
        email,
        password,
        language_to_learn: languageToLearn,
        proficiency_level: proficiencyLevel,
        daily_goal: dailyGoal,
        start_option: startOption
      }, {
        headers: {
          'Content-Type': 'application/json',
        }
      });

      console.log(response.data);
      setSuccessMessage('User created successfully!');
      // Clear the form
      setName('');
      setEmail('');
      setPassword('');
      setLanguageToLearn('');
      setProficiencyLevel('');
      setDailyGoal('');
      setStartOption('');
    } catch (error) {
      console.error('Error creating user:', error);
      if (error.response) {
        setErrorMessage(error.response.data.error || 'An error occurred while creating the user.');
      } else {
        setErrorMessage('An error occurred while creating the user.');
      }
    }
  };

  return (
    <div>
      <h2>User Registration</h2>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <input type="text" placeholder="Language to Learn" value={languageToLearn} onChange={(e) => setLanguageToLearn(e.target.value)} required />
        <input type="text" placeholder="Proficiency Level" value={proficiencyLevel} onChange={(e) => setProficiencyLevel(e.target.value)} required />
        <input type="number" placeholder="Daily Goal (minutes)" value={dailyGoal} onChange={(e) => setDailyGoal(e.target.value)} required />
        <input type="text" placeholder="Start Option" value={startOption} onChange={(e) => setStartOption(e.target.value)} required />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default UserRegistration;