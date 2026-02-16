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

      if (!API_KEY) throw new Error("GEMINI_API_KEY is missing in worker environment");
      
      // Routing based on request data
      if (body.query) {
        const query = body.query.trim();
        const results = [];

        // 1. TRY OPEN FOOD FACTS (OFF) - Best for Branded/UPC
        try {
          const offUrl = `https://world.openfoodfacts.org/cgi/search.pl?search_terms=${encodeURIComponent(query)}&search_simple=1&action=process&json=1&page_size=5`;
          const offRes = await fetch(offUrl, { headers: { "User-Agent": "FirstRep - Web - 1.0" } });
          const offData = await offRes.json();

          if (offData.products && offData.products.length > 0) {
            offData.products.forEach(p => {
              if (p.nutriments && p.nutriments["energy-kcal_100g"]) {
                results.push({
                  id: "off_" + (p.id || p.code),
                  name: `${p.product_name} ${p.brands ? '(' + p.brands + ')' : ''}`.trim(),
                  unit: "100g",
                  calories: Math.round(p.nutriments["energy-kcal_100g"]),
                  protein: p.nutriments.proteins_100g || 0,
                  carbs: p.nutriments.carbohydrates_100g || 0,
                  fat: p.nutriments.fat_100g || 0,
                  source: "OFF"
                });
              }
            });
          }
        } catch (e) {
          console.error("OFF API Error:", e);
        }

        // 2. IF OFF IS EMPTY OR FEW RESULTS, FILL WITH GEMINI (Best for Restaurants/Generic)
        if (results.length < 3) {
          // Fixed model path
          const searchUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;
          const searchPrompt = `You are a nutrition database API. Return a JSON array of 5 food items matching: "${query}".
          Focus on restaurant meals or generic items if brands are missing.
          
          Structure:
          [
            {
              "id": "ai_unique_string",
              "name": "Food Name (Restaurant Name if applicable)",
              "unit": "standard serving size",
              "calories": 100,
              "protein": 10,
              "carbs": 20,
              "fat": 5
            }
          ]
          Return ONLY the JSON array.`;

          const aiRes = await fetch(searchUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              contents: [{ parts: [{ text: searchPrompt }] }],
              generationConfig: { response_mime_type: "application/json" }
            }),
          });
          const aiData = await aiRes.json();
          if (aiData.candidates && aiData.candidates[0] && aiData.candidates[0].content && aiData.candidates[0].content.parts[0]) {
            let aiText = aiData.candidates[0].content.parts[0].text;
            aiText = aiText.replace(/```json\s?|```/g, "").trim();
            try {
              const aiItems = JSON.parse(aiText);
              aiItems.forEach(item => {
                item.source = "AI";
                results.push(item);
              });
            } catch (e) {}
          }
        }

        return new Response(JSON.stringify(results.slice(0, 8)), {
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      // WORKOUT GENERATION LOGIC (Fixed model path)
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

      // Safe defaults for mandatory fields
      const age = body.age || 25;
      const sex = body.sex || 'male';
      const goal = body.goal || 'Build Muscle';
      const equipment = body.equipment || 'Full Gym';
      const daysPerWeek = body.daysPerWeek || 3;
      const sessionTime = body.sessionTime || 60;
      const experience = body.experience || 'Beginner';
      const lastWorkout = body.lastWorkout || 'Never';
      const injuries = body.injuries || 'None';

      const promptText = `You are an elite fitness coach. Generate a customized workout plan:
- Age: ${age}
- Sex: ${sex}
- Goal: ${goal}
- Equipment: ${equipment}
- Schedule: ${daysPerWeek} days/week, ${sessionTime} mins/session
- Experience: ${experience}
- Last workout: ${lastWorkout}
- Injury: ${injuries}

Return ONLY a JSON object:
{
  "name": "Plan Name",
  "schedule": "X days/week",
  "reasoning": "Why this plan fits.",
  "days": [
    {
      "day_label": "Day 1",
      "exercises": [{"exercise": "Name", "sets": 3, "reps": "10", "rest": "60s"}]
    }
  ]
}
Use ONLY: ${exerciseList}`;

      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: promptText }] }],
          generationConfig: { response_mime_type: "application/json" }
        }),
      });

      const data = await response.json();
      
      if (!data.candidates || !data.candidates[0] || !data.candidates[0].content || !data.candidates[0].content.parts[0]) {
        throw new Error("Invalid AI response: " + JSON.stringify(data));
      }

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
