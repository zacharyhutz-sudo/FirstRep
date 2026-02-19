import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Debug Helper for Zach
export async function getTableSchema(tableName: string) {
    const { data, error } = await supabase
        .from(tableName)
        .select('*')
        .limit(1);
    
    if (error) {
        console.error(`Error inspecting ${tableName}:`, error);
        return null;
    }
    return data && data.length > 0 ? Object.keys(data[0]) : "Table empty, cannot infer columns.";
}
