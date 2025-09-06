import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [users, setUsers] = useState([]);
  const [posts, setPosts] = useState([]);
  const [communities, setCommunities] = useState([]);
  const [influence, setInfluence] = useState({});
  const [linkPredictions, setLinkPredictions] = useState([]);
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    fetchUsers();
    fetchPosts();
    fetchCommunities();
    fetchInfluence();
    fetchLinkPredictions();
    fetchAnomalies();
  }, []);

  const fetchUsers = async () => {
    const res = await axios.get('http://localhost:5000/users');
    setUsers(res.data);
  };

  const fetchPosts = async () => {
    const res = await axios.get('http://localhost:5000/posts');
    setPosts(res.data);
  };

  const fetchCommunities = async () => {
    const res = await axios.get('http://localhost:5000/communities/detect');
    setCommunities(res.data);
  };

  const fetchInfluence = async () => {
    const res = await axios.get('http://localhost:5000/influence/analyze');
    setInfluence(res.data);
  };

  const fetchLinkPredictions = async () => {
    const res = await axios.get('http://localhost:5000/links/predict');
    setLinkPredictions(res.data);
  };

  const fetchAnomalies = async () => {
    const res = await axios.get('http://localhost:5000/anomalies/detect');
    setAnomalies(res.data);
  };

  return (
    <div className="p-4 font-sans">
      <h1 className="text-3xl font-bold mb-4">Social Media Analytics Dashboard</h1>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Users</h2>
        <ul className="list-disc pl-5">
          {users.map(u => (
            <li key={u.UserID}>{u.Name} ({u.Email})</li>
          ))}
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Posts</h2>
        <ul className="list-disc pl-5 max-h-40 overflow-auto border p-2">
          {posts.map(p => (
            <li key={p.PostID}>
              User {p.UserID}: {p.Content} (Sentiment: {p.SentimentScore.toFixed(2)})
            </li>
          ))}
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Communities Detected</h2>
        {communities.map(c => (
          <div key={c.CommunityID} className="mb-2 p-2 border rounded">
            <strong>Community {c.CommunityID}</strong>: Members {c.Members.join(', ')}
          </div>
        ))}
      </section>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Influence Scores (PageRank)</h2>
        <ul className="list-disc pl-5 max-h-40 overflow-auto border p-2">
          {Object.entries(influence).map(([user, score]) => (
            <li key={user}>User  {user}: {score.toFixed(3)}</li>
          ))}
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Link Predictions</h2>
        <ul className="list-disc pl-5 max-h-40 overflow-auto border p-2">
          {linkPredictions.map((lp, idx) => (
            <li key={idx}>
              User {lp.User1ID} &amp; User {lp.User2ID} - Score: {lp.PredictionScore.toFixed(3)}
            </li>
          ))}
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Anomalies Detected</h2>
        <ul className="list-disc pl-5 max-h-40 overflow-auto border p-2">
          {anomalies.map((a, idx) => (
            <li key={idx}>
              User {a.UserID} - {a.ActivityType} (Score: {a.Score})
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default App;