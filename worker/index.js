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
BARBELL: Barbell Squat, Bench Press, Deadlift, Overhead Press, Barbell Row, Romanian Deadlift, Front Squat, Incline Bench Press, Close-Grip Bench Press, Barbell Curl, Skull Crushers, Sumo Deadlift, Hip Thrust
DUMBBELL: Dumbbell Press, Dumbbell Bench Press, Dumbbell Incline Press, Dumbbell Row, Dumbbell Lunges, Dumbbell RDL, Dumbbell Shoulder Press, Dumbbell Curl, Hammer Curl, Lateral Raises, Dumbbell Fly, Goblet Squat, Dumbbell Tricep Extension, Rear Delt Fly, Bulgarian Split Squat
CABLE/MACHINE: Lat Pulldown, Seated Cable Row, Cable Fly, Tricep Pushdowns, Face Pulls, Leg Press, Leg Curls, Leg Extension, Hack Squat, Cable Lateral Raise
BODYWEIGHT: Pushups, Air Squats, Burpees, Jumping Jacks, Mountain Climbers, Pull-Ups, Chin-Ups, Dips, Weighted Dips, Plank, Russian Twist, Hanging Leg Raise, Bicycle Crunches, Dead Bug, Glute Bridges, Calf Raises, Step-ups, Box Jumps, Kettlebell Swing, Battle Ropes`;

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
