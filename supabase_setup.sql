# Supabase Schema Setup

Execute these in the Supabase SQL Editor:

```sql
-- Create profiles table
create table profiles (
  id uuid references auth.users on delete cascade primary key,
  updated_at timestamp with time zone,
  username text unique,
  full_name text,
  avatar_url text,
  goal text,
  experience_level text,
  equipment_available text
);

-- Create food_logs table
create table food_logs (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users on delete cascade not null,
  logged_at date default current_date not null,
  meal_type text not null, -- breakfast, lunch, dinner, snacks
  food_name text not null,
  amount float not null,
  calories float not null,
  protein float not null,
  carbs float not null,
  fat float not null,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create workout_plans table
create table workout_plans (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users on delete cascade not null,
  plan_name text not null,
  schedule_summary text,
  plan_data jsonb not null, -- The full JSON of the generated plan
  is_active boolean default true,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Set up Row Level Security (RLS)
alter table profiles enable row level security;
alter table food_logs enable row level security;
alter table workout_plans enable row level security;

-- Policies
create policy "Users can view their own profile." on profiles for select using (auth.uid() = id);
create policy "Users can update their own profile." on profiles for update using (auth.uid() = id);

create policy "Users can manage their own food logs." on food_logs 
  for all using (auth.uid() = user_id);

create policy "Users can manage their own workout plans." on workout_plans 
  for all using (auth.uid() = user_id);
```
