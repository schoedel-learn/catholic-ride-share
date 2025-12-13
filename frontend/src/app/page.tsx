import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      <div className="max-w-xl w-full px-6 py-12 rounded-3xl border border-slate-800 bg-slate-900/70 shadow-xl">
        <div className="mb-8 text-center">
          <p className="text-sm font-semibold tracking-wide text-slate-400 uppercase">
            Welcome to
          </p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">
            Catholic Ride Share
          </h1>
          <p className="mt-3 text-slate-300">
            Connect with nearby parishioners for rides to Mass, confession, and
            parish events. Serve and be served, all from your phone.
          </p>
        </div>

        <div className="flex flex-col gap-3">
          <Link
            href="/login"
            className="inline-flex items-center justify-center rounded-lg bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-slate-900 shadow-sm hover:bg-emerald-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2"
          >
            Sign in
          </Link>
          <Link
            href="/register"
            className="inline-flex items-center justify-center rounded-lg border border-slate-700 px-4 py-2.5 text-sm font-semibold text-slate-100 hover:bg-slate-800"
          >
            Create an account
          </Link>
        </div>

        <p className="mt-6 text-xs text-center text-slate-500">
          By continuing, you agree to serve others with charity and kindness,
          reflecting Christ&apos;s love in every journey.
        </p>
      </div>
    </main>
  );
}

