import React, { createContext, useContext, useEffect, useState } from 'react';
import {
  fetchCurrentUser,
  loginRequest,
  logoutRequest,
  registerRequest
} from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const bootstrap = async () => {
      try {
        const profile = await fetchCurrentUser();
        setUser(profile);
      } catch (error) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    bootstrap();
  }, []);

  const login = async (credentials) => {
    const data = await loginRequest(credentials);
    setUser(data.user);
    return data.user;
  };

  const register = async (payload) => {
    await registerRequest(payload);
    return login({ username: payload.username, password: payload.password });
  };

  const logout = async () => {
    await logoutRequest();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
