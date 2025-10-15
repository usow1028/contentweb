import React, { useEffect, useState } from 'react';
import { fetchWeeklyResults } from '../services/api';

const ResultsPage = () => {
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadResults = async () => {
      try {
        const data = await fetchWeeklyResults();
        setResults(data);
      } catch (err) {
        setError('Unable to load weekly results.');
      }
    };

    loadResults();
  }, []);

  if (error) {
    return (
      <section className="results-page">
        <h2>Weekly Results</h2>
        <p className="error">{error}</p>
      </section>
    );
  }

  if (!results) {
    return (
      <section className="results-page">
        <h2>Weekly Results</h2>
        <p>Loading...</p>
      </section>
    );
  }

  return (
    <section className="results-page">
      <h2>Weekly Results</h2>
      <p>
        Week Starting: {new Date(results.current_week_start).toLocaleDateString()} (UTC)
      </p>
      <div className="result-summary">
        <p>Accurate AI Guesses: {results.accurate_ai_guesses}</p>
        <p>Accurate Human Guesses: {results.accurate_human_guesses}</p>
      </div>

      <div className="result-submissions">
        <h3>Participating Submissions</h3>
        {results.submissions.length === 0 ? (
          <p>No submissions this week.</p>
        ) : (
          <ul>
            {results.submissions.map((submission) => (
              <li key={submission.id}>
                <strong>{submission.title}</strong> — {submission.category}
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
};

export default ResultsPage;
