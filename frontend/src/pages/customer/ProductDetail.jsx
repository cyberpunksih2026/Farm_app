import React, { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getProductById, PRODUCTS } from '../../data/products';
import { useCart } from '../../context/CartContext';
import { Navbar } from '../../components/customer/Navbar';
import { Footer } from '../../components/customer/Footer';
import { PriceTransparencyModal } from '../../components/customer/PriceTransparencyModal';
import {
  ArrowLeft,
  ShieldCheck,
  Sparkles,
  MapPin,
  Clock,
  Plus,
  Minus,
  Check,
  ShoppingCart,
  Award,
  Leaf,
  Info
} from 'lucide-react';

export const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const product = getProductById(id) || PRODUCTS[0];
  const { getItemQuantity, addItem, updateQuantity } = useCart();
  const [transparencyOpen, setTransparencyOpen] = useState(false);
  const [addedAnimation, setAddedAnimation] = useState(false);

  const quantity = getItemQuantity(product.id);
  const discountPercent = Math.round(((product.marketPrice - product.price) / product.marketPrice) * 100);

  const handleAdd = () => {
    addItem(product, 1);
    setAddedAnimation(true);
    setTimeout(() => setAddedAnimation(false), 1200);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/50 dark:bg-slate-950 font-sans">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
        {/* Breadcrumbs & Back */}
        <div className="flex items-center gap-2 text-xs text-slate-500 mb-6">
          <Link to="/" className="flex items-center gap-1 hover:text-brand-600 transition-colors">
            <ArrowLeft className="w-3.5 h-3.5" /> Back to Fresh Marketplace
          </Link>
          <span>/</span>
          <span className="capitalize">{product.categoryName}</span>
          <span>/</span>
          <span className="font-semibold text-slate-900 dark:text-white truncate max-w-xs">
            {product.name}
          </span>
        </div>

        {/* Main Product Card Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 sm:p-8 shadow-sm">
          {/* Left Column: Image */}
          <div className="lg:col-span-5 space-y-4">
            <div className="relative aspect-square rounded-3xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-100 dark:border-slate-800">
              <img
                src={product.image}
                alt={product.name}
                className="w-full h-full object-cover object-center"
              />

              {product.freshnessTag && (
                <div className="absolute top-4 left-4 px-3 py-1 rounded-xl bg-slate-950/80 backdrop-blur-md text-white text-xs font-bold flex items-center gap-1.5 shadow-md">
                  <Sparkles className="w-3.5 h-3.5 text-amber-400" />
                  <span>{product.freshnessTag}</span>
                </div>
              )}

              {product.organicCertified && (
                <div className="absolute top-4 right-4 px-3 py-1 rounded-xl bg-brand-600 text-white text-xs font-bold uppercase tracking-wider shadow-md">
                  100% Organic
                </div>
              )}
            </div>

            {/* FPO Origin Assurance Card */}
            <div className="p-4 rounded-2xl bg-brand-50/70 dark:bg-brand-950/40 border border-brand-200/80 dark:border-brand-900/60 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-brand-900 dark:text-brand-200">
                <ShieldCheck className="w-4 h-4 text-brand-600" />
                <span>Verified Direct FPO Origin</span>
              </div>
              <p className="text-xs text-brand-800 dark:text-brand-300 leading-relaxed">
                Directly harvested by <span className="font-bold">{product.farmerLead || 'Farmer Group'}</span> from <span className="font-bold">{product.fpoName}</span>, located in {product.fpoLocation}.
              </p>
            </div>
          </div>

          {/* Right Column: Information & Pricing */}
          <div className="lg:col-span-7 space-y-6">
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-xs text-brand-600 font-bold uppercase tracking-wider">
                <MapPin className="w-3.5 h-3.5" />
                <span>{product.fpoName} • {product.fpoLocation}</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight">
                {product.name}
              </h1>
              <p className="text-sm text-slate-500 font-medium">
                Unit size: <span className="font-bold text-slate-800 dark:text-slate-200">{product.unit}</span>
              </p>
            </div>

            {/* Price Box with Transparency */}
            <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-3">
              <div className="flex items-baseline gap-3">
                <span className="text-3xl font-black text-slate-900 dark:text-white">
                  ₹{product.price}
                </span>
                {product.marketPrice > product.price && (
                  <span className="text-base text-slate-400 line-through">
                    ₹{product.marketPrice}
                  </span>
                )}
                {discountPercent > 0 && (
                  <span className="px-2.5 py-0.5 rounded-lg bg-brand-100 text-brand-800 dark:bg-brand-950 dark:text-brand-300 text-xs font-bold uppercase">
                    Save {discountPercent}% vs Mandi
                  </span>
                )}
              </div>

              {/* Transparency Banner */}
              <div className="flex items-center justify-between p-3 rounded-xl bg-white dark:bg-slate-900 border border-brand-200 dark:border-brand-900/60 text-xs">
                <div className="flex items-center gap-2 font-semibold text-brand-900 dark:text-brand-200">
                  <Award className="w-4 h-4 text-brand-600" />
                  <span>₹{product.farmerPrice} paid directly to the farmer</span>
                </div>
                <button
                  onClick={() => setTransparencyOpen(true)}
                  className="text-xs font-bold text-brand-600 hover:text-brand-700 underline flex items-center gap-1"
                >
                  <Info className="w-3.5 h-3.5" /> Price Breakdown
                </button>
              </div>
            </div>

            {/* Description */}
            <div className="space-y-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Produce Story &amp; Details
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                {product.description}
              </p>
            </div>

            {/* Highlights */}
            {product.highlights && (
              <div className="space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Quality Assurance
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {product.highlights.map((item, idx) => (
                    <div key={idx} className="flex items-center gap-2 text-xs text-slate-700 dark:text-slate-300">
                      <Check className="w-4 h-4 text-brand-600 shrink-0" />
                      <span>{item}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Nutritional Info */}
            {product.nutrition && (
              <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                  Nutritional Highlights (Per 100g)
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {Object.entries(product.nutrition).map(([key, value]) => (
                    <div key={key} className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 text-center">
                      <div className="text-[10px] uppercase font-bold text-slate-400">{key}</div>
                      <div className="text-xs font-extrabold text-slate-900 dark:text-white mt-0.5">{value}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Actions: Add to Cart / Quantity Selector */}
            <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center gap-4">
              {quantity === 0 ? (
                <button
                  onClick={handleAdd}
                  className="w-full sm:w-auto flex-1 px-8 py-3.5 rounded-2xl bg-brand-600 hover:bg-brand-700 active:scale-98 text-white font-bold text-sm shadow-xl shadow-brand-600/25 flex items-center justify-center gap-2 transition-all"
                >
                  <Plus className="w-4 h-4" />
                  Add to Cart • ₹{product.price}
                </button>
              ) : (
                <div className="flex items-center gap-3 w-full sm:w-auto">
                  <div className="flex items-center gap-2 bg-brand-50 dark:bg-brand-950 border border-brand-300 dark:border-brand-800 rounded-2xl p-1.5">
                    <button
                      onClick={() => updateQuantity(product.id, quantity - 1)}
                      className="w-9 h-9 rounded-xl bg-white dark:bg-slate-800 text-brand-700 dark:text-brand-300 flex items-center justify-center font-bold hover:bg-brand-100 transition-colors shadow-sm"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="w-8 text-center text-sm font-bold text-brand-900 dark:text-brand-100">
                      {quantity}
                    </span>
                    <button
                      onClick={() => updateQuantity(product.id, quantity + 1)}
                      className="w-9 h-9 rounded-xl bg-brand-600 text-white flex items-center justify-center font-bold hover:bg-brand-700 transition-colors shadow-sm"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                  <Link
                    to="/cart"
                    className="flex-1 px-6 py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center justify-center gap-2 transition-colors"
                  >
                    <ShoppingCart className="w-4 h-4" /> View Cart
                  </Link>
                </div>
              )}

              <Link
                to="/cart"
                className="w-full sm:w-auto px-6 py-3.5 rounded-2xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold text-xs text-center transition-colors"
              >
                Go to Cart
              </Link>
            </div>
          </div>
        </div>
      </main>

      <Footer />

      <PriceTransparencyModal
        product={product}
        isOpen={transparencyOpen}
        onClose={() => setTransparencyOpen(false)}
      />
    </div>
  );
};
