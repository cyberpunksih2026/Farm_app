import React from 'react';
import { X, TrendingUp, ShieldCheck, ArrowRight, DollarSign, CheckCircle2 } from 'lucide-react';

export const PriceTransparencyModal = ({ product, isOpen, onClose }) => {
  if (!isOpen || !product) return null;

  const farmerSharePercent = Math.round((product.farmerPrice / product.price) * 100);
  const consumerSavingsPercent = Math.round(((product.marketPrice - product.price) / product.marketPrice) * 100);
  const logisticsAndQuality = Math.max(2, Math.round((product.price - product.farmerPrice) * 0.65));
  const platformFee = Math.max(1, product.price - product.farmerPrice - logisticsAndQuality);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl max-w-lg w-full overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-6 bg-brand-50/80 dark:bg-brand-950/40 border-b border-brand-100 dark:border-brand-900/40 flex items-start justify-between">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-brand-600 text-white text-[11px] font-bold tracking-wide uppercase mb-2">
              <ShieldCheck className="w-3.5 h-3.5" />
              100% Fair Price Guarantee
            </div>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">
              Price Transparency Breakdown
            </h3>
            <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
              {product.name} ({product.unit})
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-white/80 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6 overflow-y-auto">
          {/* Comparison Cards */}
          <div className="grid grid-cols-2 gap-3">
            <div className="p-4 rounded-2xl bg-brand-50/60 dark:bg-brand-950/30 border border-brand-200/80 dark:border-brand-900/50">
              <span className="text-[11px] font-semibold text-brand-700 dark:text-brand-300 uppercase">
                Farmer Realization
              </span>
              <div className="text-2xl font-extrabold text-brand-900 dark:text-brand-100 mt-1">
                {farmerSharePercent}%
              </div>
              <p className="text-[11px] text-brand-700 dark:text-brand-400 mt-0.5">
                ₹{product.farmerPrice} paid directly to {product.farmerLead || 'Farmer'}
              </p>
            </div>

            <div className="p-4 rounded-2xl bg-amber-50/60 dark:bg-amber-950/30 border border-amber-200/80 dark:border-amber-900/50">
              <span className="text-[11px] font-semibold text-amber-700 dark:text-amber-300 uppercase">
                Customer Savings
              </span>
              <div className="text-2xl font-extrabold text-amber-900 dark:text-amber-100 mt-1">
                {consumerSavingsPercent}%
              </div>
              <p className="text-[11px] text-amber-700 dark:text-amber-400 mt-0.5">
                Saved vs traditional market (₹{product.marketPrice})
              </p>
            </div>
          </div>

          {/* Value Chain Breakdown */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-3">
              Where your ₹{product.price} goes:
            </h4>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 text-xs">
                <div className="flex items-center gap-2.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-brand-600" />
                  <div>
                    <div className="font-semibold text-slate-800 dark:text-slate-200">
                      Direct Farmer / FPO Payout
                    </div>
                    <div className="text-[11px] text-slate-500">
                      {product.fpoName} ({product.fpoLocation})
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-slate-900 dark:text-white">₹{product.farmerPrice}</div>
                  <div className="text-[10px] text-brand-600 font-semibold">{farmerSharePercent}% of total</div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 text-xs">
                <div className="flex items-center gap-2.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-blue-500" />
                  <div>
                    <div className="font-semibold text-slate-800 dark:text-slate-200">
                      Cold-Chain Logistics & Quality Grading
                    </div>
                    <div className="text-[11px] text-slate-500">
                      Ozone sanitization, crates, and temp-controlled transit
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-slate-900 dark:text-white">₹{logisticsAndQuality}</div>
                  <div className="text-[10px] text-slate-500">Actual cost</div>
                </div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 text-xs">
                <div className="flex items-center gap-2.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-slate-400" />
                  <div>
                    <div className="font-semibold text-slate-800 dark:text-slate-200">
                      FarmApp Tech & Operations
                    </div>
                    <div className="text-[11px] text-slate-500">
                      Platform hosting, traceability and customer support
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-slate-900 dark:text-white">₹{platformFee}</div>
                  <div className="text-[10px] text-slate-500">Fixed margin</div>
                </div>
              </div>
            </div>
          </div>

          {/* Traditional Middlemen comparison */}
          <div className="p-4 rounded-2xl bg-rose-50/50 dark:bg-rose-950/20 border border-rose-200/60 dark:border-rose-900/40 text-xs">
            <div className="font-bold text-rose-800 dark:text-rose-300 mb-1">
              Traditional Mandi Supply Chain Disadvantage:
            </div>
            <p className="text-slate-600 dark:text-slate-400 text-[11px] leading-relaxed">
              In conventional agricultural wholesale, 4-6 intermediaries (village aggregators, commission agents, regional mandi traders, wholesale dealers) take up to 65% of the consumer price while produce spends 48+ hours in transit.
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 dark:bg-slate-800/80 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-medium text-xs transition-colors"
          >
            Got it, thanks!
          </button>
        </div>
      </div>
    </div>
  );
};
