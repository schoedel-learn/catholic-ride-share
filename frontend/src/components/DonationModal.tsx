"use client";

import { useMemo, useState } from "react";
import { loadStripe } from "@stripe/stripe-js";
import {
  Elements,
  PaymentElement,
  useElements,
  useStripe,
} from "@stripe/react-stripe-js";
import type { DonationIntent } from "@/lib/api";

type Props = {
  open: boolean;
  intent: DonationIntent | null;
  title?: string;
  onClose: () => void;
  onSuccess?: () => void;
};

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || ""
);

function DonationCheckoutForm({
  onClose,
  onSuccess,
}: {
  onClose: () => void;
  onSuccess?: () => void;
}) {
  const stripe = useStripe();
  const elements = useElements();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!stripe || !elements) return;

    setSubmitting(true);
    try {
      const result = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: window.location.href,
        },
        redirect: "if_required",
      });

      if (result.error) {
        setError(result.error.message || "Payment failed");
        return;
      }

      onSuccess?.();
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <PaymentElement />
      {error && (
        <div className="rounded-md bg-red-900/30 border border-red-700 px-3 py-2 text-xs text-red-200">
          {error}
        </div>
      )}
      <div className="flex items-center justify-end gap-2">
        <button
          type="button"
          onClick={onClose}
          className="rounded-md border border-slate-700 px-3 py-2 text-sm text-slate-200 hover:bg-slate-800"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={!stripe || !elements || submitting}
          className="rounded-md bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {submitting ? "Processing…" : "Donate"}
        </button>
      </div>
    </form>
  );
}

export function DonationModal({ open, intent, title, onClose, onSuccess }: Props) {
  const appearance = useMemo(
    () => ({
      theme: "night" as const,
    }),
    []
  );

  if (!open) return null;

  const publishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;
  const missingStripe = !publishableKey;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4"
      role="dialog"
      aria-modal="true"
      aria-label={title || "Donate"}
    >
      <div className="w-full max-w-lg rounded-xl border border-slate-800 bg-slate-950 text-slate-100 shadow-xl">
        <div className="flex items-start justify-between gap-4 border-b border-slate-800 px-5 py-4">
          <div>
            <h3 className="text-base font-semibold">{title || "Support the app"}</h3>
            {intent && (
              <p className="mt-1 text-xs text-slate-400">
                Donation amount:{" "}
                <span className="text-slate-200">
                  ${intent.amount.toFixed(2)}
                </span>
              </p>
            )}
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-md border border-slate-800 px-2 py-1 text-xs text-slate-300 hover:bg-slate-900"
          >
            Close
          </button>
        </div>

        <div className="px-5 py-4">
          {!intent ? (
            <p className="text-sm text-slate-300">Preparing donation…</p>
          ) : missingStripe ? (
            <div className="rounded-md bg-amber-900/20 border border-amber-700 px-3 py-2 text-xs text-amber-200">
              Missing{" "}
              <code className="font-mono">NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY</code>
              . Configure it in your frontend environment to collect donations.
            </div>
          ) : (
            <Elements
              stripe={stripePromise}
              options={{
                clientSecret: intent.client_secret,
                appearance,
              }}
            >
              <DonationCheckoutForm onClose={onClose} onSuccess={onSuccess} />
            </Elements>
          )}
        </div>
      </div>
    </div>
  );
}
