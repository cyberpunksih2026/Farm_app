import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Sprout } from 'lucide-react';

export const CustomerProtectedRoute = ({ children }) => {
  const { isAuthenticated, isCustomer, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-950 p-4">
        <div className="flex flex-col items-center gap-4 text-center">
          <div className="w-14 h-14 rounded-2xl bg-brand-600 text-white flex items-center justify-center shadow-lg shadow-brand-600/30 animate-pulse">
            <Sprout className="w-8 h-8" />
          </div>
          <div className="space-y-1">
            <div className="text-sm font-bold text-slate-800 dark:text-slate-200">
              Verifying FarmApp Session...
            </div>
            <div className="text-xs text-slate-400">
              Connecting directly to fresh farm supply chain
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!isAuthenticated || !isCustomer) {
    // Preserve target location so user seamlessly returns to /checkout or their desired page
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};
