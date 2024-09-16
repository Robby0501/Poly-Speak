import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const languages = [
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'it', name: 'Italian', flag: '🇮🇹' },
  { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
  // Add more languages as needed
];

const proficiencyLevels = [
  "I'm new to the language",
  "I know some common words",
  "I can have basic conversations",
  "I can talk about various topics",
  "I can discuss most topics in detail"
];

const dailyGoals = [
  { minutes: 5, label: '5 min / day' },
  { minutes: 10, label: '10 min / day' },
  { minutes: 15, label: '15 min / day' },
  { minutes: 20, label: '20 min / day' },
];

function StepByStepSignup() {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [language, setLanguage] = useState('');
  const [proficiency, setProficiency] = useState('');
  const [dailyGoal, setDailyGoal] = useState('');
  const [startOption, setStartOption] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Get email and password from the state passed by UserRegistration
    const { email: stateEmail, password: statePassword } = location.state || {};
    if (stateEmail && statePassword) {
      setEmail(stateEmail);
      setPassword(statePassword);
    } else {
      // If email and password are not provided, redirect back to registration
      navigate('/register');
    }
  }, [location, navigate]);

  const handleSubmit = async (option) => {
    try {
      console.log('Submitting with:', { name, email, password, language, proficiency, dailyGoal, option });
      
      if (!name || !email || !password || !language || !proficiency || !dailyGoal || !option) {
        console.log('Missing fields:', { name, email, password, language, proficiency, dailyGoal, option });
        setError('Please fill in all fields');
        return null;
      }
  
      const response = await axios.post('http://localhost:5001/user', {
        name,
        email,
        password,
        language_to_learn: language,
        proficiency_level: proficiency,
        daily_goal: dailyGoal,
        start_option: option
      });
      console.log('User created:', response.data);
  
      // Generate initial lesson based on start_option
      const lessonResponse = await axios.get('http://localhost:5001/initial-lesson', {
        params: {
          user_id: response.data.user_id,
          start_option: option,
          proficiency_level: proficiency
        }
      });
      console.log('Initial lesson:', lessonResponse.data);
  
      return { userId: response.data.user_id, lesson: lessonResponse.data.lesson };
    } catch (error) {
      console.error('Error during signup:', error);
      console.error('Error response:', error.response?.data);
      setError(error.response?.data?.error || 'An error occurred during signup');
      return null;
    }
  };

  const handleSubmitWithOption = async (option) => {
    setStartOption(option);
    setError(''); // Clear any previous errors
  
    if (!name || !email || !password || !language || !proficiency || !dailyGoal) {
      setError('Please fill in all fields');
      return;
    }
  
    const result = await handleSubmit(option);
    if (result) {
      navigate('/dashboard', { 
        state: { 
          userId: result.userId, 
          language: language,
          lesson: result.lesson, 
          startOption: option 
        } 
      });
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div>
            <h2>What's your name?</h2>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
            />
            <button onClick={() => setStep(2)}>Next</button>
          </div>
        );
      case 2:
        return (
          <div>
            <h2>Hi {name}, what would you like to learn?</h2>
            {languages.map((lang) => (
              <button key={lang.code} onClick={() => { setLanguage(lang.name); setStep(3); }}>
                {lang.flag} {lang.name}
              </button>
            ))}
          </div>
        );
      case 3:
        return (
          <div>
            <h2>How much {language} do you know?</h2>
            {proficiencyLevels.map((level, index) => (
              <button key={index} onClick={() => { setProficiency(level); setStep(4); }}>
                {level}
              </button>
            ))}
          </div>
        );
      case 4:
        return (
          <div>
            <h2>What's your daily learning goal?</h2>
            {dailyGoals.map((goal) => (
              <button key={goal.minutes} onClick={() => { setDailyGoal(goal.minutes); setStep(5); }}>
                {goal.label}
              </button>
            ))}
          </div>
        );
        case 5:
            return (
              <div>
                <h2>Where would you like to start?</h2>
                <button onClick={() => {
                  console.log('From scratch clicked');
                  handleSubmitWithOption('from scratch');
                }}>
                  From scratch (take the easiest lesson of the course)
                </button>
                <button onClick={() => {
                  console.log('Find my level clicked');
                  handleSubmitWithOption('find my level');
                }}>
                  Find my level (let Poly recommend where you should start learning)
                </button>
              </div>
            );
      default:
        return null;
    }
  };

  return (
    <div>
      {renderStep()}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default StepByStepSignup;