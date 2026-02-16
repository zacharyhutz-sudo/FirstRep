import { createClient } from '@supabase/supabase-js';

// Hardcoded for GitHub Pages because environment variables are not available at runtime on static hosts
const supabaseUrl = 'https://mbpirbbsijlejtsjwtkm.supabase.co';
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1icGlyYmJzaWpsZWp0c2p3dGttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg0NTA5OTcsImV4cCI6MjA1NDAyNjk5N30.R_639vN1_9Bv-472-X0-22X379v-2-3_0v-63-X37U';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
