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
      const { sex, age, goal, level } = await request.json();

      // 2. Call Google Gemini 1.5 Flash (Free Tier)
      const API_KEY = env.GEMINI_API_KEY;
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

      const prompt = `You are a professional fitness coach for the app "FirstRep". 
      Generate a customized 3-day workout plan for a ${age} year old ${sex} with the goal of "${goal}" and a training level of "${level}".
      
      Return ONLY a JSON object with this exact structure:
      {
        "name": "Plan Name",
        "schedule": "X days/week",
        "reasoning": "1-2 sentences on why this fits them",
        "workout": [
          {"exercise": "Name", "sets": 3, "reps": "10", "rest": "60s"}
        ]
      }
      
      Only include these exercises: Barbell Squat, Bench Press, Barbell Row, Overhead Press, Lat Pulldown, Goblet Squat, Dumbbell RDL, Seated Cable Row, Glute Bridges, Deadlift.`;

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
