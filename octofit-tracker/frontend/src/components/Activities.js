import React, { useState, useEffect } from 'react';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchActivities();
  }, []);

  const fetchActivities = async () => {
    try {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = codespace
        ? `https://${codespace}-8000.app.github.dev/api/activities/`
        : 'http://localhost:8000/api/activities/';
      
      console.log('Fetching activities from:', apiUrl);
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Activities data received:', data);
      
      // Handle both paginated (.results) and plain array responses
      const activitiesData = data.results || data;
      setActivities(Array.isArray(activitiesData) ? activitiesData : []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching activities:', err);
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

  return (
    <div className="container-fluid mt-4">
      <div className="page-header">
        <div className="container">
          <h1>🏃 Activities</h1>
          <p className="mb-0">Track and monitor fitness activities</p>
        </div>
      </div>
      
      <div className="container">
        {activities.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📊</div>
            <h3>No Activities Yet</h3>
            <p>Start tracking your fitness journey!</p>
          </div>
        ) : (
          <div className="table-wrapper">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">All Activities ({activities.length})</h5>
              <button className="btn btn-primary btn-sm">Add Activity</button>
            </div>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Activity</th>
                    <th>Type</th>
                    <th>Duration</th>
                    <th>Distance</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {activities.map((activity, index) => (
                    <tr key={activity.id || index}>
                      <td><strong>{activity.name || 'Activity'}</strong></td>
                      <td>
                        <span className="badge bg-info">
                          {activity.activity_type || 'N/A'}
                        </span>
                      </td>
                      <td>{activity.duration || 'N/A'} mins</td>
                      <td>{activity.distance || 'N/A'} km</td>
                      <td>{activity.date ? new Date(activity.date).toLocaleDateString() : 'N/A'}</td>
                      <td>
                        <button className="btn btn-sm btn-outline-primary me-1">View</button>
                        <button className="btn btn-sm btn-outline-secondary">Edit</button>
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

export default Activities;
