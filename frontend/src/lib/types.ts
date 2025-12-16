export type UserRole = "rider" | "driver" | "both" | "admin";

export interface User {
  id: number;
  email: string;
  phone?: string | null;
  first_name: string;
  last_name: string;
  role: UserRole;
  parish_id?: number | null;
  profile_photo_url?: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

