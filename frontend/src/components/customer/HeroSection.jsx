import React from 'react';
import { Sprout, ArrowRight, ShieldCheck, Clock, Users, Sparkles, TrendingUp, CheckCircle2 } from 'lucide-react';

export const HeroSection = ({ onExploreClick, onHowItWorksClick }) => {
  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-brand-50/70 via-white to-soil-50/50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950 pt-8 pb-12 border-b border-slate-200/60 dark:border-slate-800">
      {/* Decorative subtle background elements */}
      <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 rounded-full bg-brand-200/30 dark:bg-brand-900/10 blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -mb-12 -ml-12 w-80 h-80 rounded-full bg-amber-200/20 dark:bg-amber-900/10 blur-3xl pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          {/* Left Column: Mission & Main Proposition */}
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
            {/* Mission Badge */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-100/80 dark:bg-brand-950/80 border border-brand-200 dark:border-brand-800/80 text-brand-900 dark:text-brand-300 text-xs font-bold shadow-sm">
              <Sprout className="w-4 h-4 text-brand-600 dark:text-brand-400" />
              <span>SIH26033 AgriTech Direct Marketplace</span>
              <span className="w-1.5 h-1.5 rounded-full bg-brand-600 animate-pulse" />
            </div>

            {/* Main Headline */}
            <div className="space-y-2">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 dark:text-white tracking-tight leading-[1.1]">
                Fresh from the farm.
              </h1>
              <p className="text-2xl sm:text-3xl font-extrabold text-brand-700 dark:text-brand-400 tracking-tight">
                Better prices for farmers. Fresher produce for you.
              </p>
            </div>

            {/* Supporting Explanation */}
            <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 max-w-2xl leading-relaxed">
              We connect local Farmer Producer Organizations (FPOs) directly to your kitchen. By removing 4-5 layers of middlemen, farmers earn up to <span className="font-bold text-slate-900 dark:text-white">40% more</span>, while you enjoy produce harvested at dawn.
            </p>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <button
                onClick={onExploreClick}
                className="w-full sm:w-auto px-7 py-3.5 rounded-2xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-sm shadow-xl shadow-brand-600/25 flex items-center justify-center gap-2.5 transition-all hover:scale-[1.02] active:scale-[0.98]"
              >
                <span>Explore Today's Fresh Harvest</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                onClick={onHowItWorksClick}
                className="w-full sm:w-auto px-6 py-3.5 rounded-2xl bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 font-bold text-sm shadow-sm transition-all"
              >
                How FarmApp Works
              </button>
            </div>

            {/* Key Value Micro Badges */}
            <div className="grid grid-cols-3 gap-2 pt-4 border-t border-slate-200/80 dark:border-slate-800">
              <div className="flex items-center gap-2 text-left">
                <div className="w-8 h-8 rounded-xl bg-brand-100 dark:bg-brand-950 text-brand-700 dark:text-brand-300 flex items-center justify-center shrink-0">
                  <Clock className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-xs font-bold text-slate-900 dark:text-white">&lt;12 Hours</div>
                  <div className="text-[10px] text-slate-500">Harvest to Door</div>
                </div>
              </div>

              <div className="flex items-center gap-2 text-left">
                <div className="w-8 h-8 rounded-xl bg-amber-100 dark:bg-amber-950 text-amber-700 dark:text-amber-300 flex items-center justify-center shrink-0">
                  <TrendingUp className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-xs font-bold text-slate-900 dark:text-white">Fair Pricing</div>
                  <div className="text-[10px] text-slate-500">Full Transparency</div>
                </div>
              </div>

              <div className="flex items-center gap-2 text-left">
                <div className="w-8 h-8 rounded-xl bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300 flex items-center justify-center shrink-0">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-xs font-bold text-slate-900 dark:text-white">100% Traceable</div>
                  <div className="text-[10px] text-slate-500">Verified FPOs</div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Supply Chain Storytelling Card */}
          <div className="lg:col-span-5">
            <div className="bg-white dark:bg-slate-900/90 rounded-3xl border border-slate-200/80 dark:border-slate-800 p-6 shadow-xl space-y-5 relative">
              <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-brand-500" />
                  <span className="text-xs font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                    Direct Agri-Supply Chain
                  </span>
                </div>
                <span className="text-[10px] font-semibold text-brand-600 bg-brand-50 dark:bg-brand-950 px-2 py-0.5 rounded-full">
                  Zero Intermediaries
                </span>
              </div>

              {/* Steps */}
              <div className="space-y-4">
                <div className="flex items-start gap-3.5 p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/60">
                  <div className="w-8 h-8 rounded-xl bg-brand-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-sm shadow-brand-600/30">
                    1
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900 dark:text-white">
                      Harvest at Sunrise (5:00 AM)
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Smallholder farmers in Nashik &amp; Solan pick produce based on verified customer demand.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5 p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/60">
                  <div className="w-8 h-8 rounded-xl bg-brand-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-sm shadow-brand-600/30">
                    2
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900 dark:text-white">
                      FPO Aggregation &amp; Ozone Wash (8:00 AM)
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Graded for export-grade quality, ozone sanitized, and packed in breathable crates.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5 p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/60">
                  <div className="w-8 h-8 rounded-xl bg-brand-600 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-sm shadow-brand-600/30">
                    3
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-900 dark:text-white">
                      Cold-Chain Transit to City Hubs (11:00 AM)
                    </div>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Temperature-controlled fleets avoid quality degradation without artificial wax coatings.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3.5 p-3 rounded-2xl bg-brand-50/80 dark:bg-brand-950/40 border border-brand-200/80 dark:border-brand-900/60">
                  <div className="w-8 h-8 rounded-xl bg-brand-700 text-white font-black text-xs flex items-center justify-center shrink-0 shadow-sm">
                    4
                  </div>
                  <div>
                    <div className="text-xs font-bold text-brand-950 dark:text-brand-200">
                      Delivered to Your Doorstep (&lt; 5:00 PM)
                    </div>
                    <p className="text-[11px] text-brand-700 dark:text-brand-400 mt-0.5">
                      Peak natural nutrition delivered on the very day of harvest.
                    </p>
                  </div>
                </div>
              </div>

              {/* Impact Footer */}
              <div className="pt-2 flex items-center justify-between text-xs text-slate-500">
                <span className="font-semibold">FPO Network: 18+ Clusters</span>
                <span className="font-bold text-brand-600">Fair Payouts Guaranteed</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
