import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';
import { Navbar } from '../../components/customer/Navbar';
import { Footer } from '../../components/customer/Footer';
import {
  ShieldCheck,
  CheckCircle2,
  MapPin,
  Clock,
  CreditCard,
  Truck,
  ArrowLeft,
  Sparkles,
  Award,
  Leaf,
  ShoppingCart
} from 'lucide-react';

export const CheckoutPlaceholder = () => {
  const { items, itemCount, subtotal, farmerTotal, savings, deliveryFee, total, clearCart } = useCart();
  const { user } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const [address, setAddress] = useState('Flat 402, Green Meadows Residency, Connaught Place');
  const [cityPin, setCityPin] = useState('New Delhi - 110001');
  const [selectedSlot, setSelectedSlot] = useState('evening-today');
  const [paymentMethod, setPaymentMethod] = useState('cod');
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderNumber, setOrderNumber] = useState('');

  const handlePlaceOrder = (e) => {
    e.preventDefault();
    if (items.length === 0) {
      toast.error('Your cart is empty.');
      return;
    }

    const demoOrderNum = `FARM-${Math.floor(100000 + Math.random() * 900000)}`;
    setOrderNumber(demoOrderNum);
    setOrderPlaced(true);
    clearCart();
    toast.success('Demonstration Order Placed Successfully!');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50/50 dark:bg-slate-950 font-sans">
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
        {orderPlaced ? (
          /* Order Confirmation Screen */
          <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 sm:p-12 text-center max-w-xl mx-auto shadow-xl space-y-6 animate-fadeIn">
            <div className="w-20 h-20 rounded-3xl bg-brand-50 dark:bg-brand-950 text-brand-600 flex items-center justify-center mx-auto shadow-inner">
              <CheckCircle2 className="w-12 h-12" />
            </div>

            <div className="space-y-2">
              <span className="px-3 py-1 rounded-full bg-brand-100 dark:bg-brand-950 text-brand-800 dark:text-brand-300 text-xs font-bold uppercase">
                Customer Authentication &amp; Checkout Verified
              </span>
              <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">
                Fresh Harvest Order Confirmed!
              </h1>
              <p className="text-xs text-slate-500">
                Order Reference: <span className="font-mono font-bold text-brand-600">{orderNumber}</span>
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-brand-50/70 dark:bg-brand-950/40 border border-brand-200/80 dark:border-brand-900/60 text-left text-xs space-y-2">
              <div className="flex items-center gap-2 font-bold text-brand-950 dark:text-brand-200">
                <Sparkles className="w-4 h-4 text-brand-600" />
                <span>Agricultural Impact Summary</span>
              </div>
              <p className="text-brand-800 dark:text-brand-300 text-[11px] leading-relaxed">
                Thank you, <span className="font-bold">{user?.full_name}</span>! Your produce will be temperature-dispatched from the Nashik/Solan FPO hub straight to your doorstep.
              </p>
            </div>

            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link
                to="/"
                className="w-full sm:w-auto px-6 py-3 rounded-2xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md shadow-brand-600/20 transition-all"
              >
                Back to Marketplace
              </Link>
            </div>
          </div>
        ) : (
          /* Main Checkout Layout */
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2 text-xs text-brand-600 font-bold uppercase tracking-wider">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Authenticated Customer Portal ({user?.email || user?.username})</span>
                </div>
                <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight">
                  Checkout &amp; Delivery Details
                </h1>
              </div>

              <Link to="/cart" className="flex items-center gap-1 text-xs font-semibold text-slate-500 hover:text-brand-600">
                <ArrowLeft className="w-4 h-4" /> Back to Cart
              </Link>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              {/* Left Column: Form Details */}
              <div className="lg:col-span-8 space-y-6">
                {/* 1. Customer Info & Address */}
                <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 sm:p-8 shadow-sm space-y-4">
                  <div className="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
                    <div className="w-8 h-8 rounded-xl bg-brand-100 dark:bg-brand-950 text-brand-700 dark:text-brand-300 flex items-center justify-center font-bold text-xs">
                      1
                    </div>
                    <div>
                      <h2 className="text-sm font-bold text-slate-900 dark:text-white">
                        Delivery Address
                      </h2>
                      <p className="text-[11px] text-slate-400">
                        Recipient: {user?.full_name} ({user?.phone || 'Customer Phone Verified'})
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 gap-3 text-xs">
                    <div className="space-y-1">
                      <label className="block text-slate-500 font-bold uppercase text-[10px]">
                        Street Address / Apartment
                      </label>
                      <input
                        type="text"
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        className="w-full p-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl text-xs text-slate-900 dark:text-white"
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="block text-slate-500 font-bold uppercase text-[10px]">
                        City &amp; PIN Code
                      </label>
                      <input
                        type="text"
                        value={cityPin}
                        onChange={(e) => setCityPin(e.target.value)}
                        className="w-full p-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl text-xs text-slate-900 dark:text-white"
                      />
                    </div>
                  </div>
                </div>

                {/* 2. Harvest Delivery Slot */}
                <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 sm:p-8 shadow-sm space-y-4">
                  <div className="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
                    <div className="w-8 h-8 rounded-xl bg-brand-100 dark:bg-brand-950 text-brand-700 dark:text-brand-300 flex items-center justify-center font-bold text-xs">
                      2
                    </div>
                    <div>
                      <h2 className="text-sm font-bold text-slate-900 dark:text-white">
                        Dawn Harvest Delivery Route
                      </h2>
                      <p className="text-[11px] text-slate-400">
                        Select cold-chain delivery window
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <label
                      className={`p-3.5 rounded-2xl border cursor-pointer transition-all flex items-start gap-3 ${
                        selectedSlot === 'evening-today'
                          ? 'border-brand-600 bg-brand-50/60 dark:bg-brand-950/40 text-brand-950 dark:text-brand-100'
                          : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 text-slate-700'
                      }`}
                    >
                      <input
                        type="radio"
                        name="slot"
                        checked={selectedSlot === 'evening-today'}
                        onChange={() => setSelectedSlot('evening-today')}
                        className="mt-1 text-brand-600 focus:ring-brand-500"
                      />
                      <div>
                        <div className="font-bold">Today Evening (5:00 PM - 8:30 PM)</div>
                        <div className="text-[11px] text-slate-500 mt-0.5">
                          Same-day harvest route (Picked at 5:00 AM)
                        </div>
                      </div>
                    </label>

                    <label
                      className={`p-3.5 rounded-2xl border cursor-pointer transition-all flex items-start gap-3 ${
                        selectedSlot === 'morning-tomorrow'
                          ? 'border-brand-600 bg-brand-50/60 dark:bg-brand-950/40 text-brand-950 dark:text-brand-100'
                          : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 text-slate-700'
                      }`}
                    >
                      <input
                        type="radio"
                        name="slot"
                        checked={selectedSlot === 'morning-tomorrow'}
                        onChange={() => setSelectedSlot('morning-tomorrow')}
                        className="mt-1 text-brand-600 focus:ring-brand-500"
                      />
                      <div>
                        <div className="font-bold">Tomorrow Morning (6:30 AM - 9:00 AM)</div>
                        <div className="text-[11px] text-slate-500 mt-0.5">
                          Early sunrise doorstep drop
                        </div>
                      </div>
                    </label>
                  </div>
                </div>

                {/* 3. Payment Method (Demo Mode) */}
                <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 sm:p-8 shadow-sm space-y-4">
                  <div className="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
                    <div className="w-8 h-8 rounded-xl bg-brand-100 dark:bg-brand-950 text-brand-700 dark:text-brand-300 flex items-center justify-center font-bold text-xs">
                      3
                    </div>
                    <div>
                      <h2 className="text-sm font-bold text-slate-900 dark:text-white">
                        Payment Method (Prototype Demo)
                      </h2>
                      <p className="text-[11px] text-slate-400">
                        Payment gateway placeholder
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <label
                      className={`p-3.5 rounded-2xl border cursor-pointer transition-all flex items-center gap-3 ${
                        paymentMethod === 'cod'
                          ? 'border-brand-600 bg-brand-50/60 dark:bg-brand-950/40 text-brand-950 dark:text-brand-100 font-bold'
                          : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 text-slate-700'
                      }`}
                    >
                      <input
                        type="radio"
                        name="payment"
                        checked={paymentMethod === 'cod'}
                        onChange={() => setPaymentMethod('cod')}
                        className="text-brand-600 focus:ring-brand-500"
                      />
                      <span>Cash on Delivery / UPI upon Delivery</span>
                    </label>

                    <label
                      className={`p-3.5 rounded-2xl border cursor-pointer transition-all flex items-center gap-3 ${
                        paymentMethod === 'upi-demo'
                          ? 'border-brand-600 bg-brand-50/60 dark:bg-brand-950/40 text-brand-950 dark:text-brand-100 font-bold'
                          : 'border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 text-slate-700'
                      }`}
                    >
                      <input
                        type="radio"
                        name="payment"
                        checked={paymentMethod === 'upi-demo'}
                        onChange={() => setPaymentMethod('upi-demo')}
                        className="text-brand-600 focus:ring-brand-500"
                      />
                      <span>UPI Direct Instant (Demo Mock)</span>
                    </label>
                  </div>
                </div>
              </div>

              {/* Right Column: Order Summary */}
              <div className="lg:col-span-4 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 sm:p-8 shadow-sm space-y-6">
                <h2 className="text-base font-bold text-slate-900 dark:text-white">
                  Order Summary
                </h2>

                <div className="space-y-3 text-xs">
                  <div className="flex items-center justify-between text-slate-600 dark:text-slate-400">
                    <span>Produce Total ({itemCount} items)</span>
                    <span className="font-bold text-slate-900 dark:text-white">₹{subtotal}</span>
                  </div>

                  <div className="flex items-center justify-between text-brand-700 dark:text-brand-300">
                    <span className="flex items-center gap-1">
                      <Award className="w-3.5 h-3.5" /> Farmer Payout
                    </span>
                    <span className="font-bold">₹{farmerTotal}</span>
                  </div>

                  <div className="flex items-center justify-between text-slate-600 dark:text-slate-400">
                    <span>Direct Express Delivery</span>
                    <span className="font-bold">
                      {deliveryFee === 0 ? <span className="text-brand-600 uppercase">FREE</span> : `₹${deliveryFee}`}
                    </span>
                  </div>

                  <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-sm">
                    <span className="font-bold text-slate-900 dark:text-white">Total to Pay</span>
                    <span className="text-xl font-black text-slate-900 dark:text-white">₹{total}</span>
                  </div>
                </div>

                <button
                  onClick={handlePlaceOrder}
                  className="w-full py-4 rounded-2xl bg-brand-600 hover:bg-brand-700 active:scale-98 text-white font-extrabold text-sm shadow-xl shadow-brand-600/25 flex items-center justify-center gap-2 transition-all"
                >
                  <CheckCircle2 className="w-5 h-5" />
                  <span>Place Demonstration Order</span>
                </button>

                <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 space-y-1">
                  <div className="font-bold text-slate-800 dark:text-slate-200">
                    Prototype Verification Notice
                  </div>
                  <p className="text-[10px] text-slate-400">
                    This order demonstrates the end-to-end Customer Authentication &amp; Protected Checkout flow. No real charges are debited.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
};
