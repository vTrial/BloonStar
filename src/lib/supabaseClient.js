import { createClient } from "@supabase/supabase-js"

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_API_KEY

// Create a Supabase client instance
const supabase = createClient(supabaseUrl, supabaseKey)
export { supabase }
