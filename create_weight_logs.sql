-- Create weight_logs table
create table weight_logs (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users on delete cascade not null,
  logged_at date default current_date not null,
  weight float not null, -- in lbs
  calories_burned integer, -- manual entry for activity
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  unique(user_id, logged_at) -- one entry per day
);

-- Enable RLS
alter table weight_logs enable row level security;

-- Policy
create policy "Users can manage their own weight logs." on weight_logs 
  for all using (auth.uid() = user_id);
