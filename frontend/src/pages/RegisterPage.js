import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    password2: '',
    team: 'AI'
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { register } = useAuth();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (formData.password !== formData.password2) {
      setError("Passwords don't match.");
      return;
    }
    try {
      setError('');
      await register(formData);
      navigate('/');
    } catch (err) {
      const detail = err.response?.data;
      if (typeof detail === 'object') {
        setError(Object.values(detail).flat().join(' '));
      } else {
        setError('Registration failed.');
      }
    }
  };

  return (
    <section className="auth-page">
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <label htmlFor="password2">Confirm Password</label>
        <input
          id="password2"
          name="password2"
          type="password"
          value={formData.password2}
          onChange={handleChange}
          required
        />

        <label htmlFor="team">Select Team</label>
        <select id="team" name="team" value={formData.team} onChange={handleChange}>
          <option value="AI">TEAM AI</option>
          <option value="HUMAN">TEAM HUMAN</option>
        </select>

        <button type="submit">Create Account</button>
      </form>
    </section>
  );
};

export default RegisterPage;
