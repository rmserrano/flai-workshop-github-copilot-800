import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = codespace
        ? `https://${codespace}-8000.app.github.dev/api/leaderboard/`
        : 'http://localhost:8000/api/leaderboard/';
      
      console.log('Fetching leaderboard from:', apiUrl);
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Leaderboard data received:', data);
      
      // Handle both paginated (.results) and plain array responses
      const leaderboardData = data.results || data;
      setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching leaderboard:', err);
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

  // Medal emojis for top 3
  const getMedal = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  return (
    <div className="container-fluid mt-4">
      <div className="page-header">
        <div className="container">
          <h1>🏅 Leaderboard</h1>
          <p className="mb-0">Top performers and team rankings</p>
        </div>
      </div>
      
      <div className="container">
        {leaderboard.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">🏆</div>
            <h3>No Leaderboard Data</h3>
            <p>Start logging activities to see rankings!</p>
          </div>
        ) : (
          <div className="table-wrapper">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">Top Performers</h5>
              <button className="btn btn-primary btn-sm">Refresh Rankings</button>
            </div>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Rank</th>
                    <th>User</th>
                    <th>Team</th>
                    <th>Points</th>
                    <th>Activities</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry, index) => (
                    <tr key={entry.id || index} className={index < 3 ? 'table-warning' : ''}>
                      <td>
                        <strong style={{ fontSize: '1.2rem' }}>
                          {getMedal(index + 1)}
                        </strong>
                      </td>
                      <td><strong>{entry.user_name || entry.user || 'N/A'}</strong></td>
                      <td>
                        <span className="badge bg-success">
                          {entry.team_name || entry.team || 'N/A'}
                        </span>
                      </td>
                      <td>
                        <span className="badge bg-primary">
                          {entry.total_points || 0} pts
                        </span>
                      </td>
                      <td>{entry.total_activities || 0}</td>
                      <td>
                        {index < 3 ? (
                          <span className="badge bg-warning text-dark">Top 3</span>
                        ) : (
                          <span className="badge bg-secondary">Active</span>
                        )}
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

export default Leaderboard;
