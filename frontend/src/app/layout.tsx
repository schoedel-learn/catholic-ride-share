"use client";

import "../globals.css";
import { ReactNode } from "react";

export const metadata = {
  title: "Catholic Ride Share",
  description: "Connecting the faithful with safe, volunteer rides.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className="bg-white text-slate-900">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <div className="mx-auto flex max-w-5xl flex-col gap-8 px-4 py-10 sm:px-8">
          <header className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm font-semibold text-crs-gold uppercase tracking-wide">
                Catholic Ride Share
              </p>
              <h1 className="text-3xl font-bold text-crs-navy">Serving the faithful</h1>
              <p className="mt-2 text-base text-slate-700">
                Volunteer drivers helping riders reach Mass, Confession, and parish life.
              </p>
            </div>
          </header>
          <main>{children}</main>
          <footer className="border-t border-slate-200 pt-6 text-sm text-slate-600">
            Built with care for accessibility and community safety.
          </footer>
        </div>
      </body>
    </html>
  );
}
