export default {
  async fetch(request, env) {
    // 1. Handle CORS (Allow the website to talk to this worker)
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    try {
      const body = await request.json();

      // 2. Call Google Gemini 1.5 Flash (Free Tier)
      const API_KEY = env.GEMINI_API_KEY;
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

      const prompt = `You are a professional fitness coach for the app "FirstRep". 
      Generate a customized workout plan based on these user stats:
      - Age: ${body.age}
      - Biological Sex: ${body.sex}
      - Goal: ${body.goal}
      - Equipment Available: ${body.equipment}
      - Schedule: ${body.daysPerWeek} days/week, ${body.sessionTime} mins/session
      - Experience: ${body.experience} level (Last time worked out: ${body.lastWorkout})
      - Injury/Pain: ${body.injuries}
      
      Return ONLY a JSON object with this exact structure:
      {
        "name": "Plan Name",
        "schedule": "X days/week",
        "reasoning": "1-2 sentences on how this plan optimizes for their specific equipment, schedule, and experience level",
        "workout": [
          {"exercise": "Name", "sets": 3, "reps": "10", "rest": "60s"}
        ]
      }
      
      Only include these exercises: Barbell Squat, Bench Press, Barbell Row, Overhead Press, Lat Pulldown, Goblet Squat, Dumbbell RDL, Seated Cable Row, Glute Bridges, Deadlift. If equipment is limited (e.g. dumbbells only), choose only the exercises that can be performed with what they have.`;

      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
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
  },
};
