import React, { useState } from 'react';
import api from './api';

const TestButton = () => {
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleClick = async () => {
    setError('');
    setMessage('');
    try {
      const response = await api.get('ping/');
      setMessage(JSON.stringify(response.data));
    } catch (err) {
      setError('API 요청에 실패했습니다.');
    }
  };

  return (
    <div className="test-button">
      <button type="button" onClick={handleClick}>
        /api/ping 테스트
      </button>
      {message && <pre className="success-message">{message}</pre>}
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default TestButton;
