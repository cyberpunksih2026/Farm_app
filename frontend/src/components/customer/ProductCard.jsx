import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { PriceTransparencyModal } from './PriceTransparencyModal';
import { Plus, Minus, Info, MapPin, Sparkles, ShieldCheck, Check } from 'lucide-react';

export const ProductCard = ({ product }) => {
  const { getItemQuantity, addItem, updateQuantity } = useCart();
  const [transparencyOpen, setTransparencyOpen] = useState(false);
  const [addedToast, setAddedToast] = useState(false);

  const quantity = getItemQuantity(product.id);
  const discountPercent = Math.round(((product.marketPrice - product.price) / product.marketPrice) * 100);

  const handleAdd = (e) => {
    e.preventDefault();
    e.stopPropagation();
    addItem(product, 1);
    setAddedToast(true);
    setTimeout(() => setAddedToast(false), 1200);
  };

  const handleIncrease = (e) => {
    e.preventDefault();
    e.stopPropagation();
    updateQuantity(product.id, quantity + 1);
  };

  const handleDecrease = (e) => {
    e.preventDefault();
    e.stopPropagation();
    updateQuantity(product.id, quantity - 1);
  };

  return (
    <>
      <div className="group bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-3.5 sm:p-4 shadow-sm hover:shadow-xl hover:border-brand-300 dark:hover:border-brand-800 transition-all duration-300 flex flex-col justify-between relative overflow-hidden">
        {/* Top Badges */}
        <div className="relative aspect-square rounded-2xl overflow-hidden bg-slate-100 dark:bg-slate-800 mb-3">
          <Link to={`/product/${product.id}`} className="block w-full h-full">
            <img
              src={product.image}
              alt={product.name}
              loading="lazy"
              className="w-full h-full object-cover object-center group-hover:scale-108 transition-transform duration-500"
            />
          </Link>

          {/* Freshness Tag Top Left */}
          {product.freshnessTag && (
            <div className="absolute top-2.5 left-2.5 px-2.5 py-1 rounded-xl bg-slate-950/75 backdrop-blur-md text-white text-[10px] font-bold tracking-wide flex items-center gap-1 shadow-sm">
              <Sparkles className="w-3 h-3 text-amber-400" />
              <span>{product.freshnessTag}</span>
            </div>
          )}

          {/* Organic Badge Top Right */}
          {product.organicCertified && (
            <div className="absolute top-2.5 right-2.5 px-2 py-0.5 rounded-lg bg-brand-600/90 backdrop-blur-md text-white text-[10px] font-extrabold uppercase tracking-wider">
              Organic
            </div>
          )}

          {/* Quick Added Indicator */}
          {addedToast && (
            <div className="absolute inset-0 bg-brand-600/80 backdrop-blur-sm flex items-center justify-center text-white font-bold text-xs gap-1.5 animate-fadeIn">
              <Check className="w-4 h-4" /> Added to Cart
            </div>
          )}
        </div>

        {/* Product Details */}
        <div className="space-y-2 flex-1">
          {/* FPO Origin Tag */}
          <div className="flex items-center gap-1 text-[11px] text-slate-500 dark:text-slate-400 font-medium truncate">
            <MapPin className="w-3 h-3 text-brand-600 shrink-0" />
            <span className="truncate">{product.fpoName} • {product.fpoLocation}</span>
          </div>

          {/* Title */}
          <Link
            to={`/product/${product.id}`}
            className="block font-bold text-sm text-slate-900 dark:text-white group-hover:text-brand-600 transition-colors line-clamp-1"
          >
            {product.name}
          </Link>

          {/* Unit */}
          <div className="text-[11px] font-medium text-slate-400 dark:text-slate-500">
            {product.unit}
          </div>

          {/* Price Transparency Badge */}
          <div className="flex items-center justify-between p-1.5 rounded-xl bg-brand-50/70 dark:bg-brand-950/40 border border-brand-100 dark:border-brand-900/40 text-[11px]">
            <div className="flex items-center gap-1 text-brand-800 dark:text-brand-300 font-semibold truncate">
              <ShieldCheck className="w-3.5 h-3.5 text-brand-600 shrink-0" />
              <span>₹{product.farmerPrice} to farmer</span>
            </div>
            <button
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                setTransparencyOpen(true);
              }}
              title="See Price Transparency Breakdown"
              className="text-brand-600 hover:text-brand-700 p-0.5"
            >
              <Info className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Pricing & Add to Cart Footer */}
        <div className="pt-3 mt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-2">
          {/* Price */}
          <div>
            <div className="flex items-baseline gap-1.5">
              <span className="text-lg font-black text-slate-900 dark:text-white">
                ₹{product.price}
              </span>
              {product.marketPrice > product.price && (
                <span className="text-xs text-slate-400 line-through">
                  ₹{product.marketPrice}
                </span>
              )}
            </div>
            {discountPercent > 0 && (
              <span className="text-[10px] font-bold text-brand-700 dark:text-brand-400 uppercase">
                Save {discountPercent}% vs Mandi
              </span>
            )}
          </div>

          {/* Add / Stepper Button */}
          {quantity === 0 ? (
            <button
              onClick={handleAdd}
              className="px-4 py-2 rounded-2xl bg-brand-600 hover:bg-brand-700 active:scale-95 text-white font-bold text-xs shadow-md shadow-brand-600/20 flex items-center gap-1 transition-all"
            >
              <Plus className="w-3.5 h-3.5" />
              Add
            </button>
          ) : (
            <div className="flex items-center gap-1 bg-brand-50 dark:bg-brand-950 border border-brand-300 dark:border-brand-800 rounded-2xl p-1">
              <button
                onClick={handleDecrease}
                className="w-7 h-7 rounded-xl bg-white dark:bg-slate-800 text-brand-700 dark:text-brand-300 flex items-center justify-center font-bold hover:bg-brand-100 transition-colors shadow-sm"
              >
                <Minus className="w-3 h-3" />
              </button>
              <span className="w-6 text-center text-xs font-bold text-brand-900 dark:text-brand-100">
                {quantity}
              </span>
              <button
                onClick={handleIncrease}
                className="w-7 h-7 rounded-xl bg-brand-600 text-white flex items-center justify-center font-bold hover:bg-brand-700 transition-colors shadow-sm"
              >
                <Plus className="w-3 h-3" />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      <PriceTransparencyModal
        product={product}
        isOpen={transparencyOpen}
        onClose={() => setTransparencyOpen(false)}
      />
    </>
  );
};
