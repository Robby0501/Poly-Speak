import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';

function Dashboard() {
  const [units, setUnits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const location = useLocation();
  const navigate = useNavigate();
  const { userId, language, lesson, startOption } = location.state || {};

  useEffect(() => {
    if (!userId) {
      navigate('/');
      return;
    }

    const fetchUnits = async () => {
      try {
        const response = await axios.get(`http://localhost:5001/units/${userId}`);
        setUnits(response.data.units);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching units:', error);
        setError('Failed to load units. Please try again.');
        setLoading(false);
      }
    };

    fetchUnits();
  }, [userId, navigate]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="dashboard">
      <h1>{language} Learning Dashboard</h1>
      {startOption && <h2>Welcome! You're starting with: {startOption}</h2>}
      {lesson && <h3>Your first lesson: {lesson}</h3>}
      {units.map((unit, index) => (
        <div key={unit.id} className="unit">
          <h2>Unit {index + 1}: {unit.title}</h2>
          <div className="lessons">
            {unit.lessons.map((lesson) => (
              <div key={lesson.id} className="lesson">
                <h3>{lesson.title}</h3>
                <button onClick={() => {/* Handle lesson start */}}>Start Lesson</button>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Dashboard;