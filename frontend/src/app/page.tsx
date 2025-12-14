import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-ivory">
      {/* Hero Section with Marian Blue header */}
      <header className="safe-top bg-gradient-to-b from-marian-600 to-marian-700 px-4 pt-12 pb-10 text-center">
        <div className="mx-auto max-w-lg">
          {/* App Icon/Logo with Gold accent */}
          <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-white shadow-lg">
            <svg className="h-10 w-10 text-marian-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M8 7h8m-8 5h8m-4 5v-5m-8 9h16a2 2 0 002-2V5a2 2 0 00-2-2H4a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Catholic Ride Share
          </h1>
          <p className="mt-3 text-base text-marian-100 sm:text-lg">
            Connecting the faithful for rides to Mass, Confession, and parish events.
          </p>
        </div>
      </header>

      {/* Main CTA Buttons - Touch-friendly sizing */}
      <main className="px-4 py-8">
        <div className="mx-auto max-w-sm space-y-3">
          <Link
            href="/login"
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-marian-500 px-6 py-4 text-lg font-semibold text-white shadow-lg shadow-marian-500/25 transition-all duration-200 active:scale-[0.98] hover:bg-marian-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-marian-500"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
            </svg>
            Sign In
          </Link>
          
          <Link
            href="/register"
            className="flex w-full items-center justify-center gap-2 rounded-xl border-2 border-navy/20 bg-white px-6 py-4 text-lg font-semibold text-navy shadow-sm transition-all duration-200 active:scale-[0.98] hover:border-navy/30 hover:bg-ivory focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-marian-500"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
            Create Account
          </Link>

          <Link
            href="/dashboard"
            className="flex w-full items-center justify-center gap-2 rounded-xl border-2 border-gold-500/50 bg-gold-50 px-6 py-4 text-lg font-semibold text-gold-800 shadow-sm transition-all duration-200 active:scale-[0.98] hover:border-gold-500 hover:bg-gold-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gold-500"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            Dashboard
          </Link>
        </div>

        {/* Feature Cards */}
        <div className="mx-auto mt-10 max-w-lg space-y-4">
          <div className="rounded-2xl border border-navy/10 bg-white p-5 shadow-sm">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-marian-100 text-marian-600">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-navy">Request a Ride</h3>
                <p className="mt-1 text-sm text-navy/70">
                  Need transportation to Mass or a parish event? Our volunteer drivers are ready to help.
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-navy/10 bg-white p-5 shadow-sm">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gold-100 text-gold-700">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-navy">Offer Your Time</h3>
                <p className="mt-1 text-sm text-navy/70">
                  Drive fellow parishioners to the sacraments. Set your availability and serve the community.
                </p>
              </div>
            </div>
          </div>

          <div className="rounded-2xl border border-navy/10 bg-white p-5 shadow-sm">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-marian-100 text-marian-600">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-navy">Safe &amp; Trusted</h3>
                <p className="mt-1 text-sm text-navy/70">
                  Verified community members. Your location is only shared when necessary.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Bottom safe area for PWA */}
      <footer className="safe-bottom border-t border-navy/10 bg-white px-4 pb-6 pt-4 text-center">
        <p className="text-xs text-navy/50">
          Serving the faithful with charity and trust.
        </p>
      </footer>
    </div>
  );
}
