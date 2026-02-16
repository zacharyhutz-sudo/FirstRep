import { createClient } from '@supabase/supabase-js';

// Accessing environment variables during build time for Astro
const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY;

// Fallback logic for safety
if (!supabaseUrl || !supabaseAnonKey) {
  console.error("Supabase credentials missing! Ensure PUBLIC_SUPABASE_URL and PUBLIC_SUPABASE_ANON_KEY are set.");
}

export const supabase = createClient(supabaseUrl || '', supabaseAnonKey || '');
