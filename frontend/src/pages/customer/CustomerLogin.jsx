import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import {
  Sprout,
  User,
  Lock,
  Eye,
  EyeOff,
  AlertCircle,
  ArrowLeft,
  ShieldCheck,
  Award,
  Leaf,
  Clock,
  Sparkles
} from 'lucide-react';

export const CustomerLogin = () => {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  // Retrieve intended destination (e.g. /checkout)
  const from = location.state?.from?.pathname || location.state?.from || '/';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    try {
      await login(identifier, password);
      toast.success('Welcome back to FarmApp! Login successful.');
      navigate(from, { replace: true });
    } catch (err) {
      const msg =
        err.response?.data?.message ||
        err.message ||
        "The email/mobile or password doesn't match. Please try again.";
      setErrorMsg(msg);
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFillDemo = () => {
    setIdentifier('customer@farmapp.in');
    setPassword('Customer@123');
  };

  return (
    <div className="min-h-screen flex bg-slate-50 dark:bg-slate-950 font-sans">
      {/* Left Column: Agricultural Visual Storytelling (Desktop Only) */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-brand-900 via-brand-800 to-soil-900 p-12 text-white flex-col justify-between relative overflow-hidden">
        {/* Subtle background glow */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Top Logo */}
        <div className="relative z-10">
          <Link to="/" className="inline-flex items-center gap-2.5 group">
            <div className="w-11 h-11 rounded-2xl bg-white text-brand-700 flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6" />
            </div>
            <div className="flex flex-col">
              <span className="text-2xl font-black tracking-tight text-white">
                Farm<span className="text-brand-300">App</span>
              </span>
              <span className="text-[10px] font-semibold text-brand-200 tracking-wider uppercase -mt-1">
                Direct from Indian Farmers
              </span>
            </div>
          </Link>
        </div>

        {/* Center Storytelling Message */}
        <div className="relative z-10 space-y-6 max-w-lg">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-800/80 border border-brand-700/60 text-brand-200 text-xs font-bold">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>Empowering 12,000+ Smallholders</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-black tracking-tight leading-tight">
            From local farms to your doorstep.
          </h1>

          <p className="text-base text-brand-100/90 leading-relaxed">
            Discover fresher produce picked at sunrise while enabling farmers to earn up to 40% higher direct payouts with zero middlemen.
          </p>

          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-brand-700/50 text-xs">
            <div className="flex items-center gap-2.5">
              <Award className="w-5 h-5 text-amber-300 shrink-0" />
              <span>100% Fair Price Realization</span>
            </div>
            <div className="flex items-center gap-2.5">
              <Clock className="w-5 h-5 text-brand-300 shrink-0" />
              <span>&lt;12 Hr Harvest to Door</span>
            </div>
          </div>
        </div>

        {/* Bottom Attribution */}
        <div className="relative z-10 text-xs text-brand-300/80">
          SIH26033 AgriTech Initiative • Smart India Hackathon
        </div>
      </div>

      {/* Right Column: Customer Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          {/* Mobile Brand Header */}
          <div className="flex items-center justify-between">
            <Link
              to="/"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-brand-600 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" /> Back to shopping
            </Link>

            <Link to="/" className="lg:hidden flex items-center gap-1.5 font-black text-slate-900 dark:text-white">
              <Sprout className="w-5 h-5 text-brand-600" /> FarmApp
            </Link>
          </div>

          {/* Form Header */}
          <div className="space-y-2">
            <h2 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight">
              Welcome back
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
              Sign in to manage your fresh produce orders and checkout seamlessly.
            </p>
          </div>

          {/* Error Message Box */}
          {errorMsg && (
            <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 dark:bg-rose-950/60 dark:border-rose-800 dark:text-rose-200 text-xs flex items-start gap-3 animate-fadeIn">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Identifier Input */}
            <div className="space-y-1.5">
              <label
                htmlFor="identifier"
                className="block text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300"
              >
                Email, Mobile, or Username
              </label>
              <div className="relative">
                <input
                  id="identifier"
                  type="text"
                  required
                  placeholder="e.g. customer@farmapp.in or 9876543210"
                  value={identifier}
                  onChange={(e) => setIdentifier(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl text-sm text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all shadow-sm"
                />
                <User className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
            </div>

            {/* Password Input */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label
                  htmlFor="password"
                  className="block text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300"
                >
                  Password
                </label>
                <Link
                  to="/forgot-password"
                  className="text-xs font-semibold text-brand-600 hover:text-brand-700 transition-colors"
                >
                  Forgot password?
                </Link>
              </div>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-11 pr-11 py-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl text-sm text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all shadow-sm"
                />
                <Lock className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none" />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="p-1 rounded-lg text-slate-400 hover:text-slate-600 absolute right-3 top-1/2 -translate-y-1/2"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-2xl bg-brand-600 hover:bg-brand-700 active:scale-98 disabled:opacity-60 text-white font-bold text-sm shadow-xl shadow-brand-600/25 flex items-center justify-center gap-2 transition-all mt-2"
            >
              {loading ? (
                <span>Signing in...</span>
              ) : (
                <span>Sign In to FarmApp</span>
              )}
            </button>
          </form>

          {/* Demo Quick-Fill Pill */}
          <div className="p-3 rounded-2xl bg-brand-50/80 dark:bg-brand-950/40 border border-brand-200/70 dark:border-brand-900/60 flex items-center justify-between text-xs">
            <span className="text-brand-900 dark:text-brand-200 font-medium">
              Demo Customer: <code className="font-mono font-bold">customer@farmapp.in</code>
            </span>
            <button
              type="button"
              onClick={handleQuickFillDemo}
              className="px-2.5 py-1 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-[11px] shadow-sm transition-all"
            >
              Quick Fill
            </button>
          </div>

          {/* Registration Prompt */}
          <div className="pt-4 border-t border-slate-200/80 dark:border-slate-800 text-center text-xs text-slate-500">
            <span>New to FarmApp? </span>
            <Link
              to="/register"
              state={{ from }}
              className="font-bold text-brand-600 hover:text-brand-700 transition-colors"
            >
              Create customer account
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
