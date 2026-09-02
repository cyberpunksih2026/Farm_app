import React from 'react';
import { Link } from 'react-router-dom';
import { Sprout, ShieldCheck, Heart, Leaf, MapPin, Phone, Mail, Award } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-soil-50 dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400">
      {/* Top Value Strip */}
      <div className="border-b border-slate-200/80 dark:border-slate-800 py-8 bg-white/60 dark:bg-slate-900/40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="flex items-center gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-brand-100 dark:bg-brand-950 text-brand-700 dark:text-brand-300 flex items-center justify-center shrink-0">
                <Sprout className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                  Direct FPO Sourcing
                </h4>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  100% farm-origin traceability to registered producer clusters
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300 flex items-center justify-center shrink-0">
                <Award className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                  Fair Price Realization
                </h4>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  Up to 40% higher earnings paid directly to farming families
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 flex items-center justify-center shrink-0">
                <Leaf className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                  Zero Chemical Coating
                </h4>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  Naturally harvested produce with zero wax or artificial ripeners
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3.5">
              <div className="w-10 h-10 rounded-2xl bg-purple-100 dark:bg-purple-950 text-purple-700 dark:text-purple-300 flex items-center justify-center shrink-0">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                  Quality Guaranteed
                </h4>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  No questions asked instant refund if you aren't delighted
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Footer Links */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <Link to="/" className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-2xl bg-brand-600 flex items-center justify-center text-white shadow-md shadow-brand-600/20">
                <Sprout className="w-5 h-5" />
              </div>
              <span className="text-2xl font-black tracking-tight text-slate-900 dark:text-white">
                Farm<span className="text-brand-600">App</span>
              </span>
            </Link>
            <p className="text-xs text-slate-500 leading-relaxed max-w-sm">
              FarmApp is India's next-generation digital agricultural supply chain platform developed for SIH26033. Connecting smallholder farmer producer organizations directly with conscious urban consumers.
            </p>
            <div className="pt-2 text-xs text-slate-500 space-y-1.5">
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-brand-600 shrink-0" />
                <span>Regional Sourcing Hubs: Nashik, Solan, Latur, Karnal</span>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-brand-600 shrink-0" />
                <span>support@farmapp.in • sih26033@farmapp.in</span>
              </div>
            </div>
          </div>

          {/* Quick Categories */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white mb-3">
              Fresh Categories
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/" className="hover:text-brand-600 transition-colors">
                  Daily Farm Vegetables
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-brand-600 transition-colors">
                  Orchard Fresh Fruits
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-brand-600 transition-colors">
                  Hydroponic Greens
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-brand-600 transition-colors">
                  Unpolished Dals &amp; Rice
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-brand-600 transition-colors">
                  Organic Lakadong Turmeric
                </Link>
              </li>
            </ul>
          </div>

          {/* Customer & Transparency */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white mb-3">
              Transparency &amp; Trust
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/" className="hover:text-brand-600 transition-colors">
                  Price Transparency Model
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-brand-600 transition-colors">
                  FPO Sourcing Standards
                </Link>
              </li>
              <li>
                <Link to="/cart" className="hover:text-brand-600 transition-colors">
                  Customer Cart
                </Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-brand-600 transition-colors">
                  Customer Sign In
                </Link>
              </li>
              <li>
                <Link to="/register" className="hover:text-brand-600 transition-colors">
                  Create Customer Account
                </Link>
              </li>
            </ul>
          </div>

          {/* FPO & Agriculture */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-white mb-3">
              FPO &amp; Ecosystem
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <span className="text-slate-400">Farmer Portal (Future)</span>
              </li>
              <li>
                <span className="text-slate-400">Logistics Fleet (Future)</span>
              </li>
              <li>
                <span className="text-slate-400">Demand Forecasting AI</span>
              </li>
              <li>
                <span className="text-slate-400">Admin Control Desk</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 mt-8 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-400">
          <div>
            © {new Date().getFullYear()} FarmApp Technologies. Developed for Smart India Hackathon (SIH26033).
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1 text-slate-500">
              Built with <Heart className="w-3 h-3 text-rose-500 fill-rose-500" /> for Indian Farmers
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
