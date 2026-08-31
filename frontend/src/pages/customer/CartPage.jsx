import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import { Navbar } from '../../components/customer/Navbar';
import { Footer } from '../../components/customer/Footer';
import {
  ShoppingCart,
  Trash2,
  Plus,
  Minus,
  ArrowRight,
  ShieldCheck,
  Award,
  Leaf,
  Sparkles,
  ArrowLeft,
  Sprout
} from 'lucide-react';

export const CartPage = () => {
  const {
    items,
    itemCount,
    subtotal,
    farmerTotal,
    marketTotal,
    savings,
    deliveryFee,
    total,
    updateQuantity,
    removeItem,
    clearCart
  } = useCart();
  const { isAuthenticated, isCustomer } = useAuth();
  const navigate = useNavigate();

  const handleProceedToCheckout = () => {
    if (isAuthenticated && isCustomer) {
      navigate('/checkout');
    } else {
      // Guest Checkout Flow: Redirect to Login while preserving target destination
      navigate('/login', { state: { from: { pathname: '/checkout' } } });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/50 dark:bg-slate-950 font-sans">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight flex items-center gap-3">
              <ShoppingCart className="w-7 h-7 text-brand-600" />
              Your Fresh Produce Cart
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Direct from farmer cooperatives with 100% price transparency.
            </p>
          </div>

          {items.length > 0 && (
            <button
              onClick={clearCart}
              className="text-xs text-rose-600 hover:text-rose-700 font-semibold transition-colors"
            >
              Clear Cart
            </button>
          )}
        </div>

        {items.length === 0 ? (
          /* Empty Cart State */
          <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-12 text-center max-w-lg mx-auto my-12 shadow-sm space-y-5">
            <div className="w-20 h-20 rounded-3xl bg-brand-50 dark:bg-brand-950/60 text-brand-600 flex items-center justify-center mx-auto shadow-inner">
              <ShoppingCart className="w-10 h-10" />
            </div>
            <div className="space-y-1">
              <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                Your basket is empty
              </h2>
              <p className="text-xs text-slate-500 max-w-xs mx-auto">
                Explore dawn-harvested fresh vegetables, fruits, and organic grains directly from verified FPOs.
              </p>
            </div>
            <Link
              to="/"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-lg shadow-brand-600/20 transition-all hover:scale-[1.02]"
            >
              <Sprout className="w-4 h-4" />
              Browse Fresh Harvest
            </Link>
          </div>
        ) : (
          /* Cart Grid */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Left Column: Cart Items List */}
            <div className="lg:col-span-8 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 sm:p-8 shadow-sm divide-y divide-slate-100 dark:divide-slate-800 space-y-4">
              {items.map(({ product, quantity }) => (
                <div
                  key={product.id}
                  className="pt-4 first:pt-0 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
                >
                  {/* Thumbnail & Info */}
                  <div className="flex items-center gap-4 flex-1">
                    <img
                      src={product.image}
                      alt={product.name}
                      className="w-20 h-20 rounded-2xl object-cover bg-slate-100 shrink-0"
                    />
                    <div className="space-y-1">
                      <div className="text-[11px] font-bold text-brand-600 uppercase tracking-wider">
                        {product.fpoName}
                      </div>
                      <Link
                        to={`/product/${product.id}`}
                        className="font-bold text-sm text-slate-900 dark:text-white hover:text-brand-600 transition-colors line-clamp-1"
                      >
                        {product.name}
                      </Link>
                      <div className="text-xs text-slate-400">
                        {product.unit} • ₹{product.price} / unit
                      </div>
                      <div className="text-[10px] font-semibold text-brand-700 dark:text-brand-300">
                        ₹{product.farmerPrice * quantity} paid straight to farmer
                      </div>
                    </div>
                  </div>

                  {/* Quantity Stepper & Subtotal */}
                  <div className="flex items-center justify-between sm:justify-end gap-6 w-full sm:w-auto">
                    {/* Stepper */}
                    <div className="flex items-center gap-1 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-1">
                      <button
                        onClick={() => updateQuantity(product.id, quantity - 1)}
                        className="w-7 h-7 rounded-xl bg-white dark:bg-slate-700 text-slate-700 dark:text-slate-200 flex items-center justify-center font-bold hover:bg-slate-100 transition-colors shadow-sm"
                      >
                        <Minus className="w-3 h-3" />
                      </button>
                      <span className="w-6 text-center text-xs font-bold text-slate-900 dark:text-white">
                        {quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(product.id, quantity + 1)}
                        className="w-7 h-7 rounded-xl bg-brand-600 text-white flex items-center justify-center font-bold hover:bg-brand-700 transition-colors shadow-sm"
                      >
                        <Plus className="w-3 h-3" />
                      </button>
                    </div>

                    {/* Total Price */}
                    <div className="text-right min-w-[70px]">
                      <div className="text-sm font-black text-slate-900 dark:text-white">
                        ₹{product.price * quantity}
                      </div>
                      {product.marketPrice > product.price && (
                        <div className="text-[10px] text-slate-400 line-through">
                          ₹{product.marketPrice * quantity}
                        </div>
                      )}
                    </div>

                    {/* Remove */}
                    <button
                      onClick={() => removeItem(product.id)}
                      className="p-1.5 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
                      title="Remove item"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}

              <div className="pt-4 flex items-center justify-between text-xs text-slate-500">
                <Link to="/" className="flex items-center gap-1 text-brand-600 font-bold hover:underline">
                  <ArrowLeft className="w-3.5 h-3.5" /> Continue Shopping
                </Link>
                <span>{itemCount} total items</span>
              </div>
            </div>

            {/* Right Column: Order Summary & Checkout Trigger */}
            <div className="lg:col-span-4 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 sm:p-8 shadow-sm space-y-6">
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                Order Value Summary
              </h2>

              <div className="space-y-3 text-xs">
                <div className="flex items-center justify-between text-slate-600 dark:text-slate-400">
                  <span>Produce Subtotal ({itemCount} items)</span>
                  <span className="font-bold text-slate-900 dark:text-white">₹{subtotal}</span>
                </div>

                <div className="flex items-center justify-between text-brand-700 dark:text-brand-300">
                  <span className="flex items-center gap-1">
                    <Award className="w-3.5 h-3.5" /> Direct Farmer Payout
                  </span>
                  <span className="font-bold">₹{farmerTotal}</span>
                </div>

                {savings > 0 && (
                  <div className="flex items-center justify-between text-amber-700 dark:text-amber-400">
                    <span>Mandi Comparison Savings</span>
                    <span className="font-bold">-₹{savings}</span>
                  </div>
                )}

                <div className="flex items-center justify-between text-slate-600 dark:text-slate-400">
                  <span>Direct Express Delivery</span>
                  <span className="font-bold">
                    {deliveryFee === 0 ? (
                      <span className="text-brand-600 uppercase">FREE</span>
                    ) : (
                      `₹${deliveryFee}`
                    )}
                  </span>
                </div>

                {deliveryFee > 0 && (
                  <div className="p-2 rounded-xl bg-brand-50 dark:bg-brand-950/40 text-[10px] text-brand-800 dark:text-brand-300">
                    Add ₹{299 - subtotal} more produce to get <span className="font-bold">FREE delivery</span>
                  </div>
                )}

                <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-sm">
                  <span className="font-bold text-slate-900 dark:text-white">Total Amount</span>
                  <span className="text-xl font-black text-slate-900 dark:text-white">₹{total}</span>
                </div>
              </div>

              {/* Guest / Authenticated Checkout Button */}
              <div className="space-y-2">
                <button
                  onClick={handleProceedToCheckout}
                  className="w-full py-4 rounded-2xl bg-brand-600 hover:bg-brand-700 active:scale-98 text-white font-extrabold text-sm shadow-xl shadow-brand-600/25 flex items-center justify-center gap-2 transition-all"
                >
                  <span>Proceed to Checkout</span>
                  <ArrowRight className="w-4 h-4" />
                </button>

                {!isAuthenticated && (
                  <p className="text-[11px] text-slate-400 text-center leading-relaxed">
                    Guest shopping enabled. You will sign in seamlessly before completing order delivery.
                  </p>
                )}
              </div>

              {/* Trust Badge */}
              <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 space-y-1">
                <div className="flex items-center gap-1.5 font-bold text-slate-800 dark:text-slate-200">
                  <ShieldCheck className="w-4 h-4 text-brand-600" />
                  <span>100% Quality &amp; Freshness Guaranteed</span>
                </div>
                <p className="text-[10px] text-slate-400">
                  Direct harvest inspection and contactless temperature-sealed delivery.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
};
