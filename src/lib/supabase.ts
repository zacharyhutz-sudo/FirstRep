import { createClient } from '@supabase/supabase-js';

// Reverting to env variables to avoid further manual key errors.
// These MUST be set in the GitHub repository secrets/variables for the build to work.
const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
