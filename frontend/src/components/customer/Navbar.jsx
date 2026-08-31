import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import {
  Sprout,
  Search,
  ShoppingCart,
  MapPin,
  User as UserIcon,
  LogOut,
  ChevronDown,
  Menu,
  X,
  ShieldCheck,
  Package,
  Leaf
} from 'lucide-react';

export const Navbar = ({ searchQuery = '', onSearchChange, onSearchSubmit }) => {
  const { user, isAuthenticated, logout } = useAuth();
  const { itemCount, subtotal } = useCart();
  const navigate = useNavigate();

  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [locationModalOpen, setLocationModalOpen] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState('New Delhi (110001)');

  const handleLogout = async () => {
    await logout();
    setUserMenuOpen(false);
    navigate('/');
  };

  const handleSearchKeyPress = (e) => {
    if (e.key === 'Enter' && onSearchSubmit) {
      onSearchSubmit(searchQuery);
    }
  };

  return (
    <>
      {/* Sticky Top Header */}
      <header className="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200/80 dark:border-slate-800 transition-colors">
        {/* Top Mini Notice Bar */}
        <div className="bg-brand-900 text-white text-[11px] font-medium py-1 px-4 text-center tracking-wide flex items-center justify-center gap-2">
          <span className="flex items-center gap-1">
            <Leaf className="w-3.5 h-3.5 text-brand-300 inline" />
            100% Direct Farmer Sourcing • Harvested at Dawn • Delivered in &lt;12 Hours
          </span>
          <span className="hidden sm:inline text-brand-300">|</span>
          <span className="hidden sm:inline text-brand-200">
            Free express delivery on orders over ₹299
          </span>
        </div>

        {/* Main Navbar */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
          {/* Logo & Location */}
          <div className="flex items-center gap-6">
            <Link to="/" className="flex items-center gap-2.5 group">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white shadow-md shadow-brand-600/20 group-hover:scale-105 transition-transform">
                <Sprout className="w-6 h-6" />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-1">
                  <span className="text-2xl font-black tracking-tight text-slate-900 dark:text-white">
                    Farm<span className="text-brand-600">App</span>
                  </span>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-md bg-brand-100 text-brand-800 dark:bg-brand-950 dark:text-brand-300">
                    Direct
                  </span>
                </div>
                <span className="text-[10px] font-semibold text-slate-400 dark:text-slate-500 -mt-1 tracking-wider uppercase">
                  Farmer to Consumer
                </span>
              </div>
            </Link>

            {/* Delivery Location Selector */}
            <button
              onClick={() => setLocationModalOpen(true)}
              className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-50 hover:bg-slate-100 dark:bg-slate-800/80 dark:hover:bg-slate-800 border border-slate-200/80 dark:border-slate-700/60 text-left transition-colors"
            >
              <MapPin className="w-4 h-4 text-brand-600 shrink-0" />
              <div className="text-xs">
                <div className="text-[10px] text-slate-400 font-medium leading-none">Deliver to</div>
                <div className="font-bold text-slate-800 dark:text-slate-200 truncate max-w-[140px] leading-tight">
                  {selectedLocation}
                </div>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400 ml-1" />
            </button>
          </div>

          {/* Search Bar */}
          <div className="flex-1 max-w-xl hidden lg:block">
            <div className="relative">
              <input
                type="text"
                placeholder="Search fresh vegetables, fruits, grains, pulses..."
                value={searchQuery}
                onChange={(e) => onSearchChange && onSearchChange(e.target.value)}
                onKeyDown={handleSearchKeyPress}
                className="w-full pl-11 pr-4 py-2.5 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-2xl text-sm text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 transition-all shadow-inner"
              />
              <Search className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              {searchQuery && (
                <button
                  onClick={() => onSearchChange && onSearchChange('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs font-semibold text-slate-400 hover:text-slate-600 px-1.5 py-0.5 rounded-full"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          {/* Right Action Icons & Auth */}
          <div className="flex items-center gap-3">
            {/* Direct Cart Button */}
            <Link
              to="/cart"
              className="flex items-center gap-2.5 px-4 py-2 rounded-2xl bg-brand-50 hover:bg-brand-100/80 dark:bg-brand-950/40 dark:hover:bg-brand-900/60 border border-brand-200/80 dark:border-brand-900/60 text-brand-900 dark:text-brand-100 transition-all group"
            >
              <div className="relative">
                <ShoppingCart className="w-5 h-5 text-brand-600 group-hover:scale-110 transition-transform" />
                {itemCount > 0 && (
                  <span className="absolute -top-2 -right-2 w-5 h-5 rounded-full bg-brand-600 text-white text-[11px] font-bold flex items-center justify-center ring-2 ring-white dark:ring-slate-900 shadow-sm animate-bounce">
                    {itemCount}
                  </span>
                )}
              </div>
              <div className="hidden sm:flex flex-col text-left">
                <span className="text-[10px] uppercase font-bold text-brand-700 dark:text-brand-400 leading-none">
                  Cart
                </span>
                <span className="text-xs font-extrabold text-slate-900 dark:text-white leading-tight">
                  ₹{subtotal}
                </span>
              </div>
            </Link>

            {/* Dynamic Customer Auth State */}
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="flex items-center gap-2 p-1.5 sm:px-3 sm:py-2 rounded-2xl bg-slate-100 hover:bg-slate-200/70 dark:bg-slate-800 dark:hover:bg-slate-700/80 border border-slate-200 dark:border-slate-700 transition-all"
                >
                  <div className="w-8 h-8 rounded-xl bg-brand-600 text-white flex items-center justify-center font-bold text-xs shadow-sm">
                    {user?.full_name?.charAt(0) || 'C'}
                  </div>
                  <div className="hidden sm:block text-left">
                    <div className="text-xs font-bold text-slate-900 dark:text-white truncate max-w-[110px]">
                      {user?.full_name || 'Customer'}
                    </div>
                    <div className="text-[10px] font-semibold text-brand-600 dark:text-brand-400 uppercase">
                      {user?.role || 'Customer'}
                    </div>
                  </div>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400 hidden sm:block" />
                </button>

                {/* Customer Dropdown */}
                {userMenuOpen && (
                  <>
                    <div
                      className="fixed inset-0 z-40"
                      onClick={() => setUserMenuOpen(false)}
                    />
                    <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-slate-900 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 py-2 z-50 animate-fadeIn">
                      <div className="px-4 py-2 border-b border-slate-100 dark:border-slate-800">
                        <div className="text-xs font-bold text-slate-900 dark:text-white truncate">
                          {user?.full_name}
                        </div>
                        <div className="text-[11px] text-slate-400 truncate">
                          {user?.email || user?.username}
                        </div>
                      </div>

                      <Link
                        to="/checkout"
                        onClick={() => setUserMenuOpen(false)}
                        className="flex items-center gap-2.5 px-4 py-2.5 text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
                      >
                        <Package className="w-4 h-4 text-slate-400" />
                        My Orders &amp; Checkout
                      </Link>

                      <div className="border-t border-slate-100 dark:border-slate-800 my-1" />

                      <button
                        onClick={handleLogout}
                        className="w-full flex items-center gap-2.5 px-4 py-2.5 text-xs font-semibold text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 text-left transition-colors"
                      >
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  </>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-2xl bg-brand-600 hover:bg-brand-700 text-white text-xs font-bold shadow-md shadow-brand-600/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="hidden md:inline-flex px-3.5 py-2 rounded-2xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-semibold transition-colors"
                >
                  Register
                </Link>
              </div>
            )}

            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-xl text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Search Bar & Menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden px-4 pb-4 pt-2 border-t border-slate-200 dark:border-slate-800 space-y-3 bg-white dark:bg-slate-900">
            <div className="relative">
              <input
                type="text"
                placeholder="Search produce..."
                value={searchQuery}
                onChange={(e) => onSearchChange && onSearchChange(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-xs"
              />
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                onClick={() => {
                  setLocationModalOpen(true);
                  setMobileMenuOpen(false);
                }}
                className="flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-300"
              >
                <MapPin className="w-4 h-4 text-brand-600" />
                <span>{selectedLocation}</span>
              </button>

              {!isAuthenticated && (
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-xs font-bold text-brand-600"
                >
                  Create an Account
                </Link>
              )}
            </div>
          </div>
        )}
      </header>

      {/* Location Selector Modal */}
      {locationModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl max-w-sm w-full p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 font-bold text-slate-900 dark:text-white">
                <MapPin className="w-5 h-5 text-brand-600" />
                Select Delivery Location
              </div>
              <button
                onClick={() => setLocationModalOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-500">
              FarmApp currently delivers fresh farm harvests across major metropolitan clusters.
            </p>

            <div className="space-y-2">
              {[
                'New Delhi (110001) — Express 6hr Sourcing',
                'Gurugram (122001) — Cold-Chain Active',
                'Noida (201301) — FPO Direct Hub',
                'Bengaluru (560001) — Karnataka Sourcing Hub',
                'Mumbai (400001) — Sahyadri Express Route',
                'Pune (411001) — Maharashtra Cluster',
              ].map((loc) => (
                <button
                  key={loc}
                  onClick={() => {
                    setSelectedLocation(loc.split(' — ')[0]);
                    setLocationModalOpen(false);
                  }}
                  className={`w-full text-left p-3 rounded-xl text-xs font-medium transition-all ${
                    selectedLocation.includes(loc.split(' — ')[0])
                      ? 'bg-brand-50 border border-brand-500 text-brand-900 font-bold'
                      : 'bg-slate-50 hover:bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
                  }`}
                >
                  {loc}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
};
