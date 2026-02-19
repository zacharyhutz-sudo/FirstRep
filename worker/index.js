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

      // 1. WORKOUT GENERATION LOGIC - USE DISTILLED DATABASE
      // This block MUST return a response to avoid falling through to Gemini
      if (body.age !== undefined && !body.query) {
        try {
          const userAge = parseInt(body.age);
          let ageBracket = "Adult";
          if (userAge < 30) ageBracket = "Young Adult";
          else if (userAge > 55) ageBracket = "Senior";
          
          const rawExp = body.experience || body.experienceLevel || "Beginner";
          const experience = (rawExp.toLowerCase().includes("beginner")) ? "Beginner" : "Experienced";
          
          const rawEquip = body.equipment || "Full Gym";
          let equipment = "Full Gym";
          if (rawEquip.toLowerCase().includes("dumbell") || rawEquip.toLowerCase().includes("dumbbell")) {
            equipment = "Dumbbells Only";
          } else if (rawEquip.toLowerCase().includes("bodyweight") || rawEquip.toLowerCase().includes("body weight")) {
            equipment = "Bodyweight Only";
          } else if (rawEquip.toLowerCase().includes("home")) {
            equipment = "Home Gym";
          } else if (rawEquip.toLowerCase().includes("minimal")) {
            equipment = "Minimal Equipment";
          }
          
          const rawGoal = body.goal || "Build Muscle";
          let goal = "Muscle Growth";
          if (rawGoal.toLowerCase().includes("strength")) {
            goal = "Strength";
          } else if (rawGoal.toLowerCase().includes("loss") || rawGoal.toLowerCase().includes("weight")) {
            goal = "Fat Loss";
          }
          
          const daysCount = parseInt(body.daysPerWeek) || parseInt(body.days) || 3;
          const split = body.split || "Full Body";
          const version = body.version || "Version A"; 
          
          const dbResponse = await fetch("https://raw.githubusercontent.com/zacharyhutz-sudo/FirstRep/main/src/data/distilled-programs.json");
          if (!dbResponse.ok) throw new Error("DB Fetch failed");
          const database = await dbResponse.json();

          const planMatch = database.find(p => 
            p.metadata.age === ageBracket &&
            p.metadata.experience === experience &&
            p.metadata.equipment === equipment &&
            p.metadata.goal === goal &&
            p.metadata.days === daysCount &&
            p.metadata.split === split &&
            p.metadata.version === version
          );

          if (planMatch) {
            return new Response(JSON.stringify({
              name: planMatch.program_name,
              schedule: planMatch.metadata.days + " days/week",
              reasoning: planMatch.reasoning,
              days: planMatch.days
            }), {
              headers: { ...corsHeaders, "Content-Type": "application/json" },
            });
          } else {
             // If no exact match, return a helpful error instead of calling Gemini
             return new Response(JSON.stringify({ 
               error: "No matching pre-generated plan found.",
               debug: { ageBracket, experience, equipment, goal, daysCount, version }
             }), { status: 404, headers: corsHeaders });
          }
        } catch (e) {
          return new Response(JSON.stringify({ error: "Database system error: " + e.message }), {
            status: 500,
            headers: corsHeaders
          });
        }
      }

      if (!API_KEY) throw new Error("GEMINI_API_KEY is missing in worker environment");
      
      // Routing based on request data
      if (body.query) {
        let query = body.query.trim();
        const USDA_KEY = env.USDA_API_KEY || "nkbewHWAcNS5jFZuP9Hfs6SEgj2bGoiAdLNDmg6N"; // Using provided key

        // RUN SEARCHES IN PARALLEL
        const [usdaResults, aiResults] = await Promise.all([
          // 1. USDA FOODDATA CENTRAL
          (async () => {
            try {
              const usdaUrl = `https://api.nal.usda.gov/fdc/v1/foods/search?query=${encodeURIComponent(query)}&pageSize=8&api_key=${USDA_KEY}`;
              const res = await fetch(usdaUrl);
              const data = await res.json();
              if (!data.foods) return [];
              
              return data.foods.map(f => {
                const getNutrient = (id) => f.foodNutrients.find(n => n.nutrientId === id || n.nutrientNumber === id.toString())?.value || 0;
                // USDA Nutrient IDs: 1008 (Calories), 1003 (Protein), 1005 (Carbs), 1004 (Fat)
                return {
                  id: "usda_" + f.fdcId,
                  name: f.description.toLowerCase().replace(/\b\w/g, l => l.toUpperCase()),
                  unit: f.servingSize ? `${f.servingSize}${f.servingSizeUnit || 'g'}` : "100g",
                  calories: Math.round(getNutrient(1008)),
                  protein: parseFloat(getNutrient(1003).toFixed(1)),
                  carbs: parseFloat(getNutrient(1005).toFixed(1)),
                  fat: parseFloat(getNutrient(1004).toFixed(1)),
                  source: "USDA"
                };
              });
            } catch (e) { return []; }
          })(),

          // 2. GEMINI AI (Fallback/Smart Matching)
          (async () => {
            try {
              const searchUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=${API_KEY}`;
              const searchPrompt = `You are a nutrition database API. Return a JSON array of 5 food items matching: "${query}".
              Focus on items NOT likely to be in a government database (branded snacks, specific restaurant meals, protein bars).
              Structure: [{"id": "ai_unique", "name": "Food Name (Brand)", "unit": "serving size", "calories": 100, "protein": 10, "carbs": 20, "fat": 5}]
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
              const aiText = aiData.candidates[0].content.parts[0].text.replace(/```json\s?|```/g, "").trim();
              const items = JSON.parse(aiText);
              return items.map(item => ({ ...item, source: "AI" }));
            } catch (e) { return []; }
          })()
        ]);

        const combined = [...usdaResults, ...aiResults].slice(0, 10);
        return new Response(JSON.stringify(combined), {
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      // WORKOUT GENERATION LOGIC (Defaulting to gemini-2.0-flash-lite for stability/rate limits)
      const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=${API_KEY}`;

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
