-- Update profiles table with new physical and lifestyle columns
ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS sex text,
ADD COLUMN IF NOT EXISTS age integer,
ADD COLUMN IF NOT EXISTS height integer,
ADD COLUMN IF NOT EXISTS weight integer,
ADD COLUMN IF NOT EXISTS activity_level text,
ADD COLUMN IF NOT EXISTS fitness_goal text;

-- Fix RLS Policies to allow users to insert their own profile during signup
DROP POLICY IF EXISTS "Users can view their own profile." ON profiles;
DROP POLICY IF EXISTS "Users can update their own profile." ON profiles;
DROP POLICY IF EXISTS "Users can insert their own profile." ON profiles;

CREATE POLICY "Users can view their own profile." ON profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update their own profile." ON profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert their own profile." ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
