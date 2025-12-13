"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { updateLocation } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function DashboardPage() {
  const router = useRouter();
  const { user, token, loading, setUser } = useAuth();
  const [locMessage, setLocMessage] = useState<string | null>(null);
  const [locError, setLocError] = useState<string | null>(null);
  const [locLoading, setLocLoading] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  const handleUpdateLocation = () => {
    if (!token) return;
    setLocError(null);
    setLocMessage(null);

    if (!("geolocation" in navigator)) {
      setLocError("Geolocation is not available in your browser.");
      return;
    }

    setLocLoading(true);
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const updated = await updateLocation(
            token,
            position.coords.latitude,
            position.coords.longitude
          );
          setUser(updated);
          setLocMessage("Location updated.");
        } catch (err) {
          setLocError(
            (err as Error).message ||
              "Unable to update location. Please try again later."
          );
        } finally {
          setLocLoading(false);
        }
      },
      (error) => {
        setLocLoading(false);
        if (error.code === error.PERMISSION_DENIED) {
          setLocError("Location permission was denied.");
        } else {
          setLocError("Unable to get your location.");
        }
      }
    );
  };

  if (loading || (!user && !locError)) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-100">
        <p className="text-sm text-slate-300">Loading your dashboard...</p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-4xl px-4 py-8 space-y-6">
        <header className="space-y-1">
          <p className="text-xs text-slate-400">Dashboard</p>
          <h1 className="text-2xl font-semibold tracking-tight">
            Welcome, {user.first_name}
          </h1>
          <p className="text-sm text-slate-400">
            From here you&apos;ll eventually request rides, offer rides, and see
            your upcoming trips.
          </p>
        </header>

        <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 space-y-3">
          <div className="flex items-center justify-between gap-2">
            <div>
              <h2 className="text-sm font-semibold text-slate-200">
                Current location
              </h2>
              <p className="text-xs text-slate-400">
                We only use your location to help match you with willing drivers
                or riders. It isn&apos;t shared publicly.
              </p>
            </div>
            <button
              type="button"
              onClick={handleUpdateLocation}
              disabled={locLoading || !token}
              className="inline-flex items-center justify-center rounded-md bg-emerald-500 px-3 py-1.5 text-xs font-semibold text-slate-950 shadow-sm hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {locLoading ? "Updating..." : "Update location"}
            </button>
          </div>
          {locError && (
            <p className="text-xs text-red-300 mt-1">{locError}</p>
          )}
          {locMessage && (
            <p className="text-xs text-emerald-300 mt-1">{locMessage}</p>
          )}
        </section>

        <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 space-y-2">
          <h2 className="text-sm font-semibold text-slate-200">Next steps</h2>
          <ul className="text-xs text-slate-400 list-disc list-inside space-y-1">
            <li>
              Review your{" "}
              <Link
                href="/profile"
                className="text-emerald-400 hover:text-emerald-300"
              >
                profile information
              </Link>
              .
            </li>
            <li>Think about when you are available to give or receive rides.</li>
            <li>
              Pray for the people you&apos;ll meet through this service — every
              ride is an opportunity for charity.
            </li>
          </ul>
        </section>
      </div>
    </main>
  );
}


