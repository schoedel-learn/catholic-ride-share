import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section - Flat, bold, high contrast */}
      <header className="safe-top bg-marian px-4 pt-14 pb-12 text-center">
        <div className="mx-auto max-w-lg">
          {/* Simple cross icon */}
          <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-gold text-navy">
            <span className="text-3xl font-bold">✝</span>
          </div>
          <h1 className="text-4xl font-black tracking-tight text-white sm:text-5xl">
            Catholic Ride Share
          </h1>
          <p className="mt-4 text-lg font-medium text-white/90">
            Get to Mass. Help others get there too.
          </p>
        </div>
      </header>

      {/* Main CTA Buttons - Flat, bold, no shadows */}
      <main className="px-4 py-8">
        <div className="mx-auto max-w-sm space-y-4">
          <Link
            href="/login"
            className="flex w-full items-center justify-center gap-3 rounded-none bg-navy px-6 py-5 text-xl font-bold text-white uppercase tracking-wide transition-colors hover:bg-black active:bg-black"
          >
            Sign In
          </Link>
          
          <Link
            href="/register"
            className="flex w-full items-center justify-center gap-3 rounded-none border-4 border-navy bg-white px-6 py-5 text-xl font-bold text-navy uppercase tracking-wide transition-colors hover:bg-navy hover:text-white active:bg-navy active:text-white"
          >
            Create Account
          </Link>

          <Link
            href="/dashboard"
            className="flex w-full items-center justify-center gap-3 rounded-none bg-gold px-6 py-5 text-xl font-bold text-navy uppercase tracking-wide transition-colors hover:bg-gold-600 active:bg-gold-600"
          >
            Dashboard
          </Link>
        </div>

        {/* Feature Cards - Flat with colored left borders */}
        <div className="mx-auto mt-12 max-w-lg space-y-0">
          <div className="border-l-8 border-marian bg-slate-100 p-6">
            <h3 className="text-xl font-bold text-navy uppercase tracking-wide">Request a Ride</h3>
            <p className="mt-2 text-base text-slate-700">
              Need a ride to Mass, Confession, or a parish event? Volunteer drivers are ready to help.
            </p>
          </div>

          <div className="border-l-8 border-gold bg-slate-50 p-6">
            <h3 className="text-xl font-bold text-navy uppercase tracking-wide">Offer Your Time</h3>
            <p className="mt-2 text-base text-slate-700">
              Drive fellow parishioners to the sacraments. Set your availability and serve.
            </p>
          </div>

          <div className="border-l-8 border-marian bg-slate-100 p-6">
            <h3 className="text-xl font-bold text-navy uppercase tracking-wide">Safe &amp; Trusted</h3>
            <p className="mt-2 text-base text-slate-700">
              Verified community members. Your privacy is protected.
            </p>
          </div>
        </div>
      </main>

      {/* Footer - Flat */}
      <footer className="safe-bottom bg-navy px-4 py-6 text-center">
        <p className="text-sm font-medium text-white/80 uppercase tracking-wider">
          Serving the faithful with charity
        </p>
      </footer>
    </div>
  );
}
