-- WORKOUT LOGGING SCHEMA
-- Run these in the Supabase SQL Editor

-- 1. Table for tracking entire workout sessions
CREATE TABLE IF NOT EXISTS completed_workouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    plan_id UUID REFERENCES workout_plans(id) ON DELETE SET NULL,
    workout_name TEXT NOT NULL,
    completed_at TIMESTAMPTZ DEFAULT NOW(),
    duration_minutes INTEGER,
    total_volume_kg NUMERIC DEFAULT 0,
    notes TEXT
);

-- 2. Table for tracking individual sets within those sessions
CREATE TABLE IF NOT EXISTS set_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    completed_workout_id UUID REFERENCES completed_workouts(id) ON DELETE CASCADE,
    exercise_name TEXT NOT NULL,
    weight NUMERIC NOT NULL,
    reps INTEGER NOT NULL,
    set_number INTEGER NOT NULL,
    completed_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Function to calculate current workout streak
CREATE OR REPLACE FUNCTION get_workout_streak(user_uuid UUID)
RETURNS INTEGER AS $$
DECLARE
    streak INTEGER := 0;
    curr_date DATE := CURRENT_DATE;
    last_date DATE;
BEGIN
    -- Check if they worked out today or yesterday to keep streak alive
    SELECT MAX(completed_at::DATE) INTO last_date 
    FROM completed_workouts 
    WHERE user_id = user_uuid;

    IF last_date IS NULL OR (curr_date - last_date) > 1 THEN
        RETURN 0;
    END IF;

    -- Count backwards
    LOOP
        SELECT DISTINCT completed_at::DATE INTO last_date
        FROM completed_workouts
        WHERE user_id = user_uuid AND completed_at::DATE = curr_date;
        
        IF FOUND THEN
            streak := streak + 1;
            curr_date := curr_date - 1;
        ELSE
            EXIT;
        END IF;
    END LOOP;

    RETURN streak;
END;
$$ LANGUAGE plpgsql;
