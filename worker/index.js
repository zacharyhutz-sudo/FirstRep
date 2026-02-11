/**
 * FirstRep Cloudflare Worker
 * Generates personalized workout plans via Gemini AI.
 */
export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
    if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });

    try {
      const body = await request.json();
      const API_KEY = env.GEMINI_API_KEY;
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

      // Available exercises grouped by equipment requirement
      const exerciseList = `
BARBELL: Barbell Squat, Bench Press, Deadlift, Overhead Press, Barbell Row, Romanian Deadlift, Front Squat, Incline Bench Press, Close-Grip Bench Press, Barbell Curl, Skull Crushers, Sumo Deadlift, Hip Thrust, T-Bar Row, Barbell Ab Rollout, Barbell Ab Rollout - On Knees, Barbell Curls Lying Against An Incline, Barbell Full Squat, Anti-Gravity Press
DUMBBELL: Dumbbell Press, Dumbbell Bench Press, Dumbbell Incline Press, Dumbbell Row, Dumbbell Lunges, Dumbbell RDL, Dumbbell Shoulder Press, Dumbbell Curl, Hammer Curl, Lateral Raises, Dumbbell Fly, Goblet Squat, Dumbbell Tricep Extension, Rear Delt Fly, Bulgarian Split Squat, Arnold Press, Zottman Curl, Alternate Hammer Curl, Alternate Incline Dumbbell Curl, Alternating Deltoid Raise, Around The Worlds
CABLE/MACHINE: Lat Pulldown, Seated Cable Row, Cable Fly, Tricep Pushdowns, Face Pulls, Leg Press, Leg Curls, Leg Extension, Hack Squat, Cable Lateral Raise, Cable Overhead Tricep Extension, Cable Bicep Curl, Cable Woodchoppers, Straight Arm Pulldown, Hammer Strength Press, Pec Deck Fly, Cable Pull-Through, Close Grip Pulldown, Preacher Curl, Ab Crunch Machine, Alternating Cable Shoulder Press
RESISTANCE_BAND: Band Good Morning, Band Good Morning (Pull Through), Band Hip Adductions, Band Pull Apart, Band Skull Crusher, Back Flyes - With Bands, Band Assisted Pull-Up, Resistance Band Rows
KETTLEBELL: Kettlebell Swing, Alternating Floor Press, Alternating Hang Clean, Alternating Kettlebell Press, Alternating Kettlebell Row, Alternating Renegade Row, Advanced Kettlebell Windmill
BODYWEIGHT: Pushups, Air Squats, Burpees, Jumping Jacks, Mountain Climbers, Pull-Ups, Chin-Ups, Dips, Weighted Dips, Plank, Russian Twist, Hanging Leg Raise, Bicycle Crunches, Dead Bug, Glute Bridges, Calf Raises, Step-ups, Box Jumps, Battle Ropes, Sit-ups, Crunches, Diamond Pushups, Wide Grip Pushups, Leg Raises, Walking Lunges, 3/4 Sit-Up, 90/90 Hamstring, Ab Roller, Alternate Heel Touchers, Alternate Leg Diagonal Bound, Ankle Circles, Ankle On The Knee, Arm Circles
FUNCTIONAL/OTHER: Atlas Stone Trainer, Atlas Stones, Axle Deadlift, Backward Drag, Backward Medicine Ball Throw, Balance Board, Ball Leg Curl
CARDIO: Running (Treadmill), Elliptical Trainer, Rowing Machine, Elevated Treadmill Walk, Stationary Bike`;

      const promptText = `You are an elite, safety-conscious fitness coach for the app "FirstRep". 
Generate a customized workout plan based on these user stats:
- Age: ${body.age}
- Biological Sex: ${body.sex}
- Goal: ${body.goal}
- Equipment Available: ${body.equipment}
- Schedule: ${body.daysPerWeek} days/week, ${body.sessionTime} mins/session
- Experience: ${body.experience} (Last workout: ${body.lastWorkout})
- Injury/Pain: ${body.injuries}

--- CRITICAL HIERARCHY OF ADAPTATION (MANDATORY) ---

1. SAFETY FIRST (Pain/Injury):
   - BACK PAIN: ABSOLUTELY NO spinal compression. Banned: Barbell Squat, Deadlift, Overhead Press, Romanian Deadlift. Replace with: Plank, Dead Bug, Bird-Dog, Glute Bridges.
   - KNEE PAIN: Banned: Lunges, Deep Squats, Box Jumps. Replace with: Box Step-ups (low box), Glute Bridges, Wall Sits.
   - SHOULDER PAIN: Banned: Overhead Press, Dips, Wide Grip Pushups. Replace with: Floor Press, Lateral Raises (light), Neutral Grip Rows.
   - WRIST PAIN: Banned: Standard Pushups, Front Squats. Replace with: Dumbbell Press (neutral grip), Knuckle Pushups, or Cable work.
   - HIP PAIN: Banned: Deep Sumo Deadlifts, Wide Stance Squats. Replace with: Glute Bridges, Step-ups, or Stationary Bike.
   - NECK PAIN: Banned: Shrugs, Heavy Barbell Back Squats. Replace with: Goblet Squats, Chest-Supported Rows.
   - If any pain is mentioned, the ENTIRE workout must be "Low Impact" and focused on stability. Avoid all high-impact jumping/plyometrics.

2. SENIOR SCALING (Age 65+):
   - OVERRIDE Duration: Regardless of user request, if Age > 65 and Experience is Beginner, limit to 20-25 mins max.
   - Volume: Max 2-3 sets per exercise.
   - Intensity: Focus on "Functional Independence" (Balance, Sit-to-Stand, Grip Strength).

3. DE-CONDITIONING (Last Workout > 3 months ago):
   - If the user hasn't worked out in months, they are "De-conditioned". 
   - Reduction: Reduce requested session time by 30% for the first week.
   - Focus: High reps (15+), low weight, focusing on form over load.

--- VOLUME & FREQUENCY CONSTRAINTS ---
- DO NOT CHANGE the number of days per week. If they requested ${body.daysPerWeek} days, you MUST return exactly ${body.daysPerWeek} days.
- For high-frequency requests (5-6 days) from Beginners or Seniors, reduce the daily load (e.g. fewer sets per day) to ensure recovery, but maintain the requested frequency.

CRITICAL: The "reasoning" field MUST explicitly list every adaptation made (e.g. "Because you mentioned back pain, I removed Deadlifts...").

Return ONLY a JSON object with this structure:
{
  "name": "Plan Name",
  "schedule": "X days/week | Y mins per session",
  "reasoning": "Detailed list of safety adaptations based on age, pain, and time since last workout.",
  "days": [
    {
      "day_label": "Day 1: Title",
      "exercises": [
        {"exercise": "Name", "sets": 3, "reps": "10", "rest": "60s"}
      ]
    }
  ]
}

Use ONLY exercises from this list (choose based on equipment):
${exerciseList}`;

      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: promptText }] }],
          generationConfig: { response_mime_type: "application/json" }
        }),
      });

      const data = await response.json();
      const plan = data.candidates[0].content.parts[0].text;

      return new Response(plan, {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }
  }
};
