import React, { useState } from 'react';
import { voteSubmission } from '../services/api';
import { useAuth } from '../context/AuthContext';

const SubmissionCard = ({ submission, onVoted }) => {
  const [guess, setGuess] = useState('AI');
  const [error, setError] = useState('');
  const { user } = useAuth();

  const handleVote = async () => {
    try {
      setError('');
      await voteSubmission(submission.id, { guess });
      if (onVoted) {
        onVoted();
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit vote.');
    }
  };

  return (
    <div className="submission-card">
      <h3>{submission.title}</h3>
      <p className="category">Category: {submission.category}</p>
      <p>{submission.description}</p>
      {submission.content_text && <pre className="content-text">{submission.content_text}</pre>}
      {submission.true_identity && user && user.id === submission.author.id && (
        <p className="identity">Actual Identity: {submission.true_identity}</p>
      )}
      <div className="vote-section">
        <label htmlFor={`guess-${submission.id}`}>Your guess:</label>
        <select
          id={`guess-${submission.id}`}
          value={guess}
          onChange={(event) => setGuess(event.target.value)}
        >
          <option value="AI">AI</option>
          <option value="HUMAN">Human</option>
        </select>
        <button type="button" onClick={handleVote} disabled={!user}>
          Submit Vote
        </button>
      </div>
      {error && <p className="error">{error}</p>}
      <p className="votes">Votes: {submission.votes_count}</p>
    </div>
  );
};

export default SubmissionCard;
