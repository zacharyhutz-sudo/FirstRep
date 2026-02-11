#!/usr/bin/env python3
"""
Generate massive expansion of FirstRep exercise DB and workout templates.
"""
import json, copy

###############################################################################
# 1. EXPANDED EXERCISE DATABASE
###############################################################################

NEW_EXERCISES = [
    # --- BARBELL ---
    {"name": "Barbell Hip Thrust", "muscles": "Glutes, Hamstrings", "equipment": "barbell",
     "instructions": ["Sit on the floor with upper back against a bench.", "Roll a loaded barbell over your hips.", "Drive hips up until fully extended, squeezing glutes at the top.", "Lower with control."],
     "image": ""},
    {"name": "Pendlay Row", "muscles": "Upper Back, Lats, Biceps", "equipment": "barbell",
     "instructions": ["Set barbell on floor, hinge at hips with flat back.", "Grip just outside knees.", "Explosively row bar to lower chest, return to floor each rep."],
     "image": ""},
    {"name": "Barbell Shrug", "muscles": "Traps", "equipment": "barbell",
     "instructions": ["Hold barbell at thigh level with overhand grip.", "Shrug shoulders straight up toward ears.", "Hold briefly at top, lower with control."],
     "image": ""},
    {"name": "Barbell Lunge", "muscles": "Quads, Glutes, Hamstrings", "equipment": "barbell",
     "instructions": ["Place barbell on upper back.", "Step forward into a lunge, lowering rear knee toward floor.", "Push through front heel to return to start."],
     "image": ""},
    {"name": "Zercher Squat", "muscles": "Quads, Glutes, Core, Biceps", "equipment": "barbell",
     "instructions": ["Hold barbell in the crook of your elbows.", "Squat down keeping torso upright.", "Drive through heels to stand."],
     "image": ""},
    {"name": "Deficit Deadlift", "muscles": "Posterior Chain, Quads, Grip", "equipment": "barbell",
     "instructions": ["Stand on a 2-3 inch platform.", "Deadlift with conventional form.", "The extra range of motion increases posterior chain demand."],
     "image": ""},
    {"name": "Pause Squat", "muscles": "Quads, Glutes, Core", "equipment": "barbell",
     "instructions": ["Squat down to parallel or below.", "Pause for 2-3 seconds at the bottom.", "Drive up explosively."],
     "image": ""},
    {"name": "Floor Press", "muscles": "Chest, Triceps", "equipment": "barbell",
     "instructions": ["Lie on floor with barbell in rack or on pins.", "Press up, elbows touch floor each rep.", "Great for lockout strength."],
     "image": ""},
    {"name": "Barbell Good Morning", "muscles": "Hamstrings, Glutes, Lower Back", "equipment": "barbell",
     "instructions": ["Place barbell on upper back.", "Hinge at hips pushing them back, slight knee bend.", "Lower torso until you feel a hamstring stretch.", "Drive hips forward to stand."],
     "image": ""},
    {"name": "Push Press", "muscles": "Shoulders, Triceps, Core", "equipment": "barbell",
     "instructions": ["Start with barbell at shoulders.", "Dip knees slightly, then explosively drive bar overhead.", "Lock out arms fully."],
     "image": ""},
    {"name": "Landmine Press", "muscles": "Shoulders, Upper Chest, Core", "equipment": "barbell",
     "instructions": ["Wedge one end of barbell in a corner or landmine attachment.", "Press the other end overhead at an angle.", "Keep core tight throughout."],
     "image": ""},
    {"name": "Landmine Row", "muscles": "Lats, Upper Back, Biceps", "equipment": "barbell",
     "instructions": ["Straddle the barbell with landmine setup.", "Hinge at hips, row the bar to your chest.", "Squeeze shoulder blades together."],
     "image": ""},
    {"name": "Barbell Reverse Lunge", "muscles": "Quads, Glutes, Hamstrings", "equipment": "barbell",
     "instructions": ["Bar on upper back, step backward into a lunge.", "Lower rear knee toward floor.", "Push through front foot to return."],
     "image": ""},
    {"name": "Snatch-Grip Deadlift", "muscles": "Upper Back, Traps, Posterior Chain", "equipment": "barbell",
     "instructions": ["Use a very wide grip on the barbell.", "Deadlift with flat back; the wide grip increases upper back demand.", "Lock out at the top."],
     "image": ""},
    {"name": "Z Press", "muscles": "Shoulders, Triceps, Core", "equipment": "barbell",
     "instructions": ["Sit on floor with legs extended, barbell at shoulders.", "Press overhead without leaning back.", "Eliminates leg drive, demanding pure shoulder strength."],
     "image": ""},

    # --- DUMBBELL ---
    {"name": "Dumbbell Pullover", "muscles": "Lats, Chest, Serratus", "equipment": "dumbbell",
     "instructions": ["Lie on a bench holding one dumbbell overhead with both hands.", "Lower the weight behind your head in an arc.", "Pull back to start using lats and chest."],
     "image": ""},
    {"name": "Dumbbell Arnold Press", "muscles": "Shoulders, Triceps", "equipment": "dumbbell",
     "instructions": ["Start with dumbbells at chin, palms facing you.", "Rotate palms outward as you press overhead.", "Reverse on the way down."],
     "image": ""},
    {"name": "Dumbbell Front Raise", "muscles": "Front Delts", "equipment": "dumbbell",
     "instructions": ["Hold dumbbells at sides.", "Raise one or both arms in front to shoulder height.", "Lower with control."],
     "image": ""},
    {"name": "Dumbbell Reverse Fly", "muscles": "Rear Delts, Upper Back", "equipment": "dumbbell",
     "instructions": ["Hinge at hips with dumbbells hanging below.", "Raise arms out to sides squeezing shoulder blades.", "Lower slowly."],
     "image": ""},
    {"name": "Dumbbell Shrug", "muscles": "Traps", "equipment": "dumbbell",
     "instructions": ["Hold dumbbells at sides.", "Shrug shoulders up toward ears.", "Hold briefly, lower."],
     "image": ""},
    {"name": "Dumbbell Step-Up", "muscles": "Quads, Glutes", "equipment": "dumbbell",
     "instructions": ["Hold dumbbells at sides.", "Step onto a bench or box.", "Drive through the top foot, bring other foot up.", "Step down with control."],
     "image": ""},
    {"name": "Concentration Curl", "muscles": "Biceps", "equipment": "dumbbell",
     "instructions": ["Sit on bench, brace elbow against inner thigh.", "Curl dumbbell up, squeezing bicep.", "Lower slowly."],
     "image": ""},
    {"name": "Dumbbell Skullcrusher", "muscles": "Triceps", "equipment": "dumbbell",
     "instructions": ["Lie on bench with dumbbells held overhead.", "Bend elbows to lower weights beside head.", "Extend back up."],
     "image": ""},
    {"name": "Incline Dumbbell Curl", "muscles": "Biceps (long head)", "equipment": "dumbbell",
     "instructions": ["Sit on incline bench, arms hanging.", "Curl dumbbells up.", "The incline stretches the long head of the bicep."],
     "image": ""},
    {"name": "Single-Arm Dumbbell Row", "muscles": "Lats, Upper Back, Biceps", "equipment": "dumbbell",
     "instructions": ["Place one knee and hand on bench.", "Row dumbbell to hip with other arm.", "Squeeze at top."],
     "image": ""},
    {"name": "Dumbbell Sumo Squat", "muscles": "Quads, Glutes, Adductors", "equipment": "dumbbell",
     "instructions": ["Wide stance, toes pointed out.", "Hold one dumbbell between legs.", "Squat down keeping chest up."],
     "image": ""},
    {"name": "Dumbbell Chest Press (Floor)", "muscles": "Chest, Triceps", "equipment": "dumbbell",
     "instructions": ["Lie on floor with dumbbells.", "Press up, elbows touch floor each rep.", "Good option without a bench."],
     "image": ""},
    {"name": "Dumbbell Lateral Lunge", "muscles": "Quads, Glutes, Adductors", "equipment": "dumbbell",
     "instructions": ["Hold dumbbells at sides.", "Step wide to one side, sitting back into that hip.", "Push back to center."],
     "image": ""},
    {"name": "Renegade Row", "muscles": "Back, Core, Shoulders", "equipment": "dumbbell",
     "instructions": ["Get in pushup position holding dumbbells.", "Row one dumbbell up while stabilizing.", "Alternate sides."],
     "image": ""},
    {"name": "Dumbbell Thruster", "muscles": "Full Body", "equipment": "dumbbell",
     "instructions": ["Hold dumbbells at shoulders.", "Squat down, then drive up pressing dumbbells overhead.", "One fluid motion."],
     "image": ""},
    {"name": "Dumbbell Calf Raise", "muscles": "Calves", "equipment": "dumbbell",
     "instructions": ["Hold dumbbells at sides.", "Rise onto toes, pause at top.", "Lower slowly."],
     "image": ""},
    {"name": "Dumbbell Wrist Curl", "muscles": "Forearms", "equipment": "dumbbell",
     "instructions": ["Sit on bench, forearms on thighs, palms up.", "Curl wrists up holding dumbbells.", "Lower slowly."],
     "image": ""},

    # --- CABLE/MACHINE ---
    {"name": "Cable Woodchop", "muscles": "Obliques, Core", "equipment": "cable",
     "instructions": ["Set cable high or low.", "Rotate torso pulling cable diagonally across body.", "Control the return."],
     "image": ""},
    {"name": "Cable Curl", "muscles": "Biceps", "equipment": "cable",
     "instructions": ["Attach straight or EZ bar to low cable.", "Curl up keeping elbows at sides.", "Lower with control."],
     "image": ""},
    {"name": "Cable Kickback", "muscles": "Glutes", "equipment": "cable",
     "instructions": ["Attach ankle cuff to low cable.", "Kick leg back squeezing glute.", "Return with control."],
     "image": ""},
    {"name": "Machine Chest Press", "muscles": "Chest, Shoulders, Triceps", "equipment": "machine",
     "instructions": ["Sit in machine, grip handles at chest level.", "Press forward until arms are extended.", "Return slowly."],
     "image": ""},
    {"name": "Machine Shoulder Press", "muscles": "Shoulders, Triceps", "equipment": "machine",
     "instructions": ["Sit in machine, grip handles at shoulder level.", "Press overhead.", "Lower with control."],
     "image": ""},
    {"name": "Pec Deck", "muscles": "Chest", "equipment": "machine",
     "instructions": ["Sit in machine, arms on pads.", "Squeeze pads together in front of chest.", "Open slowly."],
     "image": ""},
    {"name": "Reverse Pec Deck", "muscles": "Rear Delts, Upper Back", "equipment": "machine",
     "instructions": ["Face the pad on pec deck machine.", "Squeeze handles back, pinching shoulder blades.", "Return slowly."],
     "image": ""},
    {"name": "Smith Machine Squat", "muscles": "Quads, Glutes", "equipment": "machine",
     "instructions": ["Set bar on shoulders in Smith machine.", "Feet slightly forward.", "Squat down and press up."],
     "image": ""},
    {"name": "Cable Pull-Through", "muscles": "Glutes, Hamstrings", "equipment": "cable",
     "instructions": ["Face away from low cable, rope between legs.", "Hinge at hips letting cable pull you back.", "Drive hips forward to stand."],
     "image": ""},
    {"name": "Machine Row", "muscles": "Upper Back, Lats, Biceps", "equipment": "machine",
     "instructions": ["Sit at machine, chest against pad.", "Pull handles toward body squeezing back.", "Return with control."],
     "image": ""},
    {"name": "Cable Overhead Tricep Extension", "muscles": "Triceps", "equipment": "cable",
     "instructions": ["Face away from high cable with rope.", "Extend arms overhead.", "Bend elbows to stretch triceps, then extend."],
     "image": ""},
    {"name": "Machine Lateral Raise", "muscles": "Side Delts", "equipment": "machine",
     "instructions": ["Sit in lateral raise machine.", "Raise arms to sides against pads.", "Lower with control."],
     "image": ""},
    {"name": "Seated Leg Curl", "muscles": "Hamstrings", "equipment": "machine",
     "instructions": ["Sit in machine with pad behind ankles.", "Curl legs back.", "Return slowly."],
     "image": ""},
    {"name": "Standing Calf Raise Machine", "muscles": "Calves", "equipment": "machine",
     "instructions": ["Stand in calf raise machine, shoulders under pads.", "Rise onto toes.", "Lower slowly past parallel."],
     "image": ""},
    {"name": "Cable Crossover", "muscles": "Chest", "equipment": "cable",
     "instructions": ["Set cables at high position.", "Step forward, bring hands together in front.", "Squeeze chest, return slowly."],
     "image": ""},
    {"name": "Assisted Pull-Up Machine", "muscles": "Lats, Biceps, Upper Back", "equipment": "machine",
     "instructions": ["Select counterweight to assist.", "Grip handles, pull yourself up.", "Lower with control."],
     "image": ""},
    {"name": "Hip Abductor Machine", "muscles": "Glutes, Hip Abductors", "equipment": "machine",
     "instructions": ["Sit in machine with legs together.", "Press legs apart against pads.", "Return slowly."],
     "image": ""},
    {"name": "Hip Adductor Machine", "muscles": "Adductors, Inner Thighs", "equipment": "machine",
     "instructions": ["Sit in machine with legs apart.", "Squeeze legs together.", "Release slowly."],
     "image": ""},

    # --- BODYWEIGHT ---
    {"name": "Pike Pushup", "muscles": "Shoulders, Triceps", "equipment": "bodyweight",
     "instructions": ["Start in downward dog position.", "Bend elbows lowering head toward floor.", "Press back up."],
     "image": ""},
    {"name": "Diamond Pushup", "muscles": "Triceps, Chest", "equipment": "bodyweight",
     "instructions": ["Place hands together in diamond shape.", "Perform pushup keeping elbows close to body.", "Great tricep emphasis."],
     "image": ""},
    {"name": "Wide Pushup", "muscles": "Chest, Shoulders", "equipment": "bodyweight",
     "instructions": ["Hands wider than shoulder width.", "Lower chest to floor.", "Press up."],
     "image": ""},
    {"name": "Decline Pushup", "muscles": "Upper Chest, Shoulders, Triceps", "equipment": "bodyweight",
     "instructions": ["Place feet on elevated surface.", "Perform pushup.", "Targets upper chest more."],
     "image": ""},
    {"name": "Inverted Row", "muscles": "Upper Back, Biceps", "equipment": "bodyweight",
     "instructions": ["Hang under a bar or table.", "Pull chest to bar.", "Lower with control."],
     "image": ""},
    {"name": "Bodyweight Skull Crusher", "muscles": "Triceps", "equipment": "bodyweight",
     "instructions": ["Place hands on elevated surface.", "Lower forehead toward surface by bending elbows.", "Extend back up."],
     "image": ""},
    {"name": "Pistol Squat", "muscles": "Quads, Glutes, Balance", "equipment": "bodyweight",
     "instructions": ["Stand on one leg.", "Squat down on that leg, other leg extended forward.", "Drive back up."],
     "image": ""},
    {"name": "Broad Jump", "muscles": "Quads, Glutes, Calves, Power", "equipment": "bodyweight",
     "instructions": ["Stand with feet shoulder width.", "Swing arms and jump forward as far as possible.", "Land softly."],
     "image": ""},
    {"name": "Bear Crawl", "muscles": "Core, Shoulders, Full Body", "equipment": "bodyweight",
     "instructions": ["Get on all fours, knees hovering.", "Crawl forward moving opposite hand and foot.", "Keep back flat."],
     "image": ""},
    {"name": "Crab Walk", "muscles": "Triceps, Shoulders, Core", "equipment": "bodyweight",
     "instructions": ["Sit, place hands behind you.", "Lift hips off ground.", "Walk forward or backward."],
     "image": ""},
    {"name": "Tuck Jump", "muscles": "Quads, Calves, Cardio", "equipment": "bodyweight",
     "instructions": ["Jump up bringing knees to chest.", "Land softly.", "Repeat quickly."],
     "image": ""},
    {"name": "Bodyweight Squat Hold", "muscles": "Quads, Glutes, Endurance", "equipment": "bodyweight",
     "instructions": ["Squat to parallel and hold.", "Keep weight in heels, chest up.", "Hold for prescribed time."],
     "image": ""},
    {"name": "Superman", "muscles": "Lower Back, Glutes", "equipment": "bodyweight",
     "instructions": ["Lie face down, arms extended.", "Lift arms, chest, and legs off floor.", "Hold briefly, lower."],
     "image": ""},
    {"name": "Reverse Lunge", "muscles": "Quads, Glutes, Hamstrings", "equipment": "bodyweight",
     "instructions": ["Step backward into a lunge.", "Lower rear knee toward floor.", "Push through front foot to return."],
     "image": ""},
    {"name": "Side Plank", "muscles": "Obliques, Core", "equipment": "bodyweight",
     "instructions": ["Lie on side, prop up on elbow.", "Lift hips forming straight line.", "Hold for prescribed time."],
     "image": ""},
    {"name": "V-Up", "muscles": "Abs, Hip Flexors", "equipment": "bodyweight",
     "instructions": ["Lie flat, arms overhead.", "Simultaneously lift legs and torso forming a V.", "Lower slowly."],
     "image": ""},
    {"name": "Hollow Body Hold", "muscles": "Core", "equipment": "bodyweight",
     "instructions": ["Lie on back, press lower back into floor.", "Extend arms overhead and legs out, hovering.", "Hold position."],
     "image": ""},
    {"name": "L-Sit (on floor or bars)", "muscles": "Core, Hip Flexors, Triceps", "equipment": "bodyweight",
     "instructions": ["Place hands on floor or parallel bars.", "Lift body, extend legs straight in front.", "Hold."],
     "image": ""},
    {"name": "Handstand Wall Hold", "muscles": "Shoulders, Core, Balance", "equipment": "bodyweight",
     "instructions": ["Kick up to handstand against wall.", "Hold with arms locked out.", "Come down carefully."],
     "image": ""},
    {"name": "Muscle-Up", "muscles": "Lats, Chest, Triceps, Full Upper Body", "equipment": "bodyweight",
     "instructions": ["Start with explosive pull-up.", "Transition over the bar.", "Press up to full extension above bar."],
     "image": ""},
    {"name": "Jumping Lunge", "muscles": "Quads, Glutes, Cardio", "equipment": "bodyweight",
     "instructions": ["Lunge position, jump and switch legs mid-air.", "Land softly in opposite lunge.", "Repeat."],
     "image": ""},
    {"name": "High Knees", "muscles": "Core, Hip Flexors, Cardio", "equipment": "bodyweight",
     "instructions": ["Run in place bringing knees to waist height.", "Pump arms.", "Keep a fast pace."],
     "image": ""},
    {"name": "Butt Kicks", "muscles": "Hamstrings, Cardio", "equipment": "bodyweight",
     "instructions": ["Run in place kicking heels to glutes.", "Keep pace quick.", "Good warmup movement."],
     "image": ""},
    {"name": "Skater Jumps", "muscles": "Glutes, Quads, Balance, Cardio", "equipment": "bodyweight",
     "instructions": ["Jump laterally to one side landing on one foot.", "Swing opposite leg behind.", "Jump to other side."],
     "image": ""},
    {"name": "Inchworm", "muscles": "Hamstrings, Core, Shoulders", "equipment": "bodyweight",
     "instructions": ["Stand, fold forward touching floor.", "Walk hands out to plank position.", "Walk feet to hands, stand up."],
     "image": ""},
    {"name": "Leg Raise", "muscles": "Lower Abs, Hip Flexors", "equipment": "bodyweight",
     "instructions": ["Lie on back, legs straight.", "Raise legs to 90 degrees.", "Lower slowly without touching floor."],
     "image": ""},
    {"name": "Flutter Kicks", "muscles": "Lower Abs, Hip Flexors", "equipment": "bodyweight",
     "instructions": ["Lie on back, legs slightly raised.", "Alternate kicking legs up and down.", "Keep lower back pressed to floor."],
     "image": ""},

    # --- KETTLEBELL ---
    {"name": "Kettlebell Goblet Squat", "muscles": "Quads, Glutes, Core", "equipment": "kettlebell",
     "instructions": ["Hold kettlebell at chest by horns.", "Squat deep keeping chest up.", "Press through heels to stand."],
     "image": ""},
    {"name": "Kettlebell Clean", "muscles": "Full Body, Shoulders", "equipment": "kettlebell",
     "instructions": ["Swing kettlebell from between legs.", "Pull and rotate it to rack position at shoulder.", "Control the catch."],
     "image": ""},
    {"name": "Kettlebell Press", "muscles": "Shoulders, Triceps, Core", "equipment": "kettlebell",
     "instructions": ["From rack position, press kettlebell overhead.", "Lock out arm.", "Lower to rack."],
     "image": ""},
    {"name": "Kettlebell Snatch", "muscles": "Full Body, Shoulders, Cardio", "equipment": "kettlebell",
     "instructions": ["Swing kettlebell from between legs.", "In one motion, punch it overhead.", "Control the descent."],
     "image": ""},
    {"name": "Kettlebell Turkish Get-Up", "muscles": "Full Body, Core, Shoulders", "equipment": "kettlebell",
     "instructions": ["Lie on back holding KB overhead with one arm.", "Stand up through a series of movements keeping KB overhead.", "Reverse to lie back down."],
     "image": ""},
    {"name": "Kettlebell Row", "muscles": "Lats, Upper Back, Biceps", "equipment": "kettlebell",
     "instructions": ["Hinge at hips, one hand on bench.", "Row KB to hip.", "Lower with control."],
     "image": ""},
    {"name": "Kettlebell Deadlift", "muscles": "Glutes, Hamstrings, Lower Back", "equipment": "kettlebell",
     "instructions": ["Stand over kettlebell.", "Hinge at hips, grip handle.", "Stand up driving hips forward."],
     "image": ""},
    {"name": "Kettlebell Windmill", "muscles": "Obliques, Shoulders, Hips", "equipment": "kettlebell",
     "instructions": ["Hold KB overhead, feet wider than hips.", "Hinge laterally reaching opposite hand to floor.", "Return to standing."],
     "image": ""},
    {"name": "Kettlebell Halo", "muscles": "Shoulders, Core", "equipment": "kettlebell",
     "instructions": ["Hold KB upside down at chest.", "Circle it around your head.", "Alternate directions."],
     "image": ""},
    {"name": "Kettlebell Farmer Carry", "muscles": "Grip, Core, Traps, Full Body", "equipment": "kettlebell",
     "instructions": ["Hold heavy KB in each hand.", "Walk with tall posture.", "Maintain tight core throughout."],
     "image": ""},
    {"name": "Kettlebell Thruster", "muscles": "Full Body", "equipment": "kettlebell",
     "instructions": ["Hold KBs at shoulders.", "Squat down, then drive up pressing overhead.", "One fluid motion."],
     "image": ""},

    # --- RESISTANCE BAND ---
    {"name": "Band Pull-Apart", "muscles": "Rear Delts, Upper Back", "equipment": "band",
     "instructions": ["Hold band in front at shoulder height.", "Pull hands apart stretching band.", "Squeeze shoulder blades."],
     "image": ""},
    {"name": "Band Face Pull", "muscles": "Rear Delts, Rotator Cuff", "equipment": "band",
     "instructions": ["Anchor band at face height.", "Pull toward face, spreading hands apart.", "Squeeze shoulder blades."],
     "image": ""},
    {"name": "Band Squat", "muscles": "Quads, Glutes", "equipment": "band",
     "instructions": ["Stand on band, hold at shoulders.", "Squat down.", "Stand up against band resistance."],
     "image": ""},
    {"name": "Band Chest Press", "muscles": "Chest, Triceps", "equipment": "band",
     "instructions": ["Anchor band behind you at chest height.", "Press forward.", "Return with control."],
     "image": ""},
    {"name": "Band Row", "muscles": "Upper Back, Lats, Biceps", "equipment": "band",
     "instructions": ["Anchor band in front at waist height.", "Pull toward body squeezing back.", "Return slowly."],
     "image": ""},
    {"name": "Band Overhead Press", "muscles": "Shoulders, Triceps", "equipment": "band",
     "instructions": ["Stand on band, hold at shoulders.", "Press overhead.", "Lower with control."],
     "image": ""},
    {"name": "Band Bicep Curl", "muscles": "Biceps", "equipment": "band",
     "instructions": ["Stand on band, hold ends.", "Curl hands toward shoulders.", "Lower slowly."],
     "image": ""},
    {"name": "Band Tricep Pushdown", "muscles": "Triceps", "equipment": "band",
     "instructions": ["Anchor band overhead.", "Push down extending arms.", "Return slowly."],
     "image": ""},
    {"name": "Band Lateral Walk", "muscles": "Glutes, Hip Abductors", "equipment": "band",
     "instructions": ["Place band around ankles or above knees.", "Step laterally maintaining tension.", "Keep slight squat position."],
     "image": ""},
    {"name": "Band Good Morning", "muscles": "Hamstrings, Glutes, Lower Back", "equipment": "band",
     "instructions": ["Stand on band, loop over neck/shoulders.", "Hinge at hips.", "Drive hips forward to stand."],
     "image": ""},
    {"name": "Band Deadlift", "muscles": "Glutes, Hamstrings, Back", "equipment": "band",
     "instructions": ["Stand on center of band.", "Hold ends, hinge at hips.", "Stand up pulling against resistance."],
     "image": ""},
    {"name": "Band Glute Bridge", "muscles": "Glutes, Hamstrings", "equipment": "band",
     "instructions": ["Place band above knees, lie on back.", "Drive hips up pressing knees out.", "Squeeze at top."],
     "image": ""},
    {"name": "Band Pallof Press", "muscles": "Core, Obliques", "equipment": "band",
     "instructions": ["Anchor band at side, hold at chest.", "Press hands straight out resisting rotation.", "Return to chest."],
     "image": ""},

    # --- MOBILITY / STRETCHING ---
    {"name": "World's Greatest Stretch", "muscles": "Hips, Thoracic Spine, Hamstrings", "equipment": "bodyweight",
     "instructions": ["Lunge forward, place opposite hand on floor.", "Rotate torso opening toward front leg side.", "Hold and switch sides."],
     "image": ""},
    {"name": "Cat-Cow Stretch", "muscles": "Spine, Core", "equipment": "bodyweight",
     "instructions": ["On all fours, alternate between arching and rounding back.", "Breathe deeply with each position."],
     "image": ""},
    {"name": "90/90 Hip Stretch", "muscles": "Hips, Glutes", "equipment": "bodyweight",
     "instructions": ["Sit with front leg at 90° and back leg at 90°.", "Lean forward over front shin.", "Switch sides."],
     "image": ""},
    {"name": "Foam Roll (Upper Back)", "muscles": "Thoracic Spine, Upper Back", "equipment": "bodyweight",
     "instructions": ["Lie on foam roller placed under upper back.", "Roll slowly from mid-back to shoulder blades.", "Pause on tight spots."],
     "image": ""},
    {"name": "Couch Stretch", "muscles": "Hip Flexors, Quads", "equipment": "bodyweight",
     "instructions": ["Place rear foot on wall or couch behind you.", "Front foot forward in lunge.", "Drive hips forward stretching hip flexor."],
     "image": ""},
]

###############################################################################
# 2. WORKOUT TEMPLATE GENERATOR
###############################################################################

# Equipment categories for exercises (mapping exercise name -> required equipment)
EQUIP_MAP = {}
# We'll populate from both existing and new exercises

FULL_GYM_EXERCISES = {
    "push": ["Bench Press", "Incline Bench Press", "Dumbbell Incline Press", "Dumbbell Press", "Overhead Press", "Dumbbell Shoulder Press", "Dumbbell Arnold Press", "Close-Grip Bench Press", "Cable Fly", "Pec Deck", "Machine Chest Press", "Machine Shoulder Press", "Cable Crossover", "Landmine Press", "Push Press", "Z Press", "Floor Press", "Dumbbell Fly", "Dumbbell Front Raise", "Lateral Raises", "Cable Lateral Raise", "Machine Lateral Raise", "Dips", "Weighted Dips", "Tricep Pushdowns", "Skull Crushers", "Dumbbell Tricep Extension", "Dumbbell Skullcrusher", "Cable Overhead Tricep Extension"],
    "pull": ["Barbell Row", "Pendlay Row", "Dumbbell Row", "Single-Arm Dumbbell Row", "Lat Pulldown", "Seated Cable Row", "Machine Row", "Pull-Ups", "Chin-Ups", "Face Pulls", "Cable Curl", "Barbell Curl", "Dumbbell Curl", "Hammer Curl", "Incline Dumbbell Curl", "Concentration Curl", "Rear Delt Fly", "Dumbbell Reverse Fly", "Reverse Pec Deck", "Landmine Row", "Barbell Shrug", "Dumbbell Shrug", "Snatch-Grip Deadlift", "Assisted Pull-Up Machine"],
    "legs": ["Barbell Squat", "Front Squat", "Hack Squat", "Leg Press", "Leg Extension", "Leg Curls", "Seated Leg Curl", "Deadlift", "Romanian Deadlift", "Sumo Deadlift", "Dumbbell Lunges", "Bulgarian Split Squat", "Hip Thrust", "Barbell Hip Thrust", "Dumbbell RDL", "Goblet Squat", "Barbell Lunge", "Barbell Reverse Lunge", "Dumbbell Step-Up", "Cable Pull-Through", "Cable Kickback", "Smith Machine Squat", "Calf Raises", "Standing Calf Raise Machine", "Hip Abductor Machine", "Hip Adductor Machine", "Pause Squat", "Deficit Deadlift", "Zercher Squat", "Barbell Good Morning", "Glute Bridges"],
    "core": ["Plank", "Side Plank", "Russian Twist", "Hanging Leg Raise", "Bicycle Crunches", "Dead Bug", "Cable Woodchop", "V-Up", "Hollow Body Hold", "Leg Raise", "Flutter Kicks", "Band Pallof Press"]
}

HOME_DB_EXERCISES = {
    "push": ["Dumbbell Press", "Dumbbell Bench Press", "Dumbbell Incline Press", "Dumbbell Shoulder Press", "Dumbbell Arnold Press", "Dumbbell Fly", "Dumbbell Front Raise", "Lateral Raises", "Dumbbell Tricep Extension", "Dumbbell Skullcrusher", "Dumbbell Chest Press (Floor)", "Dumbbell Thruster"],
    "pull": ["Dumbbell Row", "Single-Arm Dumbbell Row", "Dumbbell Curl", "Hammer Curl", "Incline Dumbbell Curl", "Concentration Curl", "Dumbbell Reverse Fly", "Dumbbell Shrug", "Renegade Row", "Dumbbell Pullover"],
    "legs": ["Goblet Squat", "Dumbbell Lunges", "Bulgarian Split Squat", "Dumbbell RDL", "Dumbbell Step-Up", "Dumbbell Sumo Squat", "Dumbbell Lateral Lunge", "Glute Bridges", "Dumbbell Calf Raise"],
    "core": ["Plank", "Side Plank", "Russian Twist", "Dead Bug", "Bicycle Crunches", "V-Up", "Hollow Body Hold", "Leg Raise", "Flutter Kicks"]
}

KB_EXERCISES = {
    "push": ["Kettlebell Press", "Kettlebell Thruster", "Pushups", "Diamond Pushup", "Pike Pushup"],
    "pull": ["Kettlebell Row", "Kettlebell Clean", "Kettlebell Halo", "Inverted Row"],
    "legs": ["Kettlebell Goblet Squat", "Kettlebell Swing", "Kettlebell Deadlift", "Kettlebell Snatch", "Reverse Lunge", "Bulgarian Split Squat"],
    "full": ["Kettlebell Turkish Get-Up", "Kettlebell Windmill", "Kettlebell Farmer Carry"],
    "core": ["Plank", "Side Plank", "Russian Twist", "Dead Bug", "Hollow Body Hold"]
}

BAND_EXERCISES = {
    "push": ["Band Chest Press", "Band Overhead Press", "Band Tricep Pushdown", "Pushups", "Diamond Pushup", "Pike Pushup"],
    "pull": ["Band Row", "Band Face Pull", "Band Pull-Apart", "Band Bicep Curl", "Inverted Row"],
    "legs": ["Band Squat", "Band Deadlift", "Band Good Morning", "Band Glute Bridge", "Band Lateral Walk", "Air Squats", "Reverse Lunge", "Bulgarian Split Squat"],
    "core": ["Band Pallof Press", "Plank", "Side Plank", "Dead Bug", "Hollow Body Hold"]
}

BW_EXERCISES = {
    "push": ["Pushups", "Diamond Pushup", "Wide Pushup", "Decline Pushup", "Pike Pushup", "Dips", "Bodyweight Skull Crusher", "Handstand Wall Hold"],
    "pull": ["Pull-Ups", "Chin-Ups", "Inverted Row", "Muscle-Up"],
    "legs": ["Air Squats", "Pistol Squat", "Bulgarian Split Squat", "Reverse Lunge", "Jumping Lunge", "Step-ups", "Broad Jump", "Box Jumps", "Glute Bridges", "Bodyweight Squat Hold", "Calf Raises"],
    "cardio": ["Burpees", "Mountain Climbers", "High Knees", "Butt Kicks", "Jumping Jacks", "Tuck Jump", "Skater Jumps"],
    "core": ["Plank", "Side Plank", "V-Up", "Hollow Body Hold", "L-Sit (on floor or bars)", "Leg Raise", "Flutter Kicks", "Superman", "Dead Bug", "Bicycle Crunches", "Bear Crawl"],
    "mobility": ["World's Greatest Stretch", "Cat-Cow Stretch", "90/90 Hip Stretch", "Couch Stretch", "Inchworm"]
}


def make_ex(name, sets, reps, rest="90s"):
    return {"exercise": name, "sets": sets, "reps": reps, "rest": rest}


def gen_id(name):
    return name.lower().replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "").replace("-", "_").replace("'", "").replace(",", "")[:60]


templates = []


# ============================================================================
# FULL GYM TEMPLATES
# ============================================================================

# --- PPL variations ---
def ppl_template(name, sex, level, variant, schedule="6 days/week", reasoning=""):
    push_a = FULL_GYM_EXERCISES["push"]
    pull_a = FULL_GYM_EXERCISES["pull"]
    legs_a = FULL_GYM_EXERCISES["legs"]
    core = FULL_GYM_EXERCISES["core"]
    
    if variant == "hypertrophy":
        days = [
            {"day_label": "Day 1: Push A (Chest Focus)", "exercises": [
                make_ex("Bench Press", 4, "8-10"), make_ex("Incline Bench Press", 3, "10-12"),
                make_ex("Cable Fly", 3, "12-15", "60s"), make_ex("Overhead Press", 3, "8-10"),
                make_ex("Lateral Raises", 3, "15-20", "60s"), make_ex("Tricep Pushdowns", 3, "12-15", "60s"),
                make_ex("Skull Crushers", 3, "10-12", "60s")]},
            {"day_label": "Day 2: Pull A (Back Width)", "exercises": [
                make_ex("Pull-Ups", 4, "6-10"), make_ex("Barbell Row", 4, "8-10"),
                make_ex("Lat Pulldown", 3, "10-12"), make_ex("Face Pulls", 3, "15-20", "60s"),
                make_ex("Barbell Curl", 3, "10-12", "60s"), make_ex("Hammer Curl", 3, "12-15", "60s")]},
            {"day_label": "Day 3: Legs A (Quad Focus)", "exercises": [
                make_ex("Barbell Squat", 4, "6-8", "150s"), make_ex("Leg Press", 3, "10-12"),
                make_ex("Leg Extension", 3, "12-15", "60s"), make_ex("Romanian Deadlift", 3, "10-12"),
                make_ex("Leg Curls", 3, "12-15", "60s"), make_ex("Calf Raises", 4, "15-20", "60s")]},
            {"day_label": "Day 4: Push B (Shoulder Focus)", "exercises": [
                make_ex("Overhead Press", 4, "6-8"), make_ex("Dumbbell Incline Press", 3, "10-12"),
                make_ex("Cable Lateral Raise", 4, "15-20", "60s"), make_ex("Pec Deck", 3, "12-15", "60s"),
                make_ex("Dumbbell Tricep Extension", 3, "12-15", "60s"), make_ex("Dips", 3, "8-12")]},
            {"day_label": "Day 5: Pull B (Back Thickness)", "exercises": [
                make_ex("Pendlay Row", 4, "6-8"), make_ex("Chin-Ups", 3, "8-12"),
                make_ex("Seated Cable Row", 3, "10-12"), make_ex("Reverse Pec Deck", 3, "15-20", "60s"),
                make_ex("Incline Dumbbell Curl", 3, "12-15", "60s"), make_ex("Dumbbell Shrug", 3, "12-15", "60s")]},
            {"day_label": "Day 6: Legs B (Glute/Ham Focus)", "exercises": [
                make_ex("Deadlift", 4, "5-6", "180s"), make_ex("Bulgarian Split Squat", 3, "10-12/leg"),
                make_ex("Hip Thrust", 3, "10-12"), make_ex("Seated Leg Curl", 3, "12-15", "60s"),
                make_ex("Hip Abductor Machine", 3, "15-20", "60s"), make_ex("Standing Calf Raise Machine", 4, "12-15", "60s")]}
        ]
    elif variant == "strength":
        days = [
            {"day_label": "Day 1: Push A (Heavy)", "exercises": [
                make_ex("Bench Press", 5, "5", "180s"), make_ex("Overhead Press", 4, "6"),
                make_ex("Dips", 3, "8-10"), make_ex("Lateral Raises", 3, "12-15", "60s"),
                make_ex("Tricep Pushdowns", 3, "10-12", "60s")]},
            {"day_label": "Day 2: Pull A (Heavy)", "exercises": [
                make_ex("Barbell Row", 5, "5", "180s"), make_ex("Pull-Ups", 4, "6-8"),
                make_ex("Face Pulls", 3, "15-20", "60s"), make_ex("Barbell Curl", 3, "8-10"),
                make_ex("Barbell Shrug", 3, "8-10")]},
            {"day_label": "Day 3: Legs A (Heavy Squat)", "exercises": [
                make_ex("Barbell Squat", 5, "5", "240s"), make_ex("Front Squat", 3, "6-8", "150s"),
                make_ex("Leg Curls", 3, "10-12"), make_ex("Calf Raises", 4, "12-15", "60s"),
                make_ex("Plank", 3, "45s", "60s")]},
            {"day_label": "Day 4: Push B (Volume)", "exercises": [
                make_ex("Incline Bench Press", 4, "8-10"), make_ex("Machine Shoulder Press", 3, "10-12"),
                make_ex("Cable Fly", 3, "12-15", "60s"), make_ex("Cable Lateral Raise", 3, "15-20", "60s"),
                make_ex("Cable Overhead Tricep Extension", 3, "12-15", "60s")]},
            {"day_label": "Day 5: Pull B (Volume)", "exercises": [
                make_ex("Lat Pulldown", 4, "8-10"), make_ex("Seated Cable Row", 4, "10-12"),
                make_ex("Dumbbell Reverse Fly", 3, "15-20", "60s"), make_ex("Hammer Curl", 3, "10-12"),
                make_ex("Dumbbell Shrug", 3, "12-15", "60s")]},
            {"day_label": "Day 6: Legs B (Heavy Dead)", "exercises": [
                make_ex("Deadlift", 5, "5", "240s"), make_ex("Hack Squat", 3, "8-10"),
                make_ex("Romanian Deadlift", 3, "8-10"), make_ex("Leg Extension", 3, "12-15", "60s"),
                make_ex("Standing Calf Raise Machine", 4, "12-15", "60s")]}
        ]
    elif variant == "female_hyp":
        days = [
            {"day_label": "Day 1: Push (Shoulders Emphasis)", "exercises": [
                make_ex("Dumbbell Shoulder Press", 4, "8-10"), make_ex("Dumbbell Incline Press", 3, "10-12"),
                make_ex("Lateral Raises", 4, "15-20", "60s"), make_ex("Cable Fly", 3, "12-15", "60s"),
                make_ex("Tricep Pushdowns", 3, "12-15", "60s")]},
            {"day_label": "Day 2: Pull", "exercises": [
                make_ex("Lat Pulldown", 4, "8-10"), make_ex("Seated Cable Row", 3, "10-12"),
                make_ex("Face Pulls", 3, "15-20", "60s"), make_ex("Dumbbell Curl", 3, "12-15", "60s"),
                make_ex("Rear Delt Fly", 3, "15-20", "60s")]},
            {"day_label": "Day 3: Legs (Glute Focus)", "exercises": [
                make_ex("Hip Thrust", 4, "8-12"), make_ex("Bulgarian Split Squat", 3, "10-12/leg"),
                make_ex("Romanian Deadlift", 3, "10-12"), make_ex("Cable Kickback", 3, "12-15/leg", "60s"),
                make_ex("Hip Abductor Machine", 3, "15-20", "60s"), make_ex("Calf Raises", 3, "15-20", "60s")]},
            {"day_label": "Day 4: Push B", "exercises": [
                make_ex("Bench Press", 3, "8-10"), make_ex("Overhead Press", 3, "8-10"),
                make_ex("Cable Lateral Raise", 3, "15-20", "60s"), make_ex("Pec Deck", 3, "12-15", "60s"),
                make_ex("Dumbbell Tricep Extension", 3, "12-15", "60s")]},
            {"day_label": "Day 5: Pull B", "exercises": [
                make_ex("Pull-Ups", 3, "AMRAP"), make_ex("Dumbbell Row", 3, "10-12"),
                make_ex("Reverse Pec Deck", 3, "15-20", "60s"), make_ex("Hammer Curl", 3, "12-15", "60s"),
                make_ex("Dumbbell Shrug", 3, "12-15", "60s")]},
            {"day_label": "Day 6: Legs B (Quad Focus)", "exercises": [
                make_ex("Barbell Squat", 4, "8-10"), make_ex("Leg Press", 3, "10-12"),
                make_ex("Leg Extension", 3, "12-15", "60s"), make_ex("Seated Leg Curl", 3, "12-15", "60s"),
                make_ex("Hip Adductor Machine", 3, "15-20", "60s"), make_ex("Standing Calf Raise Machine", 3, "15-20", "60s")]}
        ]
    else:
        return None
    
    return {
        "id": gen_id(name),
        "target": {"sex": sex, "goal": "Build Muscle", "level": level},
        "equipment": "Full Gym",
        "name": name,
        "schedule": schedule,
        "reasoning": reasoning,
        "days": days
    }

# PPL variations
templates.append(ppl_template("Hypertrophy PPL (6-Day)", "male", "Intermediate", "hypertrophy",
    reasoning="Classic Push/Pull/Legs split run twice per week for maximum hypertrophy stimulus. Each session alternates between heavy compounds and isolation work."))
templates.append(ppl_template("Strength PPL (6-Day)", "male", "Advanced", "strength",
    reasoning="PPL split with strength-focused rep ranges on primary movements. Heavy compounds followed by volume work for balanced development."))
templates.append(ppl_template("Women's Hypertrophy PPL (6-Day)", "female", "Intermediate", "female_hyp",
    reasoning="PPL split designed for women with emphasis on glutes, shoulders, and back development. Higher rep ranges on isolation work."))

# --- 5-Day Bro Split ---
templates.append({
    "id": "classic_bro_split_5day", "target": {"sex": "male", "goal": "Build Muscle", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Classic Bro Split (5-Day)", "schedule": "5 days/week",
    "reasoning": "The classic bodybuilding split: one major muscle group per day. Maximum volume per body part with full week of recovery. Great for intermediate lifters wanting focused sessions.",
    "days": [
        {"day_label": "Day 1: Chest", "exercises": [
            make_ex("Bench Press", 4, "8-10"), make_ex("Incline Bench Press", 4, "8-10"),
            make_ex("Dumbbell Fly", 3, "12-15", "60s"), make_ex("Cable Crossover", 3, "12-15", "60s"),
            make_ex("Pec Deck", 3, "15-20", "60s")]},
        {"day_label": "Day 2: Back", "exercises": [
            make_ex("Deadlift", 4, "5-6", "180s"), make_ex("Barbell Row", 4, "8-10"),
            make_ex("Lat Pulldown", 3, "10-12"), make_ex("Seated Cable Row", 3, "10-12"),
            make_ex("Dumbbell Pullover", 3, "12-15", "60s")]},
        {"day_label": "Day 3: Shoulders", "exercises": [
            make_ex("Overhead Press", 4, "6-8"), make_ex("Dumbbell Arnold Press", 3, "10-12"),
            make_ex("Lateral Raises", 4, "15-20", "60s"), make_ex("Face Pulls", 3, "15-20", "60s"),
            make_ex("Dumbbell Front Raise", 3, "12-15", "60s"), make_ex("Barbell Shrug", 4, "10-12")]},
        {"day_label": "Day 4: Legs", "exercises": [
            make_ex("Barbell Squat", 4, "6-8", "180s"), make_ex("Leg Press", 4, "10-12"),
            make_ex("Romanian Deadlift", 3, "10-12"), make_ex("Leg Extension", 3, "12-15", "60s"),
            make_ex("Leg Curls", 3, "12-15", "60s"), make_ex("Standing Calf Raise Machine", 4, "15-20", "60s")]},
        {"day_label": "Day 5: Arms", "exercises": [
            make_ex("Close-Grip Bench Press", 4, "8-10"), make_ex("Barbell Curl", 4, "8-10"),
            make_ex("Skull Crushers", 3, "10-12"), make_ex("Hammer Curl", 3, "10-12"),
            make_ex("Tricep Pushdowns", 3, "12-15", "60s"), make_ex("Concentration Curl", 3, "12-15", "60s"),
            make_ex("Cable Overhead Tricep Extension", 3, "12-15", "60s")]}
    ]
})

# --- Arnold Split ---
templates.append({
    "id": "arnold_split_6day", "target": {"sex": "male", "goal": "Build Muscle", "level": "Advanced"},
    "equipment": "Full Gym", "name": "Arnold Split (6-Day)", "schedule": "6 days/week",
    "reasoning": "Arnold Schwarzenegger's legendary split: Chest/Back, Shoulders/Arms, Legs, repeat. Antagonist supersets on Day 1 maximize pump and efficiency.",
    "days": [
        {"day_label": "Day 1: Chest & Back", "exercises": [
            make_ex("Bench Press", 5, "6-10"), make_ex("Pull-Ups", 5, "8-12"),
            make_ex("Incline Bench Press", 4, "8-10"), make_ex("Barbell Row", 4, "8-10"),
            make_ex("Dumbbell Fly", 3, "12-15", "60s"), make_ex("Lat Pulldown", 3, "10-12")]},
        {"day_label": "Day 2: Shoulders & Arms", "exercises": [
            make_ex("Overhead Press", 4, "6-8"), make_ex("Dumbbell Arnold Press", 3, "10-12"),
            make_ex("Lateral Raises", 4, "15-20", "60s"), make_ex("Barbell Curl", 4, "8-10"),
            make_ex("Skull Crushers", 4, "8-10"), make_ex("Hammer Curl", 3, "10-12"),
            make_ex("Tricep Pushdowns", 3, "12-15", "60s")]},
        {"day_label": "Day 3: Legs", "exercises": [
            make_ex("Barbell Squat", 5, "6-10", "180s"), make_ex("Leg Press", 4, "10-12"),
            make_ex("Romanian Deadlift", 4, "8-10"), make_ex("Leg Extension", 3, "12-15", "60s"),
            make_ex("Leg Curls", 3, "12-15", "60s"), make_ex("Standing Calf Raise Machine", 5, "15-20", "60s")]},
        {"day_label": "Day 4: Chest & Back", "exercises": [
            make_ex("Dumbbell Incline Press", 4, "8-10"), make_ex("Chin-Ups", 4, "8-12"),
            make_ex("Cable Fly", 3, "12-15", "60s"), make_ex("Seated Cable Row", 4, "10-12"),
            make_ex("Dumbbell Press", 3, "10-12"), make_ex("Dumbbell Pullover", 3, "12-15", "60s")]},
        {"day_label": "Day 5: Shoulders & Arms", "exercises": [
            make_ex("Push Press", 4, "6-8"), make_ex("Cable Lateral Raise", 4, "15-20", "60s"),
            make_ex("Face Pulls", 3, "15-20", "60s"), make_ex("Incline Dumbbell Curl", 3, "10-12"),
            make_ex("Dumbbell Tricep Extension", 3, "10-12"), make_ex("Cable Curl", 3, "12-15", "60s"),
            make_ex("Dumbbell Skullcrusher", 3, "10-12")]},
        {"day_label": "Day 6: Legs", "exercises": [
            make_ex("Front Squat", 4, "6-8", "150s"), make_ex("Bulgarian Split Squat", 3, "10-12/leg"),
            make_ex("Hip Thrust", 4, "10-12"), make_ex("Hack Squat", 3, "10-12"),
            make_ex("Seated Leg Curl", 3, "12-15", "60s"), make_ex("Calf Raises", 4, "15-20", "60s")]}
    ]
})

# --- Upper/Lower variations ---
for sex, suffix, level in [("male", "", "Intermediate"), ("female", " (Women's)", "Intermediate"), ("male", " (Strength)", "Intermediate"), ("any", " (Beginner)", "Beginner")]:
    goal = "Strength / Powerlifting" if "Strength" in suffix else "Build Muscle"
    if "Beginner" in suffix:
        days = [
            {"day_label": "Day 1: Upper A", "exercises": [
                make_ex("Bench Press", 3, "8-10"), make_ex("Barbell Row", 3, "8-10"),
                make_ex("Overhead Press", 3, "10-12"), make_ex("Lat Pulldown", 3, "10-12"),
                make_ex("Dumbbell Curl", 2, "12-15", "60s"), make_ex("Tricep Pushdowns", 2, "12-15", "60s")]},
            {"day_label": "Day 2: Lower A", "exercises": [
                make_ex("Barbell Squat", 3, "8-10"), make_ex("Romanian Deadlift", 3, "10-12"),
                make_ex("Leg Press", 3, "10-12"), make_ex("Leg Curls", 3, "12-15", "60s"),
                make_ex("Calf Raises", 3, "15-20", "60s"), make_ex("Plank", 3, "30s", "60s")]},
            {"day_label": "Day 3: Upper B", "exercises": [
                make_ex("Dumbbell Incline Press", 3, "10-12"), make_ex("Seated Cable Row", 3, "10-12"),
                make_ex("Dumbbell Shoulder Press", 3, "10-12"), make_ex("Face Pulls", 3, "15-20", "60s"),
                make_ex("Hammer Curl", 2, "12-15", "60s"), make_ex("Dumbbell Tricep Extension", 2, "12-15", "60s")]},
            {"day_label": "Day 4: Lower B", "exercises": [
                make_ex("Deadlift", 3, "6-8", "150s"), make_ex("Bulgarian Split Squat", 3, "10-12/leg"),
                make_ex("Leg Extension", 3, "12-15", "60s"), make_ex("Glute Bridges", 3, "12-15"),
                make_ex("Standing Calf Raise Machine", 3, "15-20", "60s"), make_ex("Dead Bug", 3, "10/side", "60s")]}
        ]
    elif "Women" in suffix:
        days = [
            {"day_label": "Day 1: Upper A", "exercises": [
                make_ex("Dumbbell Shoulder Press", 4, "8-10"), make_ex("Lat Pulldown", 4, "8-10"),
                make_ex("Dumbbell Incline Press", 3, "10-12"), make_ex("Seated Cable Row", 3, "10-12"),
                make_ex("Lateral Raises", 3, "15-20", "60s"), make_ex("Face Pulls", 3, "15-20", "60s")]},
            {"day_label": "Day 2: Lower A (Glute Focus)", "exercises": [
                make_ex("Hip Thrust", 4, "8-12"), make_ex("Romanian Deadlift", 4, "10-12"),
                make_ex("Bulgarian Split Squat", 3, "10-12/leg"), make_ex("Cable Kickback", 3, "12-15/leg", "60s"),
                make_ex("Hip Abductor Machine", 3, "15-20", "60s"), make_ex("Calf Raises", 3, "15-20", "60s")]},
            {"day_label": "Day 3: Upper B", "exercises": [
                make_ex("Bench Press", 3, "8-10"), make_ex("Pull-Ups", 3, "AMRAP"),
                make_ex("Cable Fly", 3, "12-15", "60s"), make_ex("Dumbbell Row", 3, "10-12"),
                make_ex("Rear Delt Fly", 3, "15-20", "60s"), make_ex("Dumbbell Curl", 3, "12-15", "60s")]},
            {"day_label": "Day 4: Lower B (Quad Focus)", "exercises": [
                make_ex("Barbell Squat", 4, "8-10"), make_ex("Leg Press", 3, "10-12"),
                make_ex("Leg Extension", 3, "12-15", "60s"), make_ex("Seated Leg Curl", 3, "12-15", "60s"),
                make_ex("Hip Adductor Machine", 3, "15-20", "60s"), make_ex("Standing Calf Raise Machine", 3, "15-20", "60s")]}
        ]
    elif "Strength" in suffix:
        days = [
            {"day_label": "Day 1: Upper A (Heavy Press)", "exercises": [
                make_ex("Bench Press", 5, "5", "180s"), make_ex("Barbell Row", 4, "5", "150s"),
                make_ex("Overhead Press", 3, "6-8"), make_ex("Chin-Ups", 3, "6-8"),
                make_ex("Face Pulls", 3, "15-20", "60s")]},
            {"day_label": "Day 2: Lower A (Heavy Squat)", "exercises": [
                make_ex("Barbell Squat", 5, "5", "240s"), make_ex("Romanian Deadlift", 3, "8-10"),
                make_ex("Leg Press", 3, "8-10"), make_ex("Leg Curls", 3, "10-12"),
                make_ex("Plank", 3, "45s", "60s")]},
            {"day_label": "Day 3: Upper B (Volume)", "exercises": [
                make_ex("Incline Bench Press", 4, "8-10"), make_ex("Pendlay Row", 4, "6-8"),
                make_ex("Dumbbell Shoulder Press", 3, "10-12"), make_ex("Lat Pulldown", 3, "10-12"),
                make_ex("Barbell Curl", 3, "10-12"), make_ex("Skull Crushers", 3, "10-12")]},
            {"day_label": "Day 4: Lower B (Heavy Dead)", "exercises": [
                make_ex("Deadlift", 5, "5", "240s"), make_ex("Front Squat", 3, "6-8", "150s"),
                make_ex("Bulgarian Split Squat", 3, "8-10/leg"), make_ex("Leg Extension", 3, "12-15", "60s"),
                make_ex("Standing Calf Raise Machine", 4, "12-15", "60s")]}
        ]
    else:  # male hypertrophy
        days = [
            {"day_label": "Day 1: Upper A (Strength)", "exercises": [
                make_ex("Bench Press", 4, "6-8"), make_ex("Barbell Row", 4, "6-8"),
                make_ex("Overhead Press", 3, "8-10"), make_ex("Chin-Ups", 3, "8-10"),
                make_ex("Lateral Raises", 3, "15-20", "60s"), make_ex("Barbell Curl", 3, "10-12")]},
            {"day_label": "Day 2: Lower A (Strength)", "exercises": [
                make_ex("Barbell Squat", 4, "6-8", "150s"), make_ex("Romanian Deadlift", 3, "8-10"),
                make_ex("Leg Press", 3, "10-12"), make_ex("Leg Curls", 3, "10-12"),
                make_ex("Calf Raises", 4, "15-20", "60s"), make_ex("Hanging Leg Raise", 3, "10-15")]},
            {"day_label": "Day 3: Upper B (Volume)", "exercises": [
                make_ex("Dumbbell Incline Press", 4, "10-12"), make_ex("Seated Cable Row", 4, "10-12"),
                make_ex("Cable Fly", 3, "12-15", "60s"), make_ex("Lat Pulldown", 3, "10-12"),
                make_ex("Dumbbell Shoulder Press", 3, "10-12"), make_ex("Face Pulls", 3, "15-20", "60s"),
                make_ex("Hammer Curl", 3, "12-15", "60s"), make_ex("Tricep Pushdowns", 3, "12-15", "60s")]},
            {"day_label": "Day 4: Lower B (Volume)", "exercises": [
                make_ex("Deadlift", 3, "5-6", "180s"), make_ex("Bulgarian Split Squat", 3, "10-12/leg"),
                make_ex("Hack Squat", 3, "10-12"), make_ex("Seated Leg Curl", 3, "12-15", "60s"),
                make_ex("Hip Thrust", 3, "10-12"), make_ex("Standing Calf Raise Machine", 4, "15-20", "60s"),
                make_ex("Cable Woodchop", 3, "12/side", "60s")]}
        ]
    
    tname = f"Upper/Lower{suffix} (4-Day)"
    templates.append({
        "id": gen_id(tname), "target": {"sex": sex, "goal": goal, "level": level},
        "equipment": "Full Gym", "name": tname, "schedule": "4 days/week",
        "reasoning": f"Upper/Lower split hitting each muscle group twice per week. Balanced volume and recovery for {level.lower()} lifters.",
        "days": days
    })

# --- Full Body variations ---
for sex, level, days_per_week in [("any", "Beginner", 3), ("male", "Intermediate", 3), ("female", "Beginner", 3), ("any", "Intermediate", 4)]:
    if days_per_week == 3 and level == "Beginner" and sex == "any":
        days = [
            {"day_label": "Day 1: Full Body A", "exercises": [
                make_ex("Barbell Squat", 3, "8-10"), make_ex("Bench Press", 3, "8-10"),
                make_ex("Barbell Row", 3, "10-12"), make_ex("Overhead Press", 2, "10-12"),
                make_ex("Plank", 3, "30s", "60s")]},
            {"day_label": "Day 2: Full Body B", "exercises": [
                make_ex("Deadlift", 3, "6-8", "150s"), make_ex("Dumbbell Incline Press", 3, "10-12"),
                make_ex("Lat Pulldown", 3, "10-12"), make_ex("Dumbbell Lunges", 2, "10/leg"),
                make_ex("Dumbbell Curl", 2, "12-15", "60s")]},
            {"day_label": "Day 3: Full Body C", "exercises": [
                make_ex("Leg Press", 3, "10-12"), make_ex("Dumbbell Shoulder Press", 3, "10-12"),
                make_ex("Seated Cable Row", 3, "10-12"), make_ex("Dumbbell Fly", 2, "12-15", "60s"),
                make_ex("Dead Bug", 3, "10/side", "60s")]}
        ]
        tname = "Full Body Beginner (3-Day)"
    elif days_per_week == 3 and level == "Intermediate":
        days = [
            {"day_label": "Day 1: Full Body A (Heavy)", "exercises": [
                make_ex("Barbell Squat", 4, "5-6", "180s"), make_ex("Bench Press", 4, "5-6", "150s"),
                make_ex("Barbell Row", 4, "6-8"), make_ex("Face Pulls", 3, "15-20", "60s"),
                make_ex("Plank", 3, "45s", "60s")]},
            {"day_label": "Day 2: Full Body B (Moderate)", "exercises": [
                make_ex("Deadlift", 3, "5-6", "180s"), make_ex("Overhead Press", 4, "8-10"),
                make_ex("Chin-Ups", 4, "8-10"), make_ex("Dumbbell Lunges", 3, "10/leg"),
                make_ex("Dumbbell Curl", 3, "12-15", "60s"), make_ex("Tricep Pushdowns", 3, "12-15", "60s")]},
            {"day_label": "Day 3: Full Body C (Volume)", "exercises": [
                make_ex("Front Squat", 3, "8-10"), make_ex("Dumbbell Incline Press", 3, "10-12"),
                make_ex("Seated Cable Row", 3, "10-12"), make_ex("Lateral Raises", 3, "15-20", "60s"),
                make_ex("Leg Curls", 3, "12-15", "60s"), make_ex("Calf Raises", 3, "15-20", "60s")]}
        ]
        tname = "Full Body Intermediate (3-Day)"
    elif sex == "female":
        days = [
            {"day_label": "Day 1: Full Body A", "exercises": [
                make_ex("Hip Thrust", 3, "10-12"), make_ex("Dumbbell Incline Press", 3, "10-12"),
                make_ex("Lat Pulldown", 3, "10-12"), make_ex("Lateral Raises", 3, "15-20", "60s"),
                make_ex("Plank", 3, "30s", "60s")]},
            {"day_label": "Day 2: Full Body B", "exercises": [
                make_ex("Barbell Squat", 3, "8-10"), make_ex("Dumbbell Row", 3, "10-12"),
                make_ex("Bench Press", 3, "10-12"), make_ex("Face Pulls", 3, "15-20", "60s"),
                make_ex("Glute Bridges", 3, "15-20", "60s")]},
            {"day_label": "Day 3: Full Body C", "exercises": [
                make_ex("Romanian Deadlift", 3, "10-12"), make_ex("Dumbbell Shoulder Press", 3, "10-12"),
                make_ex("Seated Cable Row", 3, "10-12"), make_ex("Bulgarian Split Squat", 3, "10/leg"),
                make_ex("Dead Bug", 3, "10/side", "60s")]}
        ]
        tname = "Women's Full Body (3-Day)"
    else:  # 4 day full body
        days = [
            {"day_label": "Day 1: Full Body (Squat Focus)", "exercises": [
                make_ex("Barbell Squat", 4, "6-8", "150s"), make_ex("Bench Press", 3, "8-10"),
                make_ex("Barbell Row", 3, "8-10"), make_ex("Lateral Raises", 3, "15-20", "60s"),
                make_ex("Plank", 3, "45s", "60s")]},
            {"day_label": "Day 2: Full Body (Press Focus)", "exercises": [
                make_ex("Overhead Press", 4, "6-8"), make_ex("Chin-Ups", 4, "8-10"),
                make_ex("Romanian Deadlift", 3, "10-12"), make_ex("Dumbbell Fly", 3, "12-15", "60s"),
                make_ex("Dumbbell Curl", 3, "12-15", "60s")]},
            {"day_label": "Day 3: Full Body (Deadlift Focus)", "exercises": [
                make_ex("Deadlift", 4, "5-6", "180s"), make_ex("Dumbbell Incline Press", 3, "10-12"),
                make_ex("Lat Pulldown", 3, "10-12"), make_ex("Dumbbell Lunges", 3, "10/leg"),
                make_ex("Tricep Pushdowns", 3, "12-15", "60s")]},
            {"day_label": "Day 4: Full Body (Volume)", "exercises": [
                make_ex("Front Squat", 3, "8-10"), make_ex("Dumbbell Shoulder Press", 3, "10-12"),
                make_ex("Seated Cable Row", 3, "10-12"), make_ex("Cable Fly", 3, "12-15", "60s"),
                make_ex("Face Pulls", 3, "15-20", "60s"), make_ex("Calf Raises", 3, "15-20", "60s")]}
        ]
        tname = "Full Body (4-Day)"
    
    templates.append({
        "id": gen_id(tname), "target": {"sex": sex, "goal": "Build Muscle", "level": level},
        "equipment": "Full Gym", "name": tname, "schedule": f"{days_per_week} days/week",
        "reasoning": f"Full body training {days_per_week}x/week for {level.lower()} lifters. Hits every muscle group each session for maximum frequency.",
        "days": days
    })

# --- Powerlifting / Strength ---
templates.append({
    "id": "powerlifting_peaking_4day", "target": {"sex": "any", "goal": "Strength / Powerlifting", "level": "Advanced"},
    "equipment": "Full Gym", "name": "Powerlifting Peaking (4-Day)", "schedule": "4 days/week",
    "reasoning": "Competition prep program focused on the big 3. Heavy singles and doubles with strategic accessory work for weak points.",
    "days": [
        {"day_label": "Day 1: Heavy Squat", "exercises": [
            make_ex("Barbell Squat", 5, "3", "300s"), make_ex("Pause Squat", 3, "3", "180s"),
            make_ex("Leg Press", 3, "8-10"), make_ex("Leg Curls", 3, "10-12"),
            make_ex("Plank", 3, "60s", "60s")]},
        {"day_label": "Day 2: Heavy Bench", "exercises": [
            make_ex("Bench Press", 5, "3", "300s"), make_ex("Close-Grip Bench Press", 3, "5-6", "150s"),
            make_ex("Dumbbell Incline Press", 3, "8-10"), make_ex("Barbell Row", 4, "6-8"),
            make_ex("Tricep Pushdowns", 3, "10-12", "60s")]},
        {"day_label": "Day 3: Heavy Deadlift", "exercises": [
            make_ex("Deadlift", 5, "3", "300s"), make_ex("Deficit Deadlift", 3, "3", "180s"),
            make_ex("Romanian Deadlift", 3, "8-10"), make_ex("Barbell Row", 3, "8-10"),
            make_ex("Hanging Leg Raise", 3, "10-15")]},
        {"day_label": "Day 4: Volume Day", "exercises": [
            make_ex("Front Squat", 3, "6-8", "150s"), make_ex("Incline Bench Press", 3, "8-10"),
            make_ex("Chin-Ups", 3, "8-10"), make_ex("Overhead Press", 3, "8-10"),
            make_ex("Face Pulls", 3, "15-20", "60s")]}
    ]
})

templates.append({
    "id": "powerlifting_beginner_3day", "target": {"sex": "any", "goal": "Strength / Powerlifting", "level": "Beginner"},
    "equipment": "Full Gym", "name": "Starting Strength Style (3-Day)", "schedule": "3 days/week",
    "reasoning": "Simple linear progression focusing on the main compound lifts. Add weight every session. Perfect for building a strength foundation.",
    "days": [
        {"day_label": "Day 1: Squat/Bench/Row", "exercises": [
            make_ex("Barbell Squat", 3, "5", "180s"), make_ex("Bench Press", 3, "5", "180s"),
            make_ex("Barbell Row", 3, "5", "150s")]},
        {"day_label": "Day 2: Squat/OHP/Deadlift", "exercises": [
            make_ex("Barbell Squat", 3, "5", "180s"), make_ex("Overhead Press", 3, "5", "180s"),
            make_ex("Deadlift", 1, "5", "180s")]},
        {"day_label": "Day 3: Squat/Bench/Row", "exercises": [
            make_ex("Barbell Squat", 3, "5", "180s"), make_ex("Bench Press", 3, "5", "180s"),
            make_ex("Barbell Row", 3, "5", "150s")]}
    ]
})

templates.append({
    "id": "powerlifting_5x5_3day", "target": {"sex": "any", "goal": "Strength / Powerlifting", "level": "Beginner"},
    "equipment": "Full Gym", "name": "5x5 Stronglifts Style (3-Day)", "schedule": "3 days/week (A/B alternating)",
    "reasoning": "Classic 5x5 program. Two workouts alternated across 3 training days. Simple, effective, progressive overload focused.",
    "days": [
        {"day_label": "Workout A", "exercises": [
            make_ex("Barbell Squat", 5, "5", "180s"), make_ex("Bench Press", 5, "5", "180s"),
            make_ex("Barbell Row", 5, "5", "150s")]},
        {"day_label": "Workout B", "exercises": [
            make_ex("Barbell Squat", 5, "5", "180s"), make_ex("Overhead Press", 5, "5", "180s"),
            make_ex("Deadlift", 1, "5", "180s")]}
    ]
})

templates.append({
    "id": "strength_531_4day", "target": {"sex": "any", "goal": "Strength / Powerlifting", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "5/3/1 Style (4-Day)", "schedule": "4 days/week",
    "reasoning": "Based on Wendler's 5/3/1. Each day has one main lift with a percentage-based progression, followed by assistance work.",
    "days": [
        {"day_label": "Day 1: OHP Day", "exercises": [
            make_ex("Overhead Press", 3, "5/3/1", "180s"), make_ex("Chin-Ups", 5, "10"),
            make_ex("Dumbbell Lunges", 3, "10/leg"), make_ex("Face Pulls", 3, "15-20", "60s"),
            make_ex("Dead Bug", 3, "10/side", "60s")]},
        {"day_label": "Day 2: Deadlift Day", "exercises": [
            make_ex("Deadlift", 3, "5/3/1", "240s"), make_ex("Barbell Row", 4, "8-10"),
            make_ex("Bulgarian Split Squat", 3, "10/leg"), make_ex("Hanging Leg Raise", 3, "10-15"),
            make_ex("Barbell Curl", 3, "10-12")]},
        {"day_label": "Day 3: Bench Day", "exercises": [
            make_ex("Bench Press", 3, "5/3/1", "180s"), make_ex("Dumbbell Row", 5, "10"),
            make_ex("Dips", 3, "8-12"), make_ex("Lateral Raises", 3, "15-20", "60s"),
            make_ex("Tricep Pushdowns", 3, "12-15", "60s")]},
        {"day_label": "Day 4: Squat Day", "exercises": [
            make_ex("Barbell Squat", 3, "5/3/1", "240s"), make_ex("Romanian Deadlift", 3, "10-12"),
            make_ex("Leg Press", 3, "10-12"), make_ex("Leg Curls", 3, "12-15", "60s"),
            make_ex("Plank", 3, "45s", "60s")]}
    ]
})

# --- Fat Loss / Conditioning ---
templates.append({
    "id": "fat_loss_full_body_3day", "target": {"sex": "any", "goal": "Lose Weight", "level": "Beginner"},
    "equipment": "Full Gym", "name": "Fat Loss Full Body (3-Day)", "schedule": "3 days/week",
    "reasoning": "Full body compound movements with shorter rest periods to maximize calorie burn while preserving muscle. Supersets increase metabolic demand.",
    "days": [
        {"day_label": "Day 1: Full Body A", "exercises": [
            make_ex("Barbell Squat", 3, "10-12"), make_ex("Bench Press", 3, "10-12"),
            make_ex("Barbell Row", 3, "10-12"), make_ex("Dumbbell Lunges", 3, "10/leg", "60s"),
            make_ex("Plank", 3, "30s", "60s"), make_ex("Jumping Jacks", 3, "60s", "30s")]},
        {"day_label": "Day 2: Full Body B", "exercises": [
            make_ex("Deadlift", 3, "8-10"), make_ex("Overhead Press", 3, "10-12"),
            make_ex("Lat Pulldown", 3, "10-12"), make_ex("Goblet Squat", 3, "12-15", "60s"),
            make_ex("Russian Twist", 3, "20", "60s"), make_ex("Mountain Climbers", 3, "30s", "30s")]},
        {"day_label": "Day 3: Full Body C", "exercises": [
            make_ex("Leg Press", 3, "12-15"), make_ex("Dumbbell Incline Press", 3, "10-12"),
            make_ex("Seated Cable Row", 3, "10-12"), make_ex("Bulgarian Split Squat", 3, "10/leg", "60s"),
            make_ex("Bicycle Crunches", 3, "20", "60s"), make_ex("Burpees", 3, "10", "60s")]}
    ]
})

templates.append({
    "id": "fat_loss_upper_lower_4day", "target": {"sex": "any", "goal": "Lose Weight", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Fat Loss Upper/Lower (4-Day)", "schedule": "4 days/week",
    "reasoning": "Upper/Lower split with metabolic finishers. Compound-focused with shorter rest periods. 4 days allows sufficient training volume while leaving recovery days for cardio.",
    "days": [
        {"day_label": "Day 1: Upper A", "exercises": [
            make_ex("Bench Press", 4, "8-10", "75s"), make_ex("Barbell Row", 4, "8-10", "75s"),
            make_ex("Overhead Press", 3, "10-12", "60s"), make_ex("Face Pulls", 3, "15-20", "45s"),
            make_ex("Dumbbell Curl", 3, "12-15", "45s"), make_ex("Tricep Pushdowns", 3, "12-15", "45s"),
            make_ex("Battle Ropes", 3, "30s", "30s")]},
        {"day_label": "Day 2: Lower A", "exercises": [
            make_ex("Barbell Squat", 4, "8-10", "90s"), make_ex("Romanian Deadlift", 3, "10-12", "75s"),
            make_ex("Leg Press", 3, "12-15", "60s"), make_ex("Leg Curls", 3, "12-15", "45s"),
            make_ex("Calf Raises", 3, "15-20", "45s"), make_ex("Burpees", 3, "10", "60s")]},
        {"day_label": "Day 3: Upper B", "exercises": [
            make_ex("Dumbbell Incline Press", 4, "10-12", "60s"), make_ex("Chin-Ups", 3, "AMRAP", "90s"),
            make_ex("Dumbbell Shoulder Press", 3, "10-12", "60s"), make_ex("Seated Cable Row", 3, "10-12", "60s"),
            make_ex("Lateral Raises", 3, "15-20", "45s"), make_ex("Mountain Climbers", 3, "30s", "30s")]},
        {"day_label": "Day 4: Lower B", "exercises": [
            make_ex("Deadlift", 3, "6-8", "120s"), make_ex("Bulgarian Split Squat", 3, "10-12/leg", "60s"),
            make_ex("Leg Extension", 3, "12-15", "45s"), make_ex("Hip Thrust", 3, "10-12", "60s"),
            make_ex("Standing Calf Raise Machine", 3, "15-20", "45s"), make_ex("Box Jumps", 3, "8", "60s")]}
    ]
})

templates.append({
    "id": "female_fat_loss_3day", "target": {"sex": "female", "goal": "Lose Weight", "level": "Beginner"},
    "equipment": "Full Gym", "name": "Women's Fat Loss (3-Day)", "schedule": "3 days/week",
    "reasoning": "Full body circuit-style workouts targeting large muscle groups for maximum calorie burn. Short rest periods keep heart rate elevated.",
    "days": [
        {"day_label": "Day 1: Full Body Circuit A", "exercises": [
            make_ex("Goblet Squat", 3, "12-15", "60s"), make_ex("Dumbbell Press", 3, "10-12", "60s"),
            make_ex("Lat Pulldown", 3, "10-12", "60s"), make_ex("Dumbbell Lunges", 3, "10/leg", "60s"),
            make_ex("Mountain Climbers", 3, "30s", "30s"), make_ex("Plank", 3, "30s", "30s")]},
        {"day_label": "Day 2: Full Body Circuit B", "exercises": [
            make_ex("Hip Thrust", 3, "12-15", "60s"), make_ex("Dumbbell Shoulder Press", 3, "10-12", "60s"),
            make_ex("Seated Cable Row", 3, "10-12", "60s"), make_ex("Step-ups", 3, "10/leg", "60s"),
            make_ex("Jumping Jacks", 3, "60s", "30s"), make_ex("Dead Bug", 3, "10/side", "30s")]},
        {"day_label": "Day 3: Full Body Circuit C", "exercises": [
            make_ex("Romanian Deadlift", 3, "10-12", "60s"), make_ex("Dumbbell Incline Press", 3, "10-12", "60s"),
            make_ex("Face Pulls", 3, "15-20", "45s"), make_ex("Bulgarian Split Squat", 3, "10/leg", "60s"),
            make_ex("Burpees", 3, "10", "60s"), make_ex("Russian Twist", 3, "20", "30s")]}
    ]
})

# --- General Fitness ---
templates.append({
    "id": "general_fitness_2day", "target": {"sex": "any", "goal": "General Fitness", "level": "Beginner"},
    "equipment": "Full Gym", "name": "Minimal Effective Dose (2-Day)", "schedule": "2 days/week",
    "reasoning": "For those who can only train twice per week. Full body sessions hitting every muscle group with compound movements. Minimal time, maximum benefit.",
    "days": [
        {"day_label": "Day 1: Full Body A", "exercises": [
            make_ex("Barbell Squat", 3, "8-10"), make_ex("Bench Press", 3, "8-10"),
            make_ex("Barbell Row", 3, "10-12"), make_ex("Dumbbell Shoulder Press", 2, "10-12"),
            make_ex("Plank", 3, "30s", "60s")]},
        {"day_label": "Day 2: Full Body B", "exercises": [
            make_ex("Deadlift", 3, "6-8", "150s"), make_ex("Dumbbell Incline Press", 3, "10-12"),
            make_ex("Lat Pulldown", 3, "10-12"), make_ex("Goblet Squat", 3, "12-15"),
            make_ex("Dead Bug", 3, "10/side", "60s")]}
    ]
})

# --- Senior / Masters ---
templates.append({
    "id": "senior_general_2day", "target": {"sex": "any", "goal": "General Fitness", "level": "Beginner"},
    "equipment": "Full Gym", "name": "Senior Fitness (2-Day)", "schedule": "2 days/week",
    "reasoning": "Safe, joint-friendly program for older adults. Machine-based exercises reduce injury risk while maintaining strength and mobility.",
    "days": [
        {"day_label": "Day 1: Full Body A", "exercises": [
            make_ex("Leg Press", 3, "10-12"), make_ex("Machine Chest Press", 3, "10-12"),
            make_ex("Machine Row", 3, "10-12"), make_ex("Machine Shoulder Press", 2, "10-12"),
            make_ex("Calf Raises", 2, "15-20", "60s"), make_ex("Plank", 2, "20s", "60s")]},
        {"day_label": "Day 2: Full Body B", "exercises": [
            make_ex("Smith Machine Squat", 3, "10-12"), make_ex("Lat Pulldown", 3, "10-12"),
            make_ex("Pec Deck", 3, "12-15", "60s"), make_ex("Leg Extension", 2, "12-15", "60s"),
            make_ex("Seated Leg Curl", 2, "12-15", "60s"), make_ex("Dead Bug", 3, "8/side", "60s")]}
    ]
})

templates.append({
    "id": "senior_strength_3day", "target": {"sex": "any", "goal": "Strength / Powerlifting", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Masters Strength (3-Day)", "schedule": "3 days/week",
    "reasoning": "Strength program adapted for lifters 50+. Lower volume per session with emphasis on form and joint health. Still progressive, still effective.",
    "days": [
        {"day_label": "Day 1: Squat Day", "exercises": [
            make_ex("Barbell Squat", 4, "5-6", "180s"), make_ex("Leg Press", 3, "8-10"),
            make_ex("Leg Curls", 3, "10-12"), make_ex("Plank", 3, "30s", "60s")]},
        {"day_label": "Day 2: Bench Day", "exercises": [
            make_ex("Bench Press", 4, "5-6", "180s"), make_ex("Dumbbell Row", 4, "8-10"),
            make_ex("Dumbbell Shoulder Press", 3, "10-12"), make_ex("Face Pulls", 3, "15-20", "60s")]},
        {"day_label": "Day 3: Deadlift Day", "exercises": [
            make_ex("Deadlift", 3, "5", "240s"), make_ex("Romanian Deadlift", 3, "8-10"),
            make_ex("Chin-Ups", 3, "AMRAP"), make_ex("Dumbbell Curl", 3, "12-15", "60s"),
            make_ex("Calf Raises", 3, "15-20", "60s")]}
    ]
})

# --- Weak Point Specialization ---
for focus, focus_name in [("chest", "Chest"), ("back", "Back"), ("shoulders", "Shoulders"), ("arms", "Arms"), ("legs", "Legs"), ("glutes", "Glutes")]:
    if focus == "chest":
        days = [
            {"day_label": "Day 1: Chest Priority", "exercises": [
                make_ex("Bench Press", 5, "6-10"), make_ex("Incline Bench Press", 4, "8-10"),
                make_ex("Cable Fly", 4, "12-15", "60s"), make_ex("Dumbbell Fly", 3, "12-15", "60s"),
                make_ex("Cable Crossover", 3, "15-20", "60s")]},
            {"day_label": "Day 2: Back & Shoulders", "exercises": [
                make_ex("Barbell Row", 4, "8-10"), make_ex("Pull-Ups", 3, "8-10"),
                make_ex("Overhead Press", 3, "8-10"), make_ex("Lateral Raises", 3, "15-20", "60s"),
                make_ex("Face Pulls", 3, "15-20", "60s")]},
            {"day_label": "Day 3: Legs", "exercises": [
                make_ex("Barbell Squat", 4, "8-10"), make_ex("Romanian Deadlift", 3, "10-12"),
                make_ex("Leg Press", 3, "10-12"), make_ex("Leg Curls", 3, "12-15", "60s"),
                make_ex("Calf Raises", 4, "15-20", "60s")]},
            {"day_label": "Day 4: Chest + Arms", "exercises": [
                make_ex("Dumbbell Incline Press", 4, "10-12"), make_ex("Pec Deck", 3, "12-15", "60s"),
                make_ex("Dips", 3, "8-12"), make_ex("Barbell Curl", 3, "10-12"),
                make_ex("Skull Crushers", 3, "10-12"), make_ex("Hammer Curl", 3, "12-15", "60s")]}
        ]
    elif focus == "back":
        days = [
            {"day_label": "Day 1: Back Priority (Width)", "exercises": [
                make_ex("Pull-Ups", 5, "AMRAP"), make_ex("Lat Pulldown", 4, "10-12"),
                make_ex("Dumbbell Pullover", 3, "12-15"), make_ex("Straight-arm Cable Pulldown", 3, "12-15", "60s") if False else make_ex("Face Pulls", 3, "15-20", "60s"),
                make_ex("Barbell Curl", 3, "10-12")]},
            {"day_label": "Day 2: Chest & Shoulders", "exercises": [
                make_ex("Bench Press", 4, "8-10"), make_ex("Overhead Press", 3, "8-10"),
                make_ex("Cable Fly", 3, "12-15", "60s"), make_ex("Lateral Raises", 3, "15-20", "60s"),
                make_ex("Tricep Pushdowns", 3, "12-15", "60s")]},
            {"day_label": "Day 3: Legs", "exercises": [
                make_ex("Barbell Squat", 4, "8-10"), make_ex("Romanian Deadlift", 3, "10-12"),
                make_ex("Leg Press", 3, "10-12"), make_ex("Leg Curls", 3, "12-15", "60s"),
                make_ex("Calf Raises", 4, "15-20", "60s")]},
            {"day_label": "Day 4: Back Priority (Thickness)", "exercises": [
                make_ex("Barbell Row", 5, "6-8"), make_ex("Seated Cable Row", 4, "10-12"),
                make_ex("Pendlay Row", 3, "6-8"), make_ex("Dumbbell Shrug", 3, "12-15"),
                make_ex("Reverse Pec Deck", 3, "15-20", "60s")]}
        ]
    elif focus == "shoulders":
        days = [
            {"day_label": "Day 1: Shoulder Priority", "exercises": [
                make_ex("Overhead Press", 5, "6-8"), make_ex("Dumbbell Arnold Press", 4, "10-12"),
                make_ex("Lateral Raises", 5, "15-20", "45s"), make_ex("Face Pulls", 4, "15-20", "60s"),
                make_ex("Dumbbell Front Raise", 3, "12-15", "60s")]},
            {"day_label": "Day 2: Chest & Back", "exercises": [
                make_ex("Bench Press", 4, "8-10"), make_ex("Barbell Row", 4, "8-10"),
                make_ex("Dumbbell Incline Press", 3, "10-12"), make_ex("Lat Pulldown", 3, "10-12"),
                make_ex("Cable Fly", 3, "12-15", "60s")]},
            {"day_label": "Day 3: Legs", "exercises": [
                make_ex("Barbell Squat", 4, "8-10"), make_ex("Romanian Deadlift", 3, "10-12"),
                make_ex("Leg Press", 3, "10-12"), make_ex("Leg Curls", 3, "12-15", "60s"),
                make_ex("Calf Raises", 4, "15-20", "60s")]},
            {"day_label": "Day 4: Shoulders + Arms", "exercises": [
                make_ex("Push Press", 4, "6-8"), make_ex("Cable Lateral Raise", 4, "15-20", "45s"),
                make_ex("Rear Delt Fly", 4, "15-20", "60s"), make_ex("Barbell Curl", 3, "10-12"),
                make_ex("Skull Crushers", 3, "10-12")]}
        ]
    elif focus == "arms":
        days = [
            {"day_label": "Day 1: Arms Priority", "exercises": [
                make_ex("Close-Grip Bench Press", 4, "6-8"), make_ex("Barbell Curl", 4, "6-8"),
                make_ex("Skull Crushers", 3, "10-12"), make_ex("Incline Dumbbell Curl", 3, "10-12"),
                make_ex("Cable Overhead Tricep Extension", 3, "12-15", "60s"), make_ex("Hammer Curl", 3, "10-12"),
                make_ex("Tricep Pushdowns", 3, "15-20", "45s")]},
            {"day_label": "Day 2: Chest & Back", "exercises": [
                make_ex("Bench Press", 4, "8-10"), make_ex("Barbell Row", 4, "8-10"),
                make_ex("Dumbbell Incline Press", 3, "10-12"), make_ex("Lat Pulldown", 3, "10-12"),
                make_ex("Lateral Raises", 3, "15-20", "60s")]},
            {"day_label": "Day 3: Legs", "exercises": [
                make_ex("Barbell Squat", 4, "8-10"), make_ex("Romanian Deadlift", 3, "10-12"),
                make_ex("Leg Press", 3, "10-12"), make_ex("Leg Curls", 3, "12-15", "60s"),
                make_ex("Calf Raises", 4, "15-20", "60s")]},
            {"day_label": "Day 4: Arms + Shoulders", "exercises": [
                make_ex("Dips", 4, "8-12"), make_ex("Chin-Ups", 4, "8-10"),
                make_ex("Dumbbell Tricep Extension", 3, "12-15", "60s"), make_ex("Concentration Curl", 3, "12-15", "60s"),
                make_ex("Overhead Press", 3, "8-10"), make_ex("Dumbbell Shrug", 3, "12-15", "60s")]}
        ]
    elif focus == "legs":
        days = [
            {"day_label": "Day 1: Quad Priority", "exercises": [
                make_ex("Barbell Squat", 5, "6-10", "180s"), make_ex("Front Squat", 3, "8-10", "150s"),
                make_ex("Leg Press", 4, "10-12"), make_ex("Leg Extension", 3, "12-15", "60s"),
                make_ex("Calf Raises", 4, "15-20", "60s")]},
            {"day_label": "Day 2: Upper Body", "exercises": [
                make_ex("Bench Press", 4, "8-10"), make_ex("Barbell Row", 4, "8-10"),
                make_ex("Overhead Press", 3, "8-10"), make_ex("Chin-Ups", 3, "8-10"),
                make_ex("Face Pulls", 3, "15-20", "60s")]},
            {"day_label": "Day 3: Hamstring/Glute Priority", "exercises": [
                make_ex("Deadlift", 4, "5-6", "180s"), make_ex("Romanian Deadlift", 3, "8-10"),
                make_ex("Hip Thrust", 4, "10-12"), make_ex("Leg Curls", 4, "12-15", "60s"),
                make_ex("Bulgarian Split Squat", 3, "10/leg")]},
            {"day_label": "Day 4: Upper + Leg Volume", "exercises": [
                make_ex("Dumbbell Incline Press", 3, "10-12"), make_ex("Seated Cable Row", 3, "10-12"),
                make_ex("Hack Squat", 3, "10-12"), make_ex("Seated Leg Curl", 3, "12-15", "60s"),
                make_ex("Standing Calf Raise Machine", 4, "15-20", "60s")]}
        ]
    else:  # glutes
        days = [
            {"day_label": "Day 1: Glute Priority A", "exercises": [
                make_ex("Hip Thrust", 5, "8-12"), make_ex("Romanian Deadlift", 4, "10-12"),
                make_ex("Bulgarian Split Squat", 3, "10-12/leg"), make_ex("Cable Kickback", 3, "12-15/leg", "60s"),
                make_ex("Hip Abductor Machine", 3, "15-20", "60s")]},
            {"day_label": "Day 2: Upper Body", "exercises": [
                make_ex("Bench Press", 3, "8-10"), make_ex("Barbell Row", 3, "8-10"),
                make_ex("Overhead Press", 3, "10-12"), make_ex("Lat Pulldown", 3, "10-12"),
                make_ex("Face Pulls", 3, "15-20", "60s")]},
            {"day_label": "Day 3: Glute Priority B", "exercises": [
                make_ex("Barbell Squat", 4, "8-10"), make_ex("Sumo Deadlift", 3, "8-10"),
                make_ex("Dumbbell Step-Up", 3, "10/leg"), make_ex("Cable Pull-Through", 3, "12-15", "60s"),
                make_ex("Glute Bridges", 3, "15-20", "60s")]},
            {"day_label": "Day 4: Legs + Upper", "exercises": [
                make_ex("Leg Press", 3, "10-12"), make_ex("Seated Leg Curl", 3, "12-15", "60s"),
                make_ex("Dumbbell Shoulder Press", 3, "10-12"), make_ex("Seated Cable Row", 3, "10-12"),
                make_ex("Calf Raises", 3, "15-20", "60s")]}
        ]
    
    templates.append({
        "id": gen_id(f"weak_point_{focus}_4day"),
        "target": {"sex": "female" if focus == "glutes" else "any", "goal": "Build Muscle", "level": "Intermediate"},
        "equipment": "Full Gym",
        "name": f"{focus_name} Specialization (4-Day)",
        "schedule": "4 days/week",
        "reasoning": f"Specialized program that prioritizes {focus_name.lower()} development with 2 dedicated sessions per week while maintaining other muscle groups.",
        "days": days
    })

# --- Sport-Specific ---
templates.append({
    "id": "athletic_performance_4day", "target": {"sex": "any", "goal": "General Fitness", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Athletic Performance (4-Day)", "schedule": "4 days/week",
    "reasoning": "Balanced program for general athleticism. Combines strength, power, and conditioning. Great for recreational athletes or anyone wanting functional fitness.",
    "days": [
        {"day_label": "Day 1: Lower Power", "exercises": [
            make_ex("Barbell Squat", 4, "5-6", "180s"), make_ex("Box Jumps", 4, "5", "120s"),
            make_ex("Romanian Deadlift", 3, "8-10"), make_ex("Bulgarian Split Squat", 3, "8/leg"),
            make_ex("Plank", 3, "45s", "60s")]},
        {"day_label": "Day 2: Upper Power", "exercises": [
            make_ex("Bench Press", 4, "5-6", "150s"), make_ex("Pull-Ups", 4, "6-8"),
            make_ex("Push Press", 3, "6-8"), make_ex("Barbell Row", 3, "6-8"),
            make_ex("Battle Ropes", 3, "30s", "60s")]},
        {"day_label": "Day 3: Lower Volume", "exercises": [
            make_ex("Front Squat", 3, "8-10"), make_ex("Hip Thrust", 3, "10-12"),
            make_ex("Dumbbell Lunges", 3, "10/leg", "60s"), make_ex("Leg Curls", 3, "12-15", "60s"),
            make_ex("Calf Raises", 3, "15-20", "60s"), make_ex("Broad Jump", 3, "5", "60s")]},
        {"day_label": "Day 4: Upper Volume", "exercises": [
            make_ex("Dumbbell Incline Press", 3, "10-12"), make_ex("Seated Cable Row", 3, "10-12"),
            make_ex("Dumbbell Shoulder Press", 3, "10-12"), make_ex("Face Pulls", 3, "15-20", "60s"),
            make_ex("Dumbbell Curl", 3, "12-15", "60s"), make_ex("Tricep Pushdowns", 3, "12-15", "60s")]}
    ]
})

templates.append({
    "id": "football_offseason_4day", "target": {"sex": "male", "goal": "Strength / Powerlifting", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Football Off-Season (4-Day)", "schedule": "4 days/week",
    "reasoning": "Power and strength focused for football athletes. Heavy compound lifts with explosive movements. Builds the raw strength and power needed on the field.",
    "days": [
        {"day_label": "Day 1: Max Effort Lower", "exercises": [
            make_ex("Barbell Squat", 5, "3-5", "240s"), make_ex("Deadlift", 3, "3-5", "240s"),
            make_ex("Box Jumps", 4, "5", "120s"), make_ex("Glute Bridges", 3, "10-12"),
            make_ex("Hanging Leg Raise", 3, "10-15")]},
        {"day_label": "Day 2: Max Effort Upper", "exercises": [
            make_ex("Bench Press", 5, "3-5", "240s"), make_ex("Barbell Row", 4, "5-6", "150s"),
            make_ex("Push Press", 3, "5-6"), make_ex("Pull-Ups", 3, "AMRAP"),
            make_ex("Face Pulls", 3, "15-20", "60s")]},
        {"day_label": "Day 3: Dynamic Lower", "exercises": [
            make_ex("Front Squat", 4, "6-8", "150s"), make_ex("Romanian Deadlift", 3, "8-10"),
            make_ex("Bulgarian Split Squat", 3, "8/leg"), make_ex("Leg Curls", 3, "10-12"),
            make_ex("Battle Ropes", 3, "30s", "60s")]},
        {"day_label": "Day 4: Dynamic Upper", "exercises": [
            make_ex("Incline Bench Press", 4, "6-8"), make_ex("Pendlay Row", 4, "6-8"),
            make_ex("Dumbbell Shoulder Press", 3, "8-10"), make_ex("Chin-Ups", 3, "8-10"),
            make_ex("Close-Grip Bench Press", 3, "8-10"), make_ex("Barbell Curl", 3, "10-12")]}
    ]
})

templates.append({
    "id": "basketball_training_3day", "target": {"sex": "any", "goal": "General Fitness", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Basketball Training (3-Day)", "schedule": "3 days/week",
    "reasoning": "Athletic program for basketball players. Focus on vertical power, lateral agility, and injury prevention. Lower body power + upper body strength.",
    "days": [
        {"day_label": "Day 1: Power & Strength", "exercises": [
            make_ex("Barbell Squat", 4, "5-6", "180s"), make_ex("Box Jumps", 4, "5", "120s"),
            make_ex("Bench Press", 3, "8-10"), make_ex("Pull-Ups", 3, "8-10"),
            make_ex("Plank", 3, "45s", "60s")]},
        {"day_label": "Day 2: Explosive & Conditioning", "exercises": [
            make_ex("Deadlift", 3, "5", "180s"), make_ex("Broad Jump", 4, "5", "90s"),
            make_ex("Dumbbell Lunges", 3, "8/leg"), make_ex("Overhead Press", 3, "8-10"),
            make_ex("Battle Ropes", 3, "30s", "60s"), make_ex("Mountain Climbers", 3, "30s", "30s")]},
        {"day_label": "Day 3: Strength & Prevention", "exercises": [
            make_ex("Front Squat", 3, "8-10"), make_ex("Romanian Deadlift", 3, "10-12"),
            make_ex("Hip Thrust", 3, "10-12"), make_ex("Dumbbell Row", 3, "10-12"),
            make_ex("Face Pulls", 3, "15-20", "60s"), make_ex("Calf Raises", 3, "15-20", "60s")]}
    ]
})

templates.append({
    "id": "soccer_training_3day", "target": {"sex": "any", "goal": "General Fitness", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Soccer Training (3-Day)", "schedule": "3 days/week",
    "reasoning": "Designed for soccer players: lower body endurance, single-leg stability, and core strength. Minimizes upper body bulk while maintaining functional strength.",
    "days": [
        {"day_label": "Day 1: Lower Power", "exercises": [
            make_ex("Barbell Squat", 4, "5-6", "180s"), make_ex("Bulgarian Split Squat", 3, "8/leg"),
            make_ex("Romanian Deadlift", 3, "8-10"), make_ex("Box Jumps", 3, "5", "90s"),
            make_ex("Plank", 3, "45s", "60s")]},
        {"day_label": "Day 2: Upper + Core", "exercises": [
            make_ex("Bench Press", 3, "8-10"), make_ex("Barbell Row", 3, "8-10"),
            make_ex("Overhead Press", 3, "10-12"), make_ex("Face Pulls", 3, "15-20", "60s"),
            make_ex("Cable Woodchop", 3, "12/side", "60s"), make_ex("Dead Bug", 3, "10/side", "60s")]},
        {"day_label": "Day 3: Lower Endurance", "exercises": [
            make_ex("Front Squat", 3, "10-12"), make_ex("Dumbbell Step-Up", 3, "10/leg"),
            make_ex("Hip Thrust", 3, "12-15"), make_ex("Leg Curls", 3, "12-15", "60s"),
            make_ex("Calf Raises", 4, "15-20", "60s"), make_ex("Side Plank", 3, "30s/side", "30s")]}
    ]
})

templates.append({
    "id": "swimming_dryland_3day", "target": {"sex": "any", "goal": "General Fitness", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Swimming Dryland (3-Day)", "schedule": "3 days/week",
    "reasoning": "Dryland training for swimmers. Focus on lat strength, shoulder stability, and core power. Complements pool training without excessive fatigue.",
    "days": [
        {"day_label": "Day 1: Pull Focus", "exercises": [
            make_ex("Pull-Ups", 4, "8-10"), make_ex("Lat Pulldown", 3, "10-12"),
            make_ex("Dumbbell Pullover", 3, "12-15"), make_ex("Face Pulls", 3, "15-20", "60s"),
            make_ex("Plank", 3, "45s", "60s")]},
        {"day_label": "Day 2: Core & Legs", "exercises": [
            make_ex("Barbell Squat", 3, "8-10"), make_ex("Romanian Deadlift", 3, "10-12"),
            make_ex("Cable Woodchop", 3, "12/side", "60s"), make_ex("V-Up", 3, "15"),
            make_ex("Flutter Kicks", 3, "30s", "30s"), make_ex("Calf Raises", 3, "15-20", "60s")]},
        {"day_label": "Day 3: Push & Stability", "exercises": [
            make_ex("Bench Press", 3, "8-10"), make_ex("Overhead Press", 3, "10-12"),
            make_ex("Lateral Raises", 3, "15-20", "60s"), make_ex("Dumbbell Row", 3, "10-12"),
            make_ex("Hollow Body Hold", 3, "30s", "60s"), make_ex("Superman", 3, "15")]}
    ]
})

# --- Endurance ---
templates.append({
    "id": "runner_strength_2day", "target": {"sex": "any", "goal": "General Fitness", "level": "Intermediate"},
    "equipment": "Full Gym", "name": "Runner's Strength (2-Day)", "schedule": "2 days/week",
    "reasoning": "Supplemental strength training for runners. Focus on single-leg stability, hip strength, and injury prevention. Designed to complement running without causing excess fatigue.",
    "days": [
        {"day_label": "Day 1: Lower Focus", "exercises": [
            make_ex("Barbell Squat", 3, "6-8"), make_ex("Bulgarian Split Squat", 3, "8/leg"),
            make_ex("Romanian Deadlift", 3, "8-10"), make_ex("Calf Raises", 3, "15-20", "60s"),
            make_ex("Plank", 3, "45s", "60s"), make_ex("Side Plank", 2, "30s/side", "30s")]},
        {"day_label": "Day 2: Full Body", "exercises": [
            make_ex("Deadlift", 3, "5-6", "150s"), make_ex("Dumbbell Step-Up", 3, "8/leg"),
            make_ex("Hip Thrust", 3, "10-12"), make_ex("Dumbbell Row", 3, "10-12"),
            make_ex("Overhead Press", 3, "10-12"), make_ex("Dead Bug", 3, "10/side", "60s")]}
    ]
})

# --- Mobility ---
templates.append({
    "id": "mobility_flexibility_3day", "target": {"sex": "any", "goal": "General Fitness", "level": "Beginner"},
    "equipment": "No Equipment", "name": "Mobility & Flexibility (3-Day)", "schedule": "3 days/week",
    "reasoning": "Dedicated mobility program for those who need to improve flexibility and joint health. Can be used standalone or as a supplement to strength training.",
    "days": [
        {"day_label": "Day 1: Lower Body Mobility", "exercises": [
            make_ex("Cat-Cow Stretch", 3, "10", "30s"), make_ex("World's Greatest Stretch", 3, "5/side", "30s"),
            make_ex("90/90 Hip Stretch", 3, "30s/side", "30s"), make_ex("Couch Stretch", 3, "30s/side", "30s"),
            make_ex("Bodyweight Squat Hold", 3, "30s", "30s"), make_ex("Glute Bridges", 3, "15", "30s")]},
        {"day_label": "Day 2: Upper Body Mobility", "exercises": [
            make_ex("Cat-Cow Stretch", 3, "10", "30s"), make_ex("Foam Roll (Upper Back)", 3, "60s", "30s"),
            make_ex("Inchworm", 3, "8", "30s"), make_ex("Dead Bug", 3, "10/side", "30s"),
            make_ex("Side Plank", 3, "20s/side", "30s"), make_ex("Superman", 3, "10", "30s")]},
        {"day_label": "Day 3: Full Body Flow", "exercises": [
            make_ex("World's Greatest Stretch", 3, "5/side", "30s"), make_ex("Cat-Cow Stretch", 3, "10", "30s"),
            make_ex("Bear Crawl", 3, "30s", "30s"), make_ex("Inchworm", 3, "8", "30s"),
            make_ex("90/90 Hip Stretch", 3, "30s/side", "30s"), make_ex("Hollow Body Hold", 3, "20s", "30s")]}
    ]
})


# ============================================================================
# HOME GYM: DUMBBELLS + BENCH
# ============================================================================

templates.append({
    "id": "db_full_body_3day_beginner", "target": {"sex": "any", "goal": "Build Muscle", "level": "Beginner"},
    "equipment": "Dumbbells Only", "name": "Dumbbell Full Body (3-Day Beginner)", "schedule": "3 days/week",
    "reasoning": "Full body dumbbell training perfect for home gym with just dumbbells and a bench. Hits every muscle group 3x/week for maximum beginner gains.",
    "days": [
        {"day_label": "Day 1: Full Body A", "exercises": [
            make_ex("Goblet Squat", 3, "10-12"), make_ex("Dumbbell Bench Press", 3, "10-12"),
            make_ex("Dumbbell Row", 3, "10-12"), make_ex("Dumbbell Shoulder Press", 2, "10-12"),
            make_ex("Plank", 3, "30s", "60s")]},
        {"day_label": "Day 2: Full Body B", "exercises": [
            make_ex("Dumbbell RDL", 3, "10-12"), make_ex("Dumbbell Incline Press", 3, "10-12"),