import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import MainPage from './pages/MainPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ResultsPage from './pages/ResultsPage';
import { useAuth } from './context/AuthContext';

const App = () => {
  const { user, logout } = useAuth();
  const themeClass = user ? (user.team === 'AI' ? 'theme-ai' : 'theme-human') : 'theme-neutral';

  return (
    <div className={`app-container ${themeClass}`}>
      <header className="app-header">
        <h1>AI vs Human</h1>
        <nav>
          <Link to="/">Main</Link>
          <Link to="/results">Weekly Results</Link>
          {user ? (
            <>
              <span className="welcome">
                Welcome, {user.username}
                <span className={`team-badge ${user.team === 'AI' ? 'badge-ai' : 'badge-human'}`}>
                  TEAM {user.team}
                </span>
              </span>
              <button type="button" onClick={logout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
