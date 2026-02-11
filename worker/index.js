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

      const promptText = `You are a professional fitness coach for the app "FirstRep". 
Generate a customized workout plan based on these user stats:
- Age: ${body.age}
- Biological Sex: ${body.sex}
- Goal: ${body.goal}
- Equipment Available: ${body.equipment}
- Schedule: ${body.daysPerWeek} days/week, ${body.sessionTime} mins/session
- Experience: ${body.experience} (Last workout: ${body.lastWorkout})
- Injury/Pain: ${body.injuries}

CRITICAL: Return a plan for EXACTLY ${body.daysPerWeek} different days.

Return ONLY a JSON object with this structure:
{
  "name": "Plan Name",
  "schedule": "${body.daysPerWeek} days/week",
  "reasoning": "Explain why this fits their equipment, schedule, and experience.",
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
