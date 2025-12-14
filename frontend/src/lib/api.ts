/**
 * API client for Catholic Ride Share backend
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

// Types
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string | null;
  role: "rider" | "driver" | "both" | "admin";
  parish_id?: number | null;
  profile_photo_url?: string | null;
  is_active: boolean;
  is_verified: boolean;
  last_known_latitude?: number | null;
  last_known_longitude?: number | null;
}

export interface Parish {
  id: number;
  name: string;
  address?: string | null;
  city?: string | null;
  state?: string | null;
  zip_code?: string | null;
  latitude?: number | null;
  longitude?: number | null;
}

export interface RideRequest {
  id: number;
  rider_id: number;
  pickup_latitude: number;
  pickup_longitude: number;
  dropoff_latitude: number;
  dropoff_longitude: number;
  destination_type: "mass" | "confession" | "prayer_event" | "social" | "other";
  parish_id?: number | null;
  requested_datetime: string;
  notes?: string | null;
  passenger_count: number;
  status: "pending" | "accepted" | "in_progress" | "completed" | "cancelled";
  created_at: string;
  updated_at: string;
}

export interface Ride {
  id: number;
  ride_request_id: number;
  driver_id: number;
  rider_id: number;
  status:
    | "accepted"
    | "driver_enroute"
    | "arrived"
    | "picked_up"
    | "in_progress"
    | "completed"
    | "cancelled";
  accepted_at: string;
  started_at?: string | null;
  completed_at?: string | null;
}

// Helper for API requests
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed: ${response.status}`);
  }

  return response.json();
}

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Bearer ${token}` };
}

// Auth endpoints
export async function login(
  email: string,
  password: string
): Promise<{ access_token: string; token_type: string }> {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData.toString(),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Login failed");
  }

  return response.json();
}

export async function register(data: {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role?: string;
}): Promise<User> {
  return apiFetch<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getCurrentUser(token: string): Promise<User> {
  return apiFetch<User>("/users/me", {
    headers: authHeaders(token),
  });
}

export async function updateCurrentUser(
  token: string,
  data: Partial<{
    first_name: string;
    last_name: string;
    phone: string;
    parish_id: number;
  }>
): Promise<User> {
  return apiFetch<User>("/users/me", {
    method: "PUT",
    headers: authHeaders(token),
    body: JSON.stringify(data),
  });
}

export async function updateLocation(
  token: string,
  latitude: number,
  longitude: number
): Promise<User> {
  return apiFetch<User>("/users/me/location", {
    method: "PUT",
    headers: authHeaders(token),
    body: JSON.stringify({ latitude, longitude }),
  });
}

export async function uploadProfilePhoto(
  token: string,
  file: File
): Promise<User> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/users/me/photo`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Photo upload failed");
  }

  return response.json();
}

export async function deleteProfilePhoto(token: string): Promise<User> {
  return apiFetch<User>("/users/me/photo", {
    method: "DELETE",
    headers: authHeaders(token),
  });
}

// Password reset
export async function forgotPassword(
  email: string
): Promise<{ message: string }> {
  return apiFetch<{ message: string }>("/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function validateResetToken(
  token: string
): Promise<{ valid: boolean }> {
  return apiFetch<{ valid: boolean }>(`/auth/validate-reset-token/${token}`);
}

export async function resetPassword(
  token: string,
  newPassword: string
): Promise<{ message: string }> {
  return apiFetch<{ message: string }>("/auth/reset-password", {
    method: "POST",
    body: JSON.stringify({ token, new_password: newPassword }),
  });
}

// Parishes
export async function listParishes(): Promise<Parish[]> {
  return apiFetch<Parish[]>("/parishes/");
}

// Ride requests
export async function createRideRequest(
  token: string,
  data: {
    pickup: { latitude: number; longitude: number };
    dropoff: { latitude: number; longitude: number };
    destination_type: string;
    requested_datetime: string;
    parish_id?: number;
    notes?: string;
    passenger_count: number;
  }
): Promise<RideRequest> {
  return apiFetch<RideRequest>("/rides/requests", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(data),
  });
}

export async function listMyRideRequests(token: string): Promise<RideRequest[]> {
  return apiFetch<RideRequest[]>("/rides/requests/my", {
    headers: authHeaders(token),
  });
}

export async function listOpenRideRequests(
  token: string
): Promise<RideRequest[]> {
  return apiFetch<RideRequest[]>("/rides/requests/open", {
    headers: authHeaders(token),
  });
}

// Rides
export async function acceptRideRequest(
  token: string,
  rideRequestId: number
): Promise<Ride> {
  return apiFetch<Ride>(`/rides/requests/${rideRequestId}/accept`, {
    method: "POST",
    headers: authHeaders(token),
  });
}

export async function listAssignedRides(token: string): Promise<Ride[]> {
  return apiFetch<Ride[]>("/rides/assigned", {
    headers: authHeaders(token),
  });
}

export async function updateRideStatus(
  token: string,
  rideId: number,
  status: Ride["status"]
): Promise<Ride> {
  return apiFetch<Ride>(`/rides/${rideId}/status`, {
    method: "PUT",
    headers: authHeaders(token),
    body: JSON.stringify({ status }),
  });
}
