import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../api/authApi';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user_info');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('access_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const checkAuth = async () => {
      const storedToken = localStorage.getItem('access_token');
      if (storedToken) {
        try {
          const res = await authApi.getMe();
          if (isMounted && res.success && res.data) {
            setUser(res.data);
            localStorage.setItem('user_info', JSON.stringify(res.data));
          }
        } catch (e) {
          if (isMounted) {
            // Token invalid or expired - gracefully reset to guest mode
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_info');
            setToken(null);
            setUser(null);
          }
        }
      } else {
        if (isMounted) {
          setUser(null);
        }
      }
      if (isMounted) {
        setLoading(false);
      }
    };
    checkAuth();

    return () => {
      isMounted = false;
    };
  }, []);

  const login = async (identifier, password) => {
    const res = await authApi.login(identifier, password);
    if (res.success && res.data) {
      const { access_token, user: userData } = res.data;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_info', JSON.stringify(userData));
      setToken(access_token);
      setUser(userData);
      return userData;
    }
    throw new Error(res.message || 'Login failed');
  };

  const register = async (customerData) => {
    const res = await authApi.registerCustomer(customerData);
    if (res.success && res.data) {
      const { access_token, user: userData } = res.data;
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('user_info', JSON.stringify(userData));
      setToken(access_token);
      setUser(userData);
      return userData;
    }
    throw new Error(res.message || 'Registration failed');
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } catch (e) {
      // ignore
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_info');
      setToken(null);
      setUser(null);
    }
  };

  const refreshCustomer = async () => {
    if (token) {
      try {
        const res = await authApi.getMe();
        if (res.success && res.data) {
          setUser(res.data);
          localStorage.setItem('user_info', JSON.stringify(res.data));
        }
      } catch (e) {
        logout();
      }
    }
  };

  const isCustomer = user?.role === 'CUSTOMER' || user?.role === 'ADMIN';
  const isAdmin = user?.role === 'ADMIN';
  const isManager = user?.role === 'MANAGER' || user?.role === 'ADMIN';

  return (
    <AuthContext.Provider
      value={{
        user,
        customer: isCustomer ? user : null,
        token,
        loading,
        login,
        register,
        logout,
        refreshCustomer,
        refreshUser: refreshCustomer,
        isAuthenticated: !!token && !!user,
        isCustomer,
        isAdmin,
        isManager,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
