"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import { deleteProfilePhoto, updateCurrentUser, uploadProfilePhoto } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function ProfilePage() {
  const router = useRouter();
  const { user, token, loading, setUser, logout } = useAuth();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [phone, setPhone] = useState("");
  const [saving, setSaving] = useState(false);
  const [photoLoading, setPhotoLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
      return;
    }
    if (user) {
      setFirstName(user.first_name);
      setLastName(user.last_name);
      setPhone(user.phone ?? "");
    }
  }, [loading, user, router]);

  const handleSave = async (e: FormEvent) => {
    e.preventDefault();
    if (!token) return;
    setSaving(true);
    setError(null);
    setMessage(null);
    try {
      const updated = await updateCurrentUser(token, {
        first_name: firstName,
        last_name: lastName,
        phone,
      });
      setUser(updated);
      setMessage("Profile updated.");
    } catch (err) {
      setError((err as Error).message || "Unable to update profile");
    } finally {
      setSaving(false);
    }
  };

  const handlePhotoChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!token) return;
    const file = event.target.files?.[0];
    if (!file) return;
    setPhotoLoading(true);
    setError(null);
    setMessage(null);
    try {
      const updated = await uploadProfilePhoto(token, file);
      setUser(updated);
      setMessage("Profile photo updated.");
    } catch (err) {
      setError((err as Error).message || "Unable to upload photo");
    } finally {
      setPhotoLoading(false);
    }
  };

  const handleRemovePhoto = async () => {
    if (!token) return;
    setPhotoLoading(true);
    setError(null);
    setMessage(null);
    try {
      const updated = await deleteProfilePhoto(token);
      setUser(updated);
      setMessage("Profile photo removed.");
    } catch (err) {
      setError((err as Error).message || "Unable to remove photo");
    } finally {
      setPhotoLoading(false);
    }
  };

  if (loading || (!user && !error)) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-100">
        <p className="text-sm text-slate-300">Loading your profile...</p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/80">
        <div className="mx-auto max-w-4xl px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold">Your profile</h1>
            <p className="text-xs text-slate-400">
              Logged in as {user.email}{" "}
              {!user.is_verified && (
                <span className="ml-1 font-medium text-amber-300">
                  (email not verified)
                </span>
              )}
            </p>
          </div>
          <button
            type="button"
            onClick={logout}
            className="text-xs rounded-md border border-slate-700 px-3 py-1.5 text-slate-200 hover:bg-slate-800"
          >
            Sign out
          </button>
        </div>
      </header>

      <div className="mx-auto max-w-4xl px-4 py-8 grid gap-8 md:grid-cols-[minmax(0,2fr)_minmax(0,1.2fr)]">
        <section>
          <h2 className="text-sm font-semibold text-slate-300 mb-3">
            Basic information
          </h2>
          <form onSubmit={handleSave} className="space-y-4">
            {error && (
              <div className="rounded-md bg-red-900/30 border border-red-700 px-3 py-2 text-xs text-red-200">
                {error}
              </div>
            )}
            {message && (
              <div className="rounded-md bg-emerald-900/30 border border-emerald-700 px-3 py-2 text-xs text-emerald-200">
                {message}
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="first_name"
                  className="block text-xs font-medium text-slate-300"
                >
                  First name
                </label>
                <input
                  id="first_name"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  className="mt-1 block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
              <div>
                <label
                  htmlFor="last_name"
                  className="block text-xs font-medium text-slate-300"
                >
                  Last name
                </label>
                <input
                  id="last_name"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  className="mt-1 block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="phone"
                className="block text-xs font-medium text-slate-300"
              >
                Phone
              </label>
              <input
                id="phone"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="mt-1 block w-full rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <button
              type="submit"
              disabled={saving}
              className="inline-flex items-center justify-center rounded-md bg-emerald-500 px-4 py-2.5 text-sm font-semibold text-slate-950 shadow-sm hover:bg-emerald-400 disabled:opacity-60 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950"
            >
              {saving ? "Saving..." : "Save changes"}
            </button>
          </form>
        </section>

        <section className="space-y-4">
          <h2 className="text-sm font-semibold text-slate-300">
            Profile photo
          </h2>
          <div className="flex items-center gap-4">
            <div className="h-20 w-20 rounded-full border border-slate-700 bg-slate-800 flex items-center justify-center overflow-hidden">
              {user.profile_photo_url ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  src={user.profile_photo_url}
                  alt="Profile"
                  className="h-full w-full object-cover"
                />
              ) : (
                <span className="text-sm text-slate-400">No photo</span>
              )}
            </div>
            <div className="flex flex-col gap-2">
              <label className="inline-flex items-center gap-2 text-xs font-medium text-emerald-300 hover:text-emerald-200 cursor-pointer">
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="hidden"
                  onChange={handlePhotoChange}
                />
                {photoLoading ? "Uploading..." : "Upload new photo"}
              </label>
              {user.profile_photo_url && (
                <button
                  type="button"
                  onClick={handleRemovePhoto}
                  disabled={photoLoading}
                  className="text-xs text-slate-400 hover:text-slate-200"
                >
                  Remove current photo
                </button>
              )}
              <p className="text-[10px] text-slate-500">
                JPEG, PNG, or WebP up to 5MB. We store a 500×500 thumbnail for
                privacy and performance.
              </p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}


