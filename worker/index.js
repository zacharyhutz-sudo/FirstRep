export default {
  async fetch(request, env) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
    if (request.method !== "POST") return new Response("Not allowed", { status: 405 });

    try {
      const body = await request.json();
      const API_KEY = env.GEMINI_API_KEY;
      const url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + API_KEY;

      const promptText = `You are a professional fitness coach for the app "FirstRep". 
      Generate a customized workout plan based on these user stats:
      - Age: ${body.age}
      - Biological Sex: ${body.sex}
      - Goal: ${body.goal}
      - Equipment Available: ${body.equipment}
      - Schedule: ${body.daysPerWeek} days/week, ${body.sessionTime} mins/session
      - Experience: ${body.experience} (Last workout: ${body.lastWorkout})
      - Injury/Pain: ${body.injuries}
      
      CRITICAL: You must return a plan for EXACTLY ${body.daysPerWeek} different days (Day 1, Day 2, etc.) to match their requested schedule.
      
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
      
      Use ONLY these exercises (choose based on equipment): 
      - Barbell: Barbell Squat, Bench Press, Deadlift
      - Dumbbell: Dumbbell Press, Dumbbell Row, Dumbbell Lunges
      - Bodyweight/Cardio: Pushups, Air Squats, Burpees, Jumping Jacks, Mountain Climbers
      - Machines: Lat Pulldown`;

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
        headers: corsHeaders
      });
    }
  }
};
