"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import {
  createRideRequest,
  acceptRideRequest,
  listAssignedRides,
  listMyRideRequests,
  listOpenRideRequests,
  listParishes,
  updateRideStatus,
  updateLocation,
  type Parish,
  type Ride,
  type RideRequest,
} from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function DashboardPage() {
  const router = useRouter();
  const { user, token, loading, setUser } = useAuth();
  const [locMessage, setLocMessage] = useState<string | null>(null);
  const [locError, setLocError] = useState<string | null>(null);
  const [locLoading, setLocLoading] = useState(false);
  const [parishes, setParishes] = useState<Parish[]>([]);
  const [myRequests, setMyRequests] = useState<RideRequest[]>([]);
  const [requestLoading, setRequestLoading] = useState(false);
  const [requestMessage, setRequestMessage] = useState<string | null>(null);
  const [requestError, setRequestError] = useState<string | null>(null);
  const [openRequests, setOpenRequests] = useState<RideRequest[]>([]);
  const [assignedRides, setAssignedRides] = useState<Ride[]>([]);
  const [driverLoading, setDriverLoading] = useState(false);
  const [driverError, setDriverError] = useState<string | null>(null);
  const [acceptingId, setAcceptingId] = useState<number | null>(null);
  const [statusUpdating, setStatusUpdating] = useState<number | null>(null);
  const [form, setForm] = useState({
    pickupLat: "37.7749",
    pickupLng: "-122.4194",
    dropoffLat: "37.7849",
    dropoffLng: "-122.4094",
    destinationType: "mass" as RideRequest["destination_type"],
    parishId: "",
    requestedDatetime: new Date(Date.now() + 60 * 60 * 1000)
      .toISOString()
      .slice(0, 16),
    notes: "",
    passengerCount: 1,
  });

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [loading, user, router]);

  useEffect(() => {
    if (!token) return;

    const load = async () => {
      try {
        const [parishList, requests] = await Promise.all([
          listParishes(),
          listMyRideRequests(token),
        ]);
        setParishes(parishList);
        setMyRequests(requests);
      } catch (err) {
        console.error("Failed loading dashboard data", err);
      }
    };

    void load();
  }, [token]);

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

  const isRider = useMemo(
    () => user?.role === "rider" || user?.role === "both",
    [user]
  );

  const isDriver = useMemo(
    () => user?.role === "driver" || user?.role === "both" || user?.role === "admin",
    [user]
  );

  useEffect(() => {
    if (!token || !isDriver) return;
    const loadDriverData = async () => {
      setDriverLoading(true);
      setDriverError(null);
      try {
        const [open, assigned] = await Promise.all([
          listOpenRideRequests(token),
          listAssignedRides(token),
        ]);
        setOpenRequests(open);
        setAssignedRides(assigned);
      } catch (err) {
        setDriverError((err as Error).message || "Unable to load driver data.");
      } finally {
        setDriverLoading(false);
      }
    };

    void loadDriverData();
  }, [token, isDriver]);

  const handleRideRequestSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!token) return;
    setRequestLoading(true);
    setRequestMessage(null);
    setRequestError(null);

    try {
      const payload = {
        pickup: {
          latitude: parseFloat(form.pickupLat),
          longitude: parseFloat(form.pickupLng),
        },
        dropoff: {
          latitude: parseFloat(form.dropoffLat),
          longitude: parseFloat(form.dropoffLng),
        },
        destination_type: form.destinationType,
        requested_datetime: new Date(form.requestedDatetime).toISOString(),
        parish_id: form.parishId ? Number(form.parishId) : undefined,
        notes: form.notes || undefined,
        passenger_count: form.passengerCount,
      };

      const created = await createRideRequest(token, payload);
      setRequestMessage("Ride request created.");
      setMyRequests((prev) => [created, ...prev]);
      setForm((prev) => ({
        ...prev,
        notes: "",
        passengerCount: 1,
      }));
    } catch (err) {
      setRequestError((err as Error).message || "Unable to create ride request.");
    } finally {
      setRequestLoading(false);
    }
  };

  const handleAcceptRide = async (rideRequestId: number) => {
    if (!token) return;
    setAcceptingId(rideRequestId);
    setDriverError(null);
    try {
      const ride = await acceptRideRequest(token, rideRequestId);
      setOpenRequests((prev) => prev.filter((req) => req.id !== rideRequestId));
      setAssignedRides((prev) => [ride, ...prev]);
    } catch (err) {
      setDriverError((err as Error).message || "Unable to accept ride.");
    } finally {
      setAcceptingId(null);
    }
  };

  const handleUpdateRideStatus = async (rideId: number, status: Ride["status"]) => {
    if (!token) return;
    setStatusUpdating(rideId);
    setDriverError(null);
    try {
      const updated = await updateRideStatus(token, rideId, status);
      setAssignedRides((prev) =>
        prev.map((ride) => (ride.id === rideId ? updated : ride))
      );
    } catch (err) {
      setDriverError((err as Error).message || "Unable to update ride status.");
    } finally {
      setStatusUpdating(null);
    }
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

        {isRider && (
          <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 space-y-4">
            <div className="flex items-start justify-between gap-2">
              <div>
                <h2 className="text-sm font-semibold text-slate-200">
                  Request a ride
                </h2>
                <p className="text-xs text-slate-400">
                  Provide pickup/dropoff coordinates for now; we&apos;ll add maps next.
                </p>
              </div>
              <span className="text-[10px] uppercase tracking-wide text-slate-500">
                Rider flow
              </span>
            </div>

            <form className="space-y-3" onSubmit={handleRideRequestSubmit}>
              {requestError && (
                <p className="text-xs text-red-300">{requestError}</p>
              )}
              {requestMessage && (
                <p className="text-xs text-emerald-300">{requestMessage}</p>
              )}

              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-lg border border-slate-800 p-3">
                  <p className="text-xs font-semibold text-slate-300">
                    Pickup (lat / lng)
                  </p>
                  <div className="mt-2 grid gap-2 sm:grid-cols-2">
                    <input
                      required
                      inputMode="decimal"
                      value={form.pickupLat}
                      onChange={(e) => setForm((p) => ({ ...p, pickupLat: e.target.value }))}
                      className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                      aria-label="Pickup latitude"
                    />
                    <input
                      required
                      inputMode="decimal"
                      value={form.pickupLng}
                      onChange={(e) => setForm((p) => ({ ...p, pickupLng: e.target.value }))}
                      className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                      aria-label="Pickup longitude"
                    />
                  </div>
                </div>

                <div className="rounded-lg border border-slate-800 p-3">
                  <p className="text-xs font-semibold text-slate-300">
                    Dropoff (lat / lng)
                  </p>
                  <div className="mt-2 grid gap-2 sm:grid-cols-2">
                    <input
                      required
                      inputMode="decimal"
                      value={form.dropoffLat}
                      onChange={(e) => setForm((p) => ({ ...p, dropoffLat: e.target.value }))}
                      className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                      aria-label="Dropoff latitude"
                    />
                    <input
                      required
                      inputMode="decimal"
                      value={form.dropoffLng}
                      onChange={(e) => setForm((p) => ({ ...p, dropoffLng: e.target.value }))}
                      className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                      aria-label="Dropoff longitude"
                    />
                  </div>
                </div>
              </div>

              <div className="grid gap-3 sm:grid-cols-2">
                <label className="text-xs font-semibold text-slate-300 space-y-1">
                  Destination type
                  <select
                    value={form.destinationType}
                    onChange={(e) =>
                      setForm((p) => ({
                        ...p,
                        destinationType: e.target.value as RideRequest["destination_type"],
                      }))
                    }
                    className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="mass">Mass</option>
                    <option value="confession">Confession</option>
                    <option value="prayer_event">Prayer event</option>
                    <option value="social">Social</option>
                    <option value="other">Other</option>
                  </select>
                </label>

                <label className="text-xs font-semibold text-slate-300 space-y-1">
                  Requested time
                  <input
                    type="datetime-local"
                    value={form.requestedDatetime}
                    onChange={(e) =>
                      setForm((p) => ({ ...p, requestedDatetime: e.target.value }))
                    }
                    className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </label>
              </div>

              <div className="grid gap-3 sm:grid-cols-2">
                <label className="text-xs font-semibold text-slate-300 space-y-1">
                  Parish (optional)
                  <select
                    value={form.parishId}
                    onChange={(e) => setForm((p) => ({ ...p, parishId: e.target.value }))}
                    className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="">Select parish</option>
                    {parishes.map((parish) => (
                      <option key={parish.id} value={parish.id}>
                        {parish.name}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="text-xs font-semibold text-slate-300 space-y-1">
                  Passengers
                  <input
                    type="number"
                    min={1}
                    max={6}
                    value={form.passengerCount}
                    onChange={(e) =>
                      setForm((p) => ({ ...p, passengerCount: Number(e.target.value) }))
                    }
                    className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  />
                </label>
              </div>

              <label className="text-xs font-semibold text-slate-300 space-y-1">
                Notes (optional)
                <textarea
                  value={form.notes}
                  onChange={(e) => setForm((p) => ({ ...p, notes: e.target.value }))}
                  className="block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  rows={3}
                />
              </label>

              <button
                type="submit"
                disabled={requestLoading}
                className="inline-flex items-center justify-center rounded-md bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-slate-950 shadow-sm hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950"
              >
                {requestLoading ? "Submitting..." : "Submit ride request"}
              </button>
            </form>

            <div className="pt-2">
              <h3 className="text-xs font-semibold text-slate-300">
                Recent requests
              </h3>
              {myRequests.length === 0 ? (
                <p className="text-xs text-slate-500 mt-1">
                  No ride requests yet. Submit one above.
                </p>
              ) : (
                <ul className="mt-2 space-y-2">
                  {myRequests.map((req) => (
                    <li
                      key={req.id}
                      className="rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-2"
                    >
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-semibold text-slate-200 capitalize">
                          {req.destination_type.replace("_", " ")}
                        </span>
                        <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] uppercase tracking-wide text-slate-300">
                          {req.status}
                        </span>
                      </div>
                      <p className="mt-1 text-[11px] text-slate-400">
                        {new Date(req.requested_datetime).toLocaleString()}
                      </p>
                      {req.notes && (
                        <p className="mt-1 text-[11px] text-slate-300">{req.notes}</p>
                      )}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </section>
        )}

        {isDriver && (
          <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 space-y-4">
            <div className="flex items-start justify-between gap-2">
              <div>
                <h2 className="text-sm font-semibold text-slate-200">Driver queue</h2>
                <p className="text-xs text-slate-400">
                  View open requests and update the status of rides you&apos;ve accepted.
                </p>
              </div>
              <span className="text-[10px] uppercase tracking-wide text-slate-500">
                Driver flow
              </span>
            </div>

            {driverError && (
              <p className="text-xs text-red-300" role="alert">
                {driverError}
              </p>
            )}

            <div className="grid gap-3 lg:grid-cols-2">
              <div className="rounded-lg border border-slate-800 bg-slate-900/70 p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-slate-300">
                    Open requests
                  </h3>
                  {driverLoading && (
                    <span className="text-[10px] text-slate-400">Loading…</span>
                  )}
                </div>
                {openRequests.length === 0 ? (
                  <p className="text-[11px] text-slate-500">
                    No open requests right now.
                  </p>
                ) : (
                  <ul className="space-y-2">
                    {openRequests.map((req) => (
                      <li
                        key={req.id}
                        className="rounded-md border border-slate-800 bg-slate-950/50 p-3"
                      >
                        <div className="flex items-center justify-between">
                          <p className="text-xs font-semibold text-slate-200 capitalize">
                            {req.destination_type.replace("_", " ")}
                          </p>
                          <span className="text-[10px] text-slate-400">
                            {new Date(req.requested_datetime).toLocaleString()}
                          </span>
                        </div>
                        <p className="mt-1 text-[11px] text-slate-400">
                          {req.passenger_count} passenger
                          {req.passenger_count > 1 ? "s" : ""}
                        </p>
                        {req.notes && (
                          <p className="mt-1 text-[11px] text-slate-300">{req.notes}</p>
                        )}
                        <button
                          type="button"
                          onClick={() => handleAcceptRide(req.id)}
                          disabled={acceptingId === req.id}
                          className="mt-2 inline-flex items-center justify-center rounded-md bg-emerald-500 px-3 py-1.5 text-[11px] font-semibold text-slate-950 shadow-sm hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900"
                        >
                          {acceptingId === req.id ? "Accepting..." : "Accept request"}
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-900/70 p-3 space-y-2">
                <div className="flex items-center justify-between">
                  <h3 className="text-xs font-semibold text-slate-300">
                    Assigned rides
                  </h3>
                  {driverLoading && (
                    <span className="text-[10px] text-slate-400">Loading…</span>
                  )}
                </div>
                {assignedRides.length === 0 ? (
                  <p className="text-[11px] text-slate-500">
                    You have no active rides yet.
                  </p>
                ) : (
                  <ul className="space-y-2">
                    {assignedRides.map((ride) => (
                      <li
                        key={ride.id}
                        className="rounded-md border border-slate-800 bg-slate-950/50 p-3 space-y-2"
                      >
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-semibold text-slate-200">Ride #{ride.id}</span>
                          <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[10px] uppercase tracking-wide text-slate-300">
                            {ride.status}
                          </span>
                        </div>
                        <div className="flex items-center justify-between text-[11px] text-slate-400">
                          <span>
                            Request #{ride.ride_request_id} • Rider {ride.rider_id}
                          </span>
                          <span>
                            {new Date(ride.accepted_at).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {(
                            [
                              "driver_enroute",
                              "arrived",
                              "picked_up",
                              "in_progress",
                              "completed",
                              "cancelled",
                            ] as Ride["status"][]
                          ).map((status) => (
                            <button
                              key={status}
                              type="button"
                              onClick={() => handleUpdateRideStatus(ride.id, status)}
                              disabled={statusUpdating === ride.id}
                              className="rounded-md border border-slate-700 px-3 py-1 text-[11px] text-slate-200 hover:bg-slate-800 disabled:opacity-60"
                            >
                              {status.replace("_", " ")}
                            </button>
                          ))}
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </section>
        )}

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


