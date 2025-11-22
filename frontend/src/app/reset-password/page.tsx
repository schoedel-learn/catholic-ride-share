"use client";

import { FormEvent, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { resetPassword, validateResetToken } from "@/lib/api";

export default function ResetPasswordPage() {
  const searchParams = useSearchParams();
  const initialToken = searchParams.get("token") ?? "";

  const [token, setToken] = useState(initialToken);
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [checking, setChecking] = useState<boolean>(!!initialToken);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const check = async () => {
      if (!initialToken) {
        setChecking(false);
        return;
      }
      try {
        await validateResetToken(initialToken);
        setChecking(false);
      } catch (err) {
        setError((err as Error).message || "Invalid or expired reset link.");
        setChecking(false);
      }
    };
    void check();
  }, [initialToken]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);
    try {
      const res = await resetPassword(token, newPassword);
      setMessage(res.message);
    } catch (err) {
      setError((err as Error).message || "Unable to reset password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-100">
      <div className="w-full max-w-md px-6 py-10 rounded-2xl border border-slate-800 bg-slate-900/70 shadow-xl">
        <h1 className="text-2xl font-semibold tracking-tight">Reset password</h1>
        <p className="mt-1 text-sm text-slate-400">
          Enter your reset token and choose a new password.
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          {checking && (
            <div className="rounded-md bg-slate-800 px-3 py-2 text-sm text-slate-200">
              Validating reset link...
            </div>
          )}
          {error && (
            <div className="rounded-md bg-red-900/40 border border-red-700 px-3 py-2 text-sm text-red-200">
              {error}
            </div>
          )}
          {message && (
            <div className="rounded-md bg-emerald-900/40 border border-emerald-700 px-3 py-2 text-sm text-emerald-200">
              {message}
            </div>
          )}

          <div>
            <label
              htmlFor="token"
              className="block text-sm font-medium text-slate-200"
            >
              Reset token
            </label>
            <input
              id="token"
              type="text"
              required
              value={token}
              onChange={(e) => setToken(e.target.value)}
              className="mt-1 block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div>
            <label
              htmlFor="new-password"
              className="block text-sm font-medium text-slate-200"
            >
              New password
            </label>
            <input
              id="new-password"
              type="password"
              required
              minLength={8}
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              className="mt-1 block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading || checking}
            className="w-full inline-flex items-center justify-center rounded-md bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-slate-950 shadow-sm hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950"
          >
            {loading ? "Resetting password..." : "Reset password"}
          </button>
        </form>

        <p className="mt-4 text-xs text-slate-400">
          After resetting, you can{" "}
          <Link href="/login" className="text-emerald-400 hover:text-emerald-300">
            sign in with your new password
          </Link>
          .
        </p>
      </div>
    </main>
  );
}


