import { createClient } from '@supabase/supabase-js';

// Hardcoded specifically to bypass GitHub Pages environment variable stripping. 
// These are PUBLIC anon keys, safe to be in client-side code.
const supabaseUrl = 'https://mbpirbbsijlejtsjwtkm.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1icGlyYmJzaWpsZWp0c2p3dGttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0NTA5OTcsImV4cCI6MjA1NDAyNjk5N30.C3C3YvX3N3V3Z3Y3X3V3Z3Y3X3V3Z3Y3X3V3Z3Y3X3U';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
