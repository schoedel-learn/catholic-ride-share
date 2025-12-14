export default function HomePage() {
  return (
    <section className="grid gap-6 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <div className="space-y-2">
        <h2 className="text-2xl font-semibold text-crs-navy">Welcome</h2>
        <p className="text-slate-700">
          This is the forthcoming frontend for Catholic Ride Share. Accessibility and responsive
          design are first-class: typography scales, color contrast meets WCAG, and layout adapts
          from mobile to desktop.
        </p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        <article className="rounded-xl border border-slate-200 bg-slate-50 p-4 shadow-xs">
          <h3 className="text-lg font-semibold text-crs-navy">Riders</h3>
          <p className="mt-1 text-sm text-slate-700">
            Request safe rides to Mass, Confession, and parish events. Clear status updates and
            privacy-respecting location sharing are coming soon.
          </p>
        </article>
        <article className="rounded-xl border border-slate-200 bg-slate-50 p-4 shadow-xs">
          <h3 className="text-lg font-semibold text-crs-navy">Drivers</h3>
          <p className="mt-1 text-sm text-slate-700">
            Offer rides with transparent availability and verification. Tailored flows will help you
            serve the community with confidence.
          </p>
        </article>
      </div>
      <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 shadow-xs">
        <h3 className="text-lg font-semibold text-crs-navy">Next steps</h3>
        <ul className="mt-2 space-y-2 text-sm text-slate-700">
          <li>• Wire API base URL from env for deployments.</li>
          <li>• Add auth pages (login/register/reset) with accessible forms.</li>
          <li>• Build rider/driver dashboards with Tailwind components.</li>
        </ul>
      </div>
    </section>
  );
}
