-- Add daily_goals column to profiles table to store JSON macros/calories
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS daily_goals JSONB DEFAULT '{"calories": 2500, "protein": 180, "carbs": 250, "fat": 70}'::jsonb;
