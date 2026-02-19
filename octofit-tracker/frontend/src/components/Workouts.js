import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = codespace
        ? `https://${codespace}-8000.app.github.dev/api/workouts/`
        : 'http://localhost:8000/api/workouts/';
      
      console.log('Fetching workouts from:', apiUrl);
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Workouts data received:', data);
      
      // Handle both paginated (.results) and plain array responses
      const workoutsData = data.results || data;
      setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching workouts:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  // Get difficulty badge color
  const getDifficultyBadge = (level) => {
    const levelLower = (level || '').toLowerCase();
    if (levelLower.includes('easy') || levelLower.includes('beginner')) return 'success';
    if (levelLower.includes('medium') || levelLower.includes('intermediate')) return 'warning';
    if (levelLower.includes('hard') || levelLower.includes('advanced')) return 'danger';
    return 'secondary';
  };

  return (
    <div className="container-fluid mt-4">
      <div className="page-header">
        <div className="container">
          <h1>💪 Workouts</h1>
          <p className="mb-0">Personalized workout suggestions and programs</p>
        </div>
      </div>
      
      <div className="container">
        {workouts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">🏋️</div>
            <h3>No Workouts Available</h3>
            <p>Add workout programs to get started!</p>
          </div>
        ) : (
          <div className="table-wrapper">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">Available Workouts ({workouts.length})</h5>
              <button className="btn btn-primary btn-sm">Create Workout</button>
            </div>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Workout Name</th>
                    <th>Category</th>
                    <th>Difficulty</th>
                    <th>Duration</th>
                    <th>Description</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {workouts.map((workout, index) => (
                    <tr key={workout.id || index}>
                      <td><strong>{workout.name || 'Workout'}</strong></td>
                      <td>
                        <span className="badge bg-info">
                          {workout.category || 'N/A'}
                        </span>
                      </td>
                      <td>
                        <span className={`badge bg-${getDifficultyBadge(workout.difficulty_level)}`}>
                          {workout.difficulty_level || 'N/A'}
                        </span>
                      </td>
                      <td>{workout.duration || 'N/A'} mins</td>
                      <td>{workout.description ? workout.description.substring(0, 50) + '...' : 'No description'}</td>
                      <td>
                        <button className="btn btn-sm btn-outline-primary me-1">Start</button>
                        <button className="btn btn-sm btn-outline-secondary">Details</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Workouts;
