import React, { useEffect, useState } from 'react';
import SubmissionCard from '../components/SubmissionCard';
import { createSubmission, fetchSubmissions } from '../services/api';
import { useAuth } from '../context/AuthContext';

const categories = [
  { value: 'IMAGE', label: 'Image' },
  { value: 'NOVEL', label: 'Novel' },
  { value: 'POETRY', label: 'Poetry' },
  { value: 'VIDEO', label: 'Video' },
  { value: 'MUSIC', label: 'Music' }
];

const identities = [
  { value: 'AI', label: 'AI' },
  { value: 'HUMAN', label: 'Human' }
];

const MainPage = () => {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'IMAGE',
    content_text: '',
    true_identity: 'AI'
  });
  const [error, setError] = useState('');
  const { user } = useAuth();

  const loadSubmissions = async () => {
    setLoading(true);
    try {
      const data = await fetchSubmissions();
      setSubmissions(data);
    } catch (err) {
      setError('Failed to load submissions.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSubmissions();
  }, []);

  const handleChange = (event) => {
    const { name, value, files } = event.target;
    if (files) {
      setFormData((prev) => ({ ...prev, [name]: files[0] }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      setError('');
      const payload = new FormData();
      Object.entries(formData).forEach(([key, value]) => {
        if (value) {
          payload.append(key, value);
        }
      });
      await createSubmission(payload);
      setFormData({
        title: '',
        description: '',
        category: 'IMAGE',
        content_text: '',
        true_identity: 'AI'
      });
      loadSubmissions();
    } catch (err) {
      setError('Failed to upload submission.');
    }
  };

  return (
    <section className="main-page">
      <h2>Featured Submissions</h2>
      {error && <p className="error">{error}</p>}
      {loading ? <p>Loading...</p> : submissions.map((submission) => (
        <SubmissionCard key={submission.id} submission={submission} onVoted={loadSubmissions} />
      ))}

      {user && (
        <form className="submission-form" onSubmit={handleSubmit}>
          <h3>Upload Your Submission</h3>
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />

          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
          />

          <label htmlFor="category">Category</label>
          <select id="category" name="category" value={formData.category} onChange={handleChange}>
            {categories.map((category) => (
              <option key={category.value} value={category.value}>
                {category.label}
              </option>
            ))}
          </select>

          <label htmlFor="content_text">Text Content</label>
          <textarea
            id="content_text"
            name="content_text"
            value={formData.content_text}
            onChange={handleChange}
          />

          <label htmlFor="content_file">Upload File</label>
          <input id="content_file" name="content_file" type="file" onChange={handleChange} />

          <label htmlFor="true_identity">Actual Identity</label>
          <select
            id="true_identity"
            name="true_identity"
            value={formData.true_identity}
            onChange={handleChange}
          >
            {identities.map((identity) => (
              <option key={identity.value} value={identity.value}>
                {identity.label}
              </option>
            ))}
          </select>

          <button type="submit">Submit</button>
        </form>
      )}
    </section>
  );
};

export default MainPage;
