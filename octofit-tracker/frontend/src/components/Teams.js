import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = codespace
        ? `https://${codespace}-8000.app.github.dev/api/teams/`
        : 'http://localhost:8000/api/teams/';
      
      console.log('Fetching teams from:', apiUrl);
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Teams data received:', data);
      
      // Handle both paginated (.results) and plain array responses
      const teamsData = data.results || data;
      setTeams(Array.isArray(teamsData) ? teamsData : []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching teams:', err);
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
          <h1>🏆 Teams</h1>
          <p className="mb-0">Compete and collaborate with your team</p>
        </div>
      </div>
      
      <div className="container">
        {teams.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">👥</div>
            <h3>No Teams Yet</h3>
            <p>Create a team to start competing!</p>
          </div>
        ) : (
          <div className="table-wrapper">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h5 className="mb-0">All Teams ({teams.length})</h5>
              <button className="btn btn-primary btn-sm">Create Team</button>
            </div>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Team Name</th>
                    <th>Description</th>
                    <th>Members</th>
                    <th>Created Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {teams.map((team, index) => (
                    <tr key={team.id || index}>
                      <td><strong>{team.name || 'Team'}</strong></td>
                      <td>{team.description || 'No description available'}</td>
                      <td>
                        <span className="badge bg-primary">
                          {team.member_count || team.members?.length || 0} members
                        </span>
                      </td>
                      <td>{team.created_at ? new Date(team.created_at).toLocaleDateString() : 'N/A'}</td>
                      <td>
                        <button className="btn btn-sm btn-outline-primary me-1">View</button>
                        <button className="btn btn-sm btn-outline-success">Join</button>
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

export default Teams;
