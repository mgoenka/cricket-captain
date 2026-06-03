---
name: cricket-strategy
description: Build a comprehensive T20 cricket match plan for club-level cricket. Use when the user mentions cricket strategy, match plan, batting order, bowling order, opening pair, toss strategy, fielding plan, head-to-head, or any upcoming cricket match. Outputs internal captain analysis plus a WhatsApp-ready team summary in the captain's voice.
---

# Cricket Match Strategy

This skill builds a full pre-match plan for a T20 cricket club match: toss call, batting order, bowling rotation, fielding plan, opposition matchups, and a WhatsApp-ready summary the captain can paste into the team chat.

The skill is **format-agnostic** for the methodology (T20 club cricket fundamentals apply broadly), but pulls team-specific data from the **captain's cricket data directory** at `~/Dev/cricket/`. If that directory doesn't exist yet, prompt the user to run the setup steps in this plugin's README (see `assets/README.md`).

## Setup expectations (Phase 0)

Before building a plan, this skill assumes the following data exists at `~/Dev/cricket/`:

```
~/Dev/cricket/
├── team/
│   ├── roster.md          # current XI player profiles
│   └── trend.md           # season form, recent results
├── opponents/             # one file per regular opponent
│   └── <opponent>.md
├── grounds/               # one file per ground we play
│   └── <ground>.md
├── scorecards/<year>/     # raw scorecards by date
└── plans/<year>/          # saved match plans (captain's + team summaries)
```

Templates for each file type live in this plugin under `assets/templates/`. Copy them to the user's data directory and fill in. If the user hasn't done setup, walk them through it briefly before building the first plan.

## Inputs the user typically provides

**Minimum required** (only ask for what's NOT already in the cricket data directory):
- **Match metadata** — date, time, opposition, ground name, tournament.
- **Confirmed XI** — list of 11 players. If all 11 are in `team/roster.md`, pull profiles automatically. If any are new, ask for their role/stats.
- **Pre-match intel** (if any) — pitch tip, opposition lineup hint, weather, dew.

**Optional**:
- Recent scorecards, head-to-head data, career stats for new players, weather forecast (or fetch via web).

**Do NOT ask** for things already saved in the data directory:
- Player batting position preferences, bowling capacity, fielding strengths.
- BaPP/BoPP timing defaults, first-over bowler, distribution patterns.
- Field position conventions, player name preferences.

If any minimum-required input is missing, ASK. Never invent stats.

### Plan for opposition unknowns by default

Opposition teams typically do NOT share their lineups before matches. Don't ask the user to confirm the opposition XI — they won't know. **Assume the opposition might field 1-2 players you haven't seen in their recent scorecards.**

This means:
- **Build flexibility into the bowling plan**: rather than optimizing for a specific predicted batting order, plan a bowling rotation that works against any reasonable order. Bring the best wicket-taker on early.
- **Don't lock matchups too tight**: a default plan like "Best bowler at over 9 vs their #5" is fine, but the captain should be ready to adapt.
- **Treat the predicted lineup as a guide, not a contract**.

### Pre-match intel still helps when available

If the captain has gotten intel from someone reliable (former teammate, friend on another team, scout), use it:
- "Tough pitch" intel → lead the team summary with survival-mode batting approach.
- "Their bowler X is on form" → build a specific matchup plan against him.
- "Ground has dew till 11 AM" → account for it in toss + rotation.

But **don't ASK the user for intel they don't have**. Plan for unknowns first; treat any intel as a bonus.

## Always check these external signals (do NOT skip)

Before finalizing the plan, ALWAYS run these checks. They take 30 seconds each and significantly sharpen the strategy.

### Weather check (mandatory)

Run a web search for "[city/region weather forecast [match date] morning/afternoon]". Capture:
- High and low temp
- Sunrise time (relevant for dew at early-morning games)
- Rain chance (% probability)
- Conditions: foggy, sunny, cloudy, windy
- UV index (relevant for outfielders)

**Implications by condition** (interpret based on equipment — see below):

| Condition | Implication |
|---|---|
| Foggy morning, dew possible | Affects ball grip more than swing/seam. Outfield slow till dew burns off. Ball travels less in cold. |
| Sunny, dry | Outfield faster after warm-up. Watch UV for outfielders. |
| Windy | Field setting must account for wind direction (long boundary = upwind, short = downwind). Skiers and swingers in the air. |
| Hot afternoon (>85°F) | Drinks breaks important. Tail-end tiredness for bowlers. |
| Rain risk >30% | Plan DLS scenario. Consider taking BPP earlier so par scores are met if rain comes. |

### Equipment: tennis ball vs leather ball

Many club leagues use a **hard tennis ball**, not a leather/cork ball. If the user's league uses tennis ball:

- **No meaningful swing or seam** — the ball comes on straight. Don't plan around "morning swing" or "new ball seam movement" in messaging.
- **Predictable bounce on hard surfaces**. Variable bounce on matting because skid is amplified.
- **Wet ball matters** — dew makes the ball slippery (grip issue, especially for spinners). Less about swing, more about ball-handling.
- **Ageing**: tennis ball loses bounce as it scuffs. Slower bowlers/spinners more effective later.
- **Bouncers**: typically not allowed in tennis-ball leagues (shoulder-height = no-ball).

When writing conditions in team summary: focus on **temperature, wind direction, pitch type, dew (for grip), wet pitch (for batting difficulty)**. Skip "swing" and "seam" language unless conditions are unusual.

Check `team/roster.md` or `assets/templates/team-roster-template.md` for an `equipment: tennis-ball` flag at the top.

### Pitch type and ground category (mandatory)

Most club grounds fall into 3 categories that play very differently:

**BB (Baseball ground)**:
- Smaller offside (compressed because the diamond is overlaid on a baseball field)
- Mostly natural grass / dirt
- Square boundaries shorter, especially leg-side
- Pull shots and pulls into the leg side are very productive
- Field tip: deep midwicket and deep square leg are critical
- **NO deep cover needed** — the short offside is protected by ring fielders

**360T (Turf ground, full 360)**:
- Full-sized cricket ground with turf pitch
- Variable bounce as game progresses
- Spinners get more turn after over 10
- Larger boundaries — boundary clearance matters

**360M (Matting ground, full 360)**:
- Synthetic matting laid over hard base
- Predictable bounce, lower carry
- **Ball skids off the surface** — harder for batters to time, easier for bowlers to attack stumps
- Cut and pull shots work well
- Yorkers king at the death
- Larger boundaries than BB but smaller than 360T

**Player ground splits matter**: check each player's profile for ground-type splits if available. A player who's strong on BB may struggle on 360M.

### Time-of-day audit (mandatory)

Filter ground stats by start time slot. Morning games (early start) and afternoon games (later start) at the same ground play very differently. Dew, sun angle, pitch hardness, and outfield speed all change. **Only weight games from the same time slot as your match.**

## Club cricket fair-chance principle (HARD RULES, not tiebreakers)

Club cricket is a weekend league. Players show up to play AND to enjoy the game. These are **hard rules** unless the user explicitly overrides them:

### Rule 1: Pure batsmen go in the top 6 of the batting order

**Always.** No exceptions based on recent form. This includes:
- The captain, regardless of his last 5 scores
- Any batter who does not bowl

**Why it matters**: a pure batsman parked at #7+ may not even get to bat. They came to bat. Give them a chance. **Form does NOT override this rule** — bad form for a few games is often noise.

### Rule 2: Distribute bowling overs as evenly as possible

**Even distribution beats concentration**, even if some bowlers are stronger. A team where everyone gets 3 overs is better than a team where the top 4 get 4 overs and the bottom bowler gets 1.

**Standard distribution for 20 overs across 6 bowlers:**

| Distribution | Pattern | Verdict |
|---|---|---|
| **4-4-3-3-3-3** | 2 strongest get 4, others 3 | **Default — most fair when all 6 are regular bowlers** |
| **4-4-4-4-2-2** | 4 regulars get 4, 2 part-timers get 2 | **Use when 2 of the 6 are part-timers** (haven't been bowling regularly) |
| 4-4-4-3-3-2 | 3 strongest get 4, 1 gets 2 | Acceptable only if the 2-over bowler is an all-rounder |
| 4-4-4-4-3-1 | Top 4 get full quota, 1 gets 1 | **Avoid.** The 1-over bowler is marginalized. |

**Distinguishing regulars from part-timers**: A bowler is a **regular** if they've bowled 3+ overs in 3+ of the last 5 games they played. They're a **part-timer** if they've bowled 0-2 overs per game on average in recent matches, even if their career figures show they used to bowl more.

**Equal-caliber tiebreak**: when two bowlers are of equal caliber (similar economy, similar matchup, similar recent form), give more overs to the bowler who **bats lower in the order**. Balance their match contribution.

**Batting compensation rule (mirror of the bowling rule)**: among players in the 7-11 batting tier, **players who bowl fewer overs should bat higher**. A 2-over bowler with decent batting at #7 beats a 4-over bowler at #7. Combine with recent batting form.

**Pure vs all-rounder cuts**:
- If math forces someone below 3 overs, cut from an all-rounder (they still contribute with bat).
- Never cut a pure bowler below 3 overs unless they bowl badly on the day AND you have a backup.

### Rule 3: All-rounders take the flex

All-rounders contribute with both bat and ball. They absorb the cuts in either column.

### Rule 4: Tail order matches what they actually do

Tail (#9-11) = pure bowlers who don't bat well. Don't shuffle for game state.

## Power plays (CRITICAL — club leagues often differ from ICC T20)

**Many club leagues do NOT have an automatic powerplay in overs 1-6 like ICC T20 rules.** Confirm the league's rules. In some club leagues (like CricBay):

- **No automatic field restriction in overs 1-6.** Default field across the entire innings is max 4 fielders outside the inner circle.
- **6 PP overs total per innings**: 3 batting (BaPP) + 3 bowling (BoPP), scattered across the innings.
- **Both PPs are the captain's choice over by over.** Neither is mandatory at the start.
- **In a PP over**: only **2 fielders** outside the inner circle. Field restriction.
- **Always**: max 5 fielders on leg side, max 2 fielders behind the wicket on leg side.

### BaPP timing — TAKE IT IN 13-17 WINDOW

**Default BaPP timing: overs 13-17** (typical stack 13-14-15, 14-15-16, or 15-16-17).

Reason: opposition takes BoPP in overs 6-10, then their captain holds strike bowlers for overs 11-12 to finish their quotas. The middle window (overs 13-17) is when 5th and 6th bowlers (part-timers) come in. That's when BaPP catches the weakest links. Overs 18-20 sees strike bowlers return for the death.

- **Never take BaPP in overs 1-10** — opposition is taking BoPP, your restriction overlaps theirs with no benefit.
- **Avoid BaPP in overs 18-20** — their strike bowlers are back for the death; field restriction helps their wicket-taking, not your scoring.

### BoPP timing — AVOID THEIR HITTERS

**BoPP gives the bowling team field restrictions that PROTECT a weaker bowler.**

- If their hitter bats top-order (#1-3), BoPP later (overs 11-15) when anchors are in.
- If their hitter bats lower order (#7-8), BoPP early (overs 6-10) before they come in.
- If they have multiple hitters, BoPP whenever there's a NON-hitter at the crease.
- **Use weaker bowlers in BoPP**, save strike bowlers for non-PP overs against their best batter.

### Other PP rules

- **Each PP over must be a DIFFERENT bowler**. A bowler cannot bowl two PP overs (batting or bowling combined).
- **Mandatory**: all 6 PP overs must be taken. If overs left = PP overs left, every remaining over becomes a PP.

## Workflow

Follow these phases. Track progress with the todo list tool.

### Phase 0 (MANDATORY): Pre-flight checklist

Before asking the user a single question or building any plan, run through this checklist. Most "asks" are already answered in saved files — do not re-ask.

**Step 0.0: Read the cricket data directory FIRST**:
```
~/Dev/cricket/
├── team/roster.md              # canonical player profiles
├── team/trend.md               # recent results, form trend
├── opponents/<team-name>.md    # threat analysis (read for the opposition)
├── grounds/<ground-name>.md    # ground stats + history (read for the venue)
├── scorecards/<year>/...       # raw scorecards if needed
└── plans/<year>/...            # prior plans for reference
```

If the opposition or ground file is missing, ASK the user once for the data and CREATE the file as part of building the plan (so it's available next time).

**Step 0.1: Cross-reference each player from the lineup against `team/roster.md`**. For each player, pull:
- Their preferred batting position
- Their bowling capacity (regular vs part-timer, max overs)
- Their fielding strengths and weaknesses
- Their profile designation (Infield / Outfield / Anywhere)
- Any "do not place at X" notes

**Step 0.2: Apply team-wide rules automatically** (from `team/roster.md` settings):
- First-over bowler (if specified)
- Distribution pattern (4-4-3-3-3-3 default, 4-4-4-4-2-2 with part-timers)
- BaPP timing (default 13-17)
- BoPP timing (default 6-10, weak bowlers protected)
- Standard field positions (team conventions)

**Step 0.3: Run the 3 external signal checks (mandatory)**:
- Weather check for the match date/time/location.
- Pitch type / ground category (BB / 360T / 360M).
- Time-of-day audit of ground stats.

**Step 0.4: ONLY THEN ask the user about**:
- Items that genuinely change match-to-match: confirmed XI, pre-match intel, any player updates / DNPs / new players not in saved roster, opposition tweaks not in saved opponent file.

**Anti-pattern**: do NOT ask "what's player X's preferred slot?" or "where should player Y field?" — these are saved. If a saved rule contradicts current match data, surface as an observation, not a question.

**Step 0.5: After the match, SAVE updates**:
- Scorecard to `~/Dev/cricket/scorecards/YYYY/MM-DD-vs-OPPONENT.md`.
- Captain's plan + team summary to `~/Dev/cricket/plans/YYYY/MM-DD-vs-OPPONENT.md`.
- Update `team/trend.md` with the result.
- Update player profiles in `team/roster.md` if new form data or new strengths/weaknesses were observed.
- Update `opponents/<team>.md` with new threats / form / lineup changes.
- Update `grounds/<ground>.md` with the new match data point.

### Phase 1: Read the ground (and time-of-day)

Pull from `grounds/<ground>.md`:
- Average first innings score, average second innings score (last 20 games)
- Highest/lowest totals
- Successful chases above 100 vs below 100
- Last 5 games at the ground (any team)
- Last 5 games for both teams at this ground

**CRITICAL: Filter ground data by start time.** Morning games and afternoon games at the same ground play very differently.

Classify the ground as one of:
- **High-scoring** (avg 1st innings ≥ 130)
- **Par** (avg 1st innings 100-129)
- **Low-scoring** (avg 1st innings < 100)

**In club cricket on low-scoring grounds, 80-85 is competitive and 100+ is winning.** Don't anchor on IPL/international par scores — and don't REFERENCE them in team messaging either. Speak the team's reality.

### Phase 2: Toss strategy

**Use ground+time-slot recent form as the strongest signal.** Tally last 5 games at the ground in the same time slot:

- Count: how many were won by the team batting first vs chasing?
- Count: how many toss winners chose to field vs bat?
- Average 1st innings vs 2nd innings score for that time slot

**Decision logic:**

| Signal | Lean |
|---|---|
| Same-slot 4 of 5 toss winners chose to field, 4 of 5 chases succeeded | **Bowl first** |
| Same-slot 1st innings avg ≥ 100, defending teams winning | **Bat first** |
| Bowling is your strength + opposition has a weak top order | **Bowl first** |
| Bowling is your strength + ground favors batting first | **Bat first** (post-up + use bowling) |
| Batting is your strength | **Bowl first** (chase a known total) |

The time-of-day data ALWAYS overrides long-term averages.

**Always include a "Plan B" if we lose the toss** and are forced into the opposite.

### Phase 3: Build the batting order

**Batting order rules**:

1. **Rotators open** (overs 1-6). New ball is hard to hit cleanly. Send strike-rotators who can score 25-30 in PP without taking risks.
2. **Hitters come in when the ball is older** (overs 7-15). This is when boundary balls travel.
3. **Captain — form-based slot**, BUT context matters. Long innings at low SR on tough pitches IS a contribution.
4. **Anchors at #5**. Most consistent player.
5. **Tail in the order they actually bat** based on recent scorecards.

**Hitter classification**:

Look at a batter's recent innings. Classify carefully:

- **Pure hitter / boundary-or-bust**: short innings, 1+ six per innings or out for 0-3, no consolidating innings of 20+ in last 5. **DO NOT bat at #3.** Either boundary in 4 balls or out cheaply.
- **Hitting all-rounder**: capable of long innings AND quick hitting. **#4 is ideal — comes in for batting PP.**
- **Consolidator**: recent SR 50-90, can build innings. Goes the distance. Usually slotted at #3.
- **Anchor**: low SR (<60), few boundaries, blocks an end.

**Slotting principle**:
- Pure hitters go at #5-6 — partner them with anchors so when they fail, you don't collapse
- Hitting all-rounders go at #4 — coincides with batting PP overs
- Consolidators at #3 — they handle the transition between PP and middle
- Anchors at #1-2 (rotator openers) and #6-7 (finishers)
- **Never put two pure hitters back-to-back.** Always sandwich a hitter between anchors or consolidators.

**The "Runs by Batting Position" table is one signal, NOT the only signal.** Player profiles in `team/roster.md` may include position-by-position breakdowns. Use as a guide for what role each player is best at, but don't lock players into rigid positions. Match situation, ground, opposition bowling, and current state at the crease all affect the right entry point.

**The match-situation override**: ALWAYS prioritize getting the right player to the crease at the right TIME, not the right SLOT. If openers are still in at over 10, send your finisher next regardless of pre-game order. If you've collapsed to 30/4 in PP, send your most reliable batter.

**Counting innings correctly (CRITICAL)**:
- **DNB (did not bat)** does NOT count as a 0. Skip it.
- **DNP (did not play)** does NOT count as a 0. Skip it.
- **Not out (X*)** is a real innings — count it.
- **Retired hurt** counts as the score they had.

When auditing recent form, use the **last 5 actual innings** (excluding DNB and DNP), not the last 5 games.

**Read form in CONTEXT, not just raw runs.** A score like 6(26) on a tough pitch chasing 56 is a survival innings — exactly what's needed when the goal is to bat 20 overs. That player did the right thing. Don't demote them.

**Pure batsmen always go in the top 6, regardless of recent form.** The fair-chance rule trumps form.

### Target-setting rule (KEY — Asymmetric batting vs bowling targets)

If the team's bowling is their strength and batting is the weakness, the two targets must reflect that asymmetry, not mirror each other.

**Batting target (when batting first)**:
- Anchored to **ground first-innings average + 5 to +10 runs** (slightly above average — aim to be competitive PLUS a small cushion).
- Don't lower for fear of overshooting (leads to under-batting).
- Don't aspire to 25-30 above average (leads to collapses).

**Bowling target (when bowling first)**:
- Anchored **10-15 runs BELOW ground first-innings average** when bowling is the team's strength.
- For weak opposition, aim at the lower end.
- For strong opposition, aim at the higher end.

**Asymmetry stays preserved**: ~15-25 run gap between bat target (avg + 5/10) and bowl target (avg - 10/15).

### Second innings averages are biased LOW — apply a buffer

When the chasing team reaches the target, the match ends. They often score only 1-2 runs beyond the target rather than batting the full 20 overs. So "average second innings score" systematically underestimates what teams can actually score.

**Adjustment**: when using second innings average as a reference (ground tendency, chase difficulty), apply a **10-15% upward buffer**.

Example: if a ground shows second innings avg 66, the buffered estimate is ~73-76. That's much closer to what the ground actually allows.

**For target anchoring, always use the FIRST innings average** (no buffer needed — it's already unbiased). Use the buffered second innings only for chase-feasibility framing.

**Pacing checkpoints (40/60 split rule)**:
- 10-over batting check: ~40% of total target with 2 wickets max.
- 10-over bowling check: ~40% of bowling-restrict target with 2-3 wickets.
- **NEVER set the same 10-over checkpoint for both** — that ignores the bowling edge.

**Round all numbers to 5-run marks** in team messaging (35, 40, 45, 50, etc.).

**Always tell the team BOTH targets** (batting total AND 10-over batting check; bowling total AND 10-over bowling check).

### LOW-TARGET CHASE RULES (chase < 80)

When chasing a sub-80 total, the entire batting plan changes. The only way to lose is to lose 10 wickets. **The chase is not a run-rate problem; it's a wicket-preservation problem.**

**THE GOAL IS TO BAT 20 OVERS.** Period.

- **Required RPO is irrelevant** when it's < 5. At 2.85 RPO, extras + singles get you home.
- **Don't try to hit boundaries.** Boundaries are optional. Survival is mandatory.
- **Leave wide deliveries.** Block straight ones. Take any single offered.
- **Don't take risks for the sake of "scoring rate"**. The required rate is already met by occupying the crease.
- **Take BaPP early (overs 7-9)** if 3+ wickets have fallen in PP. Get the field up to support survival.

**Captain's pre-match brief in low chases or tough-pitch matches**: explicitly tell the team "we need to bat 20 overs. Even if we score 50, we still have a chance."

### Phase 4: Build the bowling rotation

**Audit first**: who has actually bowled in last 5 games? Career stats are stale. **Drop any "bowler" who has not bowled in 5+ recent games.**

**Sequencing rules (HARD constraints)**:

1. **No bowler bowls consecutive overs.** A bowler can bowl over N and N+2, but not N and N+1.
2. **Each BoPP must be a different bowler.**
3. **Each BaPP must also be a different bowler.**
4. **PP restriction across both PP types**: a bowler can bowl at most ONE PP over total in an innings.

**Strategic sequencing**:

5. **Bowlers prefer 2-over spells with one over gap** (preference, NOT a hard rule).
6. **Bowler preferences matter** — note them in `team/roster.md`.
7. **Use weaker bowlers in BoPP**, save stronger bowlers for late phase or matchup overs.
8. **BaPP defense plan**: after over 10, ideally have 4+ bowlers with at least 1 over left. NEVER lock all your bowlers' final overs into rigid slots.
9. **Match-up first, then form**: bring the best bowler in regular field when the opposition's best batter is at the crease.
10. **6th-bowler problem**: if only 5 confirmed bowlers cover 19-20 overs, you still need a 6th bowler for at least 1 over.
11. **No bowler may have more than 2 overs remaining after over 12 (HARD constraint).** By the end of over 12, every bowler must have bowled at least 2 of their 4 overs. Holding a 4-over bowler with 3-4 overs banked for the death does not work — it forces too many overs from one bowler late and the line/rhythm suffers. Front-load so that after over 12 the most any single bowler can still have is 2 overs, then spread the final 8 overs (13-20) so no one carries 3+. Stricter companion to rule 8.

**Core rotation principles (club / tennis-ball cricket)**:

A. **Give the very first over to a WEAKER bowler, not the best one.** Batsmen rarely attack from ball 1 — they're settling. A weaker bowler in over 1 will give up fewer runs than they would later because nobody is swinging yet. Save your best wicket-takers for overs 4-8 when the batsmen are looking for boundaries and the matchup actually matters. This applies in tennis-ball / club cricket where the new ball doesn't swing meaningfully. It does NOT apply to leather-ball cricket.

B. **Spinners need the ball to soften.** Profile-designated spinners are generally not effective with the brand-new ball — bounce is too high, ball grips less, batsmen pick line easily. Bring spinners in from over 4-5 onward. Don't waste a spinner's 4 overs in the new-ball phase.

C. **Some bowlers prefer the old ball.** Even non-spinners (slower mediums, cutters) may prefer bowling after the ball has scuffed. Honor stated preferences — a bowler in their preferred phase performs better than one forced into an uncomfortable spot.

D. **First-over bowler ≠ established pattern unless re-confirmed for current XI.** If the usual first-over bowler is absent for this match, do NOT default to "the most established bowler in this XI". Re-apply principle A (weaker first) to whoever is actually playing.

**BaPP defense at 17-20 (key rule)**:
- **4 different bowlers in the last 4 overs (17-20), at least 3 of them PP-eligible (non-BoPP).**
- The cleanest way: 3 BoPP bowlers + 3 non-BoPP. The 3 non-BoPP go in 17-20, plus 1 of the BoPP'd bowlers takes the 4th late slot.
- Schedule each BoPP bowler's remaining overs in the non-PP window (overs 11-16), so they're done before BaPP starts.

**Wicket-cluster trigger (KEY)**: If 3+ wickets fall within 6 overs, the original plan is dead — change immediately. Push best bowler in for an extra over. Tighten the field. Take BoPP if not yet taken.

### Phase 5: Field settings

Team-specific field conventions are in `team/roster.md`. Standard club field by phase:

#### Powerplay (only 2 outside circle)
- 1 slip (gully optional) for first 2 overs
- Mid-off, mid-on **inside** circle
- Square leg + point as boundary riders (these are your 2 outside)
- WK up to stumps for any spinner / slower bowler

#### Middle (max 4 outside circle)
- Sweeper cover, deep midwicket, long-on, long-off — typical 4 out
- 2 close catchers when spin/slow is bowling
- Cut singles to top scorers (extra fielder on their preferred side)

#### Death (max 4 outside circle)
- Both squares back (deep square leg, deep point), long-off, long-on
- One catcher only if there's a new batsman
- WK back; deep third for top edges

#### Ground-type field adjustments
- **BB (Baseball ground, short offside)**: **No deep cover or deep extra cover needed** — the short offside boundary is protected by ring fielders. Standard BB deep set: long-on, long-off, deep mid-wicket (or deep square leg). Often 3 outside rather than 4.
- **360M (Matting)**: Pack offside ring for cutters. Deep square leg + deep point are key PP outfielders.
- **360T (Turf)**: Larger boundaries. All deep positions matter.

#### Catching specialists
- WK should be the team's best keeper (and a captain ideally, for game reading)
- Slip: best slip catcher
- Point: best ground fielder (most catches)
- Long-off / long-on: best high-ball fielder
- Always note any chronic dropper and hide them at a low-traffic position

### Phase 6: Opposition matchups

**Use last 5 games of the opposition**, not historical H2H or career stats.

#### Step 1: Map their likely batting order from `opponents/<team>.md`

For each player:
- How many of the last games did they play?
- What positions have they batted at?
- What's their typical entry point?

Build a **predicted batting order**. Identify which players are likely to open, bat #3-4, bat #5-6 (often their captain/anchor), or bat lower order (often their hitters).

Use this to **predict when each opposition batter will come in**.

#### Step 2: Map their PP timing patterns

Look at the opposition's last 5 scorecards. When did they take BoPP and BaPP?

#### Step 3: Classify their batters

- For each top opposition batsman in their **last 5 games**: note boundary count (4s + 6s), batting position, typical SR.
- Classify each as: **anchor** (SR < 80), **rotator** (SR 80-110), or **hitter** (SR > 110 OR multiple sixes recently).

#### Step 4: Bowler-vs-batter matchup planning (KEY RULE)

**Always bring your best bowler when their best batter is at the crease — in a regular-field over.**

- Identify their best batter (highest avg + boundary frequency in recent games).
- Identify the over when they likely come in.
- **Plan your best bowler's overs to coincide with that entry window — but in a NON-PP over with regular field.**

**Why NOT in BoPP**: Field restriction (only 2 outside) helps the batter. Use regular field (max 4 outside) so your best bowler has 4 deep fielders to support him.

**For each hitter in their lineup, plan a deeper field setting before they come in.** For anchors, do the opposite: stack the ring. Strangle them on dot balls.

For each top opposition bowler, note economy and classify as:
- **See off** (eco < 4.0): rotate strike. Don't gift wickets. Attack the other end.
- **Attack** (eco > 4.5): get the in-form hitter on strike during their overs.

## Output Format

Always produce the plan in this exact order:

1. **Match header** — teams, date, ground, format
2. **Ground read** — what the data says, target totals
3. **Toss strategy** — what we want, plus Plan B if we lose
4. **Batting order** — table with role and rationale
5. **Bowling plan (Plan A)** — phase-by-phase with bowlers and overs
6. **Field settings** — by phase
7. **Opposition matchups** — table of their threats vs our counter
8. **First 10 overs goal** — explicit batting AND bowling targets
9. **Game plan by scenario** — A: bat first / B: chase / C: defending low / D: chasing big
10. **Plan B — Internal backup** — see "Plan B" section below. **For the captain only, never share with the team.**
11. **Three things that win this match** — concrete priorities
12. **Captain's summary** — full detail for the captain to save and reference on match day.
13. **Team summary (WhatsApp)** — high-level for the team chat. Does NOT reveal individual quotas or batting positions.

## Plan B — Internal backup (for the captain only)

Always produce a Plan B section internally, but NEVER include it in the team summary.

Include these standard triggers and responses:

### Bowling triggers
- **Opening bowler goes for 8+ runs in first over**: pull after over 1, bring in another bowler.
- **Both opening bowlers struggle**: rotate to economic bowlers in PP, save wicket-takers for BPP.
- **Opposition top order is still set at over 9**: bring back best wicket-taker.
- **Opposition is hitting at over 12** (projected total > target): defensive shift to most economic bowlers in BPP3.

### Batting triggers
- **If 2 wickets fall in PP**: shift batting PP earlier to get hitters in with field up.
- **If 5 wickets fall by over 12**: save batting PP for overs 17-19 with set anchor at the crease.
- **If chasing and required rate climbs above 8**: take next BPP immediately.
- **If batting first and we're 80+ at over 15**: take BPP overs 16-17-18 for 50+ in last 5.

### Field triggers
- **If a fielder drops 2 catches**: move them to a position where they don't get the ball (e.g. deep fine leg).
- **If extras count climbs (10+ wides by over 10)**: bowling-team meeting at next break.
- **If their hitter is tonking us**: deeper field on his preferred boundary, give him a single, attack the other batter.

## Two summaries — captain's vs team's

Always produce TWO summaries at the end of the plan.

**Team summary regen rule**: once the user has confirmed they sent the team summary to WhatsApp, **DO NOT regenerate it on subsequent corrections** unless the change is critical (player drops out, toss strategy completely flips, match called off, or explicit ask). Internal/captain's-side changes should only update the captain's summary.

### 1. Captain's summary (for the captain to save and reference)

This is for **the captain only**. Full detail. Includes:
- Toss strategy + Plan B if we lose
- **Full batting lineup, listed line by line (one player per line, all 11 named).** Not a paragraph. Vertical list with position, player, role notes.
- **Full bowling rotation, listed line by line (one over per line, all 20 overs).** Each line: over number, bowler name, BoPP/BaPP/regular marker.
- **Full fielding positions, listed line by line (one position per line, all 11 slots named).** Each line: position, player, brief reason.
- Individual quotas (who bowls 4, who bowls 3)
- BoPP and BaPP defense plan
- Day-of contingencies (Plan B triggers)
- Opposition matchups

### 2. Team summary (for the team WhatsApp chat)

This is what gets shared with the team. **Does NOT include**:
- **Individual bowling quotas** — don't tell someone they're only bowling 3 overs ahead of time.
- **Specific batting positions for #6-11** — don't tell anyone outside top 5 their fixed position.
- **Day-of-performance backups** — no "if X struggles" language.
- Form analysis or recent-game caveats.
- **"Save best bowlers for later" phrasing** — players bowling early might feel undervalued. Frame as "X and Y open, then we go by game state".

**WHAT GOES in the team summary** (always include all five of the items in bold below):
- Conditions (weather, pitch type)
- Opposition profile (general — "they have weak batting", "their key bowlers are X and Y")
- **Toss contingency**: what we want if we win + adjustments if we lose
- **Top 5 batting order (REQUIRED)** — name positions 1 through 5. For the rest, say "Then [list of names] in some order based on game state". Top-5 is the firm commitment; #6-11 is fluid.
- **Opening bowler AND first-change bowler (REQUIRED)** — explicitly name the over-1 bowler ("opens") and the over-2 bowler ("first change"). Then "then X, Y, Z come in based on game state". Do NOT reveal individual quotas. Do NOT use "save best for later" phrasing — frame as "A opens, B first change, then others come in".
- **Fielding positions (REQUIRED)** — assign each player to a position. Be specific: "A goes to slip, B at point, C at long-on". List ALL 11 (1 bowler + 1 WK + 9 fielders).
- First 10 overs goals (batting + bowling targets)
- Key matchups (their star batsmen, their star bowlers, our counters)
- Catch reminder if the team has been dropping catches recently
- Simple rules for the day (3-5 ground/condition-tied principles)
- Arrival time

**Lead the team summary with the ARRIVAL time, not the match start time.** If start is 8:30 AM, the opening line should read "Be at the ground by 8 AM. Match starts at 8:30." People skim — if start time comes first, they'll show up at start time and miss warm up. Close the team summary with a time reinforcement like "See you at 8 AM" to anchor it one more time.

**Always include a "ping the captain directly" call-out in EVERY team summary** (placed just before the final closing line). Ask anyone with concerns about their role, batting slot, bowling spot, or fielding position to reach out **directly and now**, before the match day. Be polite and warm, not rude. Example: "If anyone has concerns or thoughts on your role, please ping me directly now so we can sort it out before the match. Much better to hear it tonight than on the field."

**Cap opposition "good bowler" call-outs at the top 2-3 in the TEAM summary.** Even if the opposition has 4-5 tight bowlers, only name the **2 or 3 toughest** in the team summary. Naming all of them makes the batters feel there is no way to score and they freeze. The full bowling tier list (all tight bowlers + econ figures) belongs in the captain's summary and the opponent file only. If every bowler is tight with no weak link, don't list them all — give a positive plan instead ("their attack is disciplined, so runs come from rotating strike and converting the loose ball, not from taking anyone on"). Always give the batters a way to play, not a wall of names.

### Fielding position assignment rules

Use **per-match rates** (catches/match, run-outs/match), profile designations, AND any player-specific preferences from `team/roster.md`:

- **Use rates not absolute counts.** A player with 100 catches in 250 matches is not better than a player with 50 catches in 100 matches.
- **Wicket-keeper**: the player listed as keeper.
- **Slip / point** (close catching): highest catches/match rate.
- **Long-on / deep midwicket** (boundary): best high-ball outfielder, "Anywhere Fielder" by profile.
- **Sweeper cover / deep cover**: athletic boundary rider.
- **Infield-only players**: respect profile designation. **NEVER put profile-designated "Infield Fielder" players in deep positions.**
- **Hide weak fielders**: players with low fielding involvement per match go to low-traffic positions.
- **Bowlers**: usually field at mid-on/mid-off near their delivery point.

**Player preferences override pure stats.** If a player asks for a specific position they're comfortable with, slot them there if it doesn't break a hard rule.

**Core fielding principles** (apply across all matches):

1. **Best fielder goes to the highest-volume deep catch position.** On a short-offside ground (e.g. BB / Baseball ground), that is usually **deep mid-wicket** — leg-side boundaries are longer and high catches from pulls/hooks land there. On a full ground, it is usually long-on or long-off. Identify the highest-volume deep catch spot for the ground and put the best high-catch outfielder there, not at an arbitrary deep spot.

2. **Slips suit fielders who don't / can't run much** but have **strong reflexes / soft hands**. A slow runner is not a defect at slip — it is a fit. Pair the role with reflexes, not athleticism.

3. **Some good infield catchers don't catch in the outfield at all** — keep them inside the ring. A player who catches well at slip / point / short cover but freezes or declines outfield catches should be kept inside the ring. Don't force them deep just because they're a "good catcher" — that's a category mismatch.

   Distinct from this is a **conservative outfielder**: a player who DOES field in the deep / ring outfield but only attempts catches when they are close and the take is clean. They are not infield-only — they are a valid backup outfielder, just a conservative catcher. Place them at lower-catch-volume outfield spots (e.g. Long-off on a short-offside ground; Mid-off or Mid-on as ring outfielder #4 or #5) rather than high-volume catch positions. Use them as the 5th outfielder in place of a strictly infield-only player when the roster allows — that frees the infield-preferring player to stay at a true infield spot (Slip, Point, Square Leg, Short Cover).

4. **Always explicitly designate the first-over bowler in the field plan.** The fielding lineup must add to 11: **1 bowler + 1 WK + 9 fielders = 11**. If you list 11 fielding positions without naming the bowler, you have miscounted. Name the bowler first, then the 10 non-bowling positions. When the first-over bowler is bowling, they occupy the bowling crease (not a fielding position); when they're not bowling later, they default to whichever non-bowling field position they were assigned.

5. **Strong outfielders also belong at Mid-Off or Mid-On — not just in the deep.** Mid-off and mid-on are high-traffic ring positions where the bowler needs safe hands and a strong arm; a good outfielder there saves more runs and takes more drives-on-the-up catches than at the deep boundary. Don't reflexively pin every good outfielder to long-on / long-off — use ring placements for them when the depth is otherwise covered.

6. **Weaker fielders / unknown fielders go to Square Leg or Short Cover** (sometimes called Short Mid-off, same idea). These positions get fewer high-pressure catches and less ground-coverage volume — the cleanest places to hide a fielder you don't trust with hard chances. **If you have not seen a player field in the outfield, treat them as "not outfield" until proven** — slot them at Square Leg or Short Cover rather than guessing.

7. **Build a 5-deep outfield depth chart for every XI and assign positions in rank order.** Every team plan needs FIVE ranked outfielders, not just three:
   - **#1 (best fielder)** → highest-volume deep catch position (often Deep Mid-Wicket on short-offside grounds; otherwise Long-on or Long-off on full grounds).
   - **#2** → other primary deep position.
   - **#3** → third deep position (when 3 outside is warranted).
   - **#4 (backup outfielder)** → **Mid-on** at the start of the game. High-traffic ring spot.
   - **#5 (backup outfielder)** → **Mid-off** at the start of the game. High-traffic ring spot.
   
   Mid-on and Mid-off are NOT casual ring slots — they are reserved for the 4th and 5th best outfielders specifically. If you don't have 5 outfielders in the XI, name the closest available player as the 5th and live with the risk. Position the first-over bowler's "when not bowling" base position carefully so a critical spot is not vacated in over 1 (Square Leg in particular must always be covered in over 1).

8. **Fielding-position listing order (apply in BOTH captain's summary and team summary):** always list positions in this exact order:
   WK, Slip, Square Leg, Point, Cover, Mid Off, Mid On, Long Off, Long On, Deep Mid Wicket.
   
   This is the standard 10 fielding positions for a typical XI on a short-offside ground (the bowler is the 11th player but is NOT listed — see rule 9). If the plan uses other positions (e.g. Short Mid-off, Backward Short Leg, Extra Cover), slot them in geographically — Short Mid-off between Cover and Mid Off, Backward Short Leg between Slip and Square Leg, Extra Cover between Cover and Mid Off. Never list positions in random order — readers scan top-to-bottom and rely on the consistent flow (close → ring → ring outfielder → deep).

9. **Do NOT list the bowler in the fielding-positions section** of either summary. The first-over bowler is named in the bowling section ("X opens at over 1"), and including them again in fielding is redundant. The fielding-positions section is 10 entries only (WK + 9 fielders); the 11th player is implicitly the bowler at the crease.

11. **Keep both summaries tight — list names, not justifications.** Do not include per-player reasoning, career stats, stated-preference notes, or tactical "why" annotations in the line-by-line lists. The summaries are reference cards, not white papers.
   
   **Do NOT include the outfield depth chart as its own section in the captain's summary.** Build the depth chart internally (rule 7) to figure out who goes to which deep / ring outfielder spot, then surface only the resulting field plan. The depth chart itself is reconstructable from the field plan, so it adds noise to the summary.

12. **Player-tag naming convention.** Tags like (S), [S], [M], [VC], (C) appear after a player's name to denote role / status. Do NOT duplicate the tag meaning in the name itself:
   - **(S) = Secondary**. Write "Name (S)", not "Name Sec (S)" or "Name Secondary (S)".
   - **(C) = Captain**, **(VC) = Vice Captain**, **[M] = Manager**, **[WK] = Wicket Keeper** — same logic, the tag is enough.
   - In the team WhatsApp summary, drop the tags entirely (use first name only). Tags appear in captain's summary and roster files only.

## Pre-match WhatsApp announcement (Playing XI message)

Many captains send a pre-match Playing XI announcement to the team WhatsApp group a day or two before the match. This is a separate message from the team summary. The format below is the standard convention used by club captains; preserve labels and ordering exactly.

**Standard structure**:

```
This is the playing XI for the upcoming match:
├ <Captain Full Name> [C & WK]   (or [C] if not the keeper)
├ @<wa-id-1>
├ @<wa-id-2> [S]                  (if secondary)
├ @<wa-id-3>
├ ... (one line per player, tree prefix `├ ` followed by name or @-mention)

Kit: @<wa-id-x>
Field setup: @<wa-id-a>, @<wa-id-b> and @<wa-id-c>
Scoring: @<wa-id-d> and @<wa-id-e>
Practice: @<wa-id-f>

Time to reach the ground: <match-start minus 30 min, e.g. 8:00am>
Match details: <Team> v <Opponent> at <Ground>, <City> on <MM/DD/YYYY> <Weekday> <HH:MMam/pm>
Live Stream: <captain's live-stream URL if applicable>
Address: <ground address>
Map: <ground map URL>

Special Instructions
<ground-specific text; omit the whole block if none>

Ground Preparation Instructions
<ground-specific text; omit the whole block if none>

Parking Instructions
<ground-specific text>

Restroom Instructions
<ground-specific text>
```

**Conventions**:
- Captain is always the first entry in the playing XI list.
- "Time to reach the ground" = match start time minus 30 minutes (warm-up window).
- Date format: `MM/DD/YYYY` followed by weekday and `HH:MMam/pm`. Use `v`, not "vs".
- Tree prefix: `├ ` (Unicode U+251C + space).
- Ground-specific data (Address, Map, Parking, Restroom, Special Instructions, Ground Preparation Instructions) is stored in `~/Dev/cricket/grounds/<ground-slug>.md` under a "Pre-match WhatsApp boilerplate" section. Pull verbatim into the message.

**Role assignments** (standard set; 1 + 3 + 2 + 1 = 7 player references):
- **Kit**: 1 player.
- **Field setup**: 3 players, joined as `@a, @b and @c`.
- **Scoring**: 2 players, joined as `@d and @e`.
- **Practice**: 1 player.

Captain does not take any of these roles (they have captain duty). Any player not assigned a role is just listed in the playing XI without further mention; that's fine.

**What the captain provides per match** (ask once for anything missing):
- Opponent team name.
- Match date, weekday, start time.
- Ground (so the right boilerplate file loads).
- WhatsApp IDs for the 10 non-captain players, with [S] tag noted where applicable.
- Role assignments (Kit, Field setup x3, Scoring x2, Practice).
   
   In batting orders, list only "Position N, Name" (or "N. Name [Tag]"). Do not append "career home", "preferred slot", "stated preference", "anchor", "N career runs", etc.
   
   In bowling rotations, list only "Over N. Bowler" plus BoPP/BaPP markers when applicable. Do not append "(first change)", "(weaker bowler)", "(spinner enters)", "(spell start)", or "(2nd of spell)". The pattern is visible from the rotation itself.
   
   In field plans, list only "Position: Name". Do not append "(his strength)", "(doesn't run much)", "(infield catcher)".
   
   In conditions, keep to weather + relevant ground type cues. Skip pitch-detail like "Hard tennis ball, no swing" unless the pitch is unusual for the league.
   
   In team summaries specifically, also skip:
   - Over-lecturing on arrival time. "Be at the ground by X" suffices; do not add "do not show up at start time ready to play, that is too late".
   - Over-detailed conditions ("ball comes on straight" etc.) — the team knows the equipment.
   - Per-player career stat call-outs.
   
   When the captain or a teammate wants the "why" for a slot, they can ask. The summaries default to brevity.

10. **Always include a "stand inside the boundary" reminder in the team summary.** Outfielders / deep fielders should stand about **20 steps in from the boundary rope**, not on the rope itself. Word the reminder warmly. **Use reasoning that supports the instruction** — "most outfield catches drop short of the rope, so standing inside puts you in the actual catching zone". DO NOT use the phrase "easier to come forward than to backpedal" — that argument actually supports standing AT the rope (always coming forward), which contradicts the instruction. Place this near the catch-reminder line in the team summary.

### Tone rules (apply to both summaries)

- Plain text. No headings. No markdown bold/italics.
- Short paragraphs (1-3 sentences). Bullet lists for items.
- Direct, warm, professional. No hype, no AI tells.
- **NO em dash**. Use periods, commas, parentheses, hyphens.
- **NO ellipsis**. Finish the thought.
- Refer to teammates by first name only.
- Refer to the opposition by team name.
- End with a simple closing — nothing more.
- **Minimize superlatives**. Don't say "X is our best catcher" repeatedly. Use one or two sparingly for things that genuinely stand out.

### Team summary tone (additional)

- **Light emojis are welcome in the team summary** (not the captain's summary). Use sparingly to highlight sections: 🏏 (cricket), 🎯 (target/attack), 🛡️ (defend/anchor), 📝 (rules), 🤝 (teamwork), 🔥 (close out), ⏰ (timing), 🥊 (matchups), 😬 / 😄 (light expressions). Cap at ~8 emojis total.
- **Light humor is welcome** in the team summary. Gentle self-deprecating notes, friendly references to past matches without dwelling, mild commentary on opposition. NEVER make jokes at specific teammates' expense.
- **BaPP/BoPP in team summary**: give the **window only** (e.g. "between overs 13 to 17"), do NOT spell out specific stacks or explain WHY we take BoPP at certain times. The team just needs to know the window. Always pair BaPP mention with the reminder that PP does NOT mean swing-for-the-fences.
- **Pacing language**: skip the math ("40/60 split"). The 10-over checkpoint number is enough plus a "pace yourselves" line.
- **Catch reminder**: include if the team has been dropping catches. Phrase as a forward-looking ask, not a callout of past drops.
- **Anti-pattern**: do NOT say "one position per player. Bowlers shift around when they are bowling." Self-evident.
- **Anti-pattern**: do NOT explain WHY we set particular field positions or WHY we pick certain bowlers for certain overs.
- **Captain's summary stays neutral/clinical**. No emojis.
- **DO NOT reference IPL, international cricket, leather-ball cricket, or any premier league** in the team summary if the team plays tennis-ball or club cricket.

## Anti-patterns (avoid these)

- **Don't anchor on IPL par scores.** 80-85 is good in club cricket; 100+ is winning.
- **Don't ignore Plan B.** Always cover the lose-toss scenario.
- **Don't bury the lead.** The toss decision and the opening pair are the two things the team most needs to see first.
- **Don't load the message with stats.** The team summary is operational.
- **Don't mention skill names, AI, or analysis tools** in the team summary. The captain wrote it.
- **Don't write speeches.** End with a simple closing.
- **Don't weight historical stats over recent form.** A player with 1500 career runs but 0+0+0+0+9 in last 5 innings is OUT of form (with context).
- **Don't ignore the time slot.** Ground stats from afternoon games at the same venue do not predict morning play.
- **Don't mix old and new opposition lineups.** Players join, leave, get suspended. Use last 5 games.
- **Don't put hitters at the top of the order with the new ball.**
- **Don't put hitters at #4 expecting new-ball protection.** 2nd wicket typically falls in new-ball overs.
- **Don't plan a bowler based on career stats alone.** Audit whether they have actually bowled in the last 5 games.
- **Don't forget the 6th-bowler rule.**
- **Don't confuse "did not play" with "no longer bowls".**
- **Don't ignore the fair-chance principle.** Specialist batsmen need a top-6 batting slot. Specialist bowlers need overs.
- **Don't assume the lineup matches the recent scorecards.** Players come back after travel, injury, or skipping a game.
- **Don't classify a hitter as a consolidator.**
- **Don't apply ICC T20 rules to club leagues if the league differs.** Confirm whether automatic PP exists in overs 1-6.
- **Don't put your best bowler's 4 overs all early.**
- **Don't use your best bowler in BoPP.**
- **Don't lock in 4 consecutive overs from one bowler.**
- **Don't ignore bowler preferences.**
- **Don't lock all final overs into rigid slots.**
- **Don't introduce a 7th bowler who hasn't bowled recently.**
- **Don't put two hitters back-to-back.**
- **Don't skip the weather check.**
- **Don't ignore pitch type.**
- **Don't index too much on recent form for batsmen.** Club umpiring is variable; a few low scores often reflects noise.
- **Don't give a pure bowler only 1-2 overs.**
- **Don't put words in the captain's mouth in the team summary.**
- **Don't soften match analyses with "variance" or "bad luck" excuses** when the team gave up wickets cheaply.
- **Don't include day-of-performance backup plans in the team summary.**
- **Always include the toss contingency in the team summary.**
- **Don't reveal individual bowling quotas in the team summary.**
- **Don't reveal individual batting positions for #6-11 in the team summary.**
- **Always produce TWO summaries**: one for the captain (full detail, kept private), one for the team (high-level, share-friendly).
- **Don't count DNB or DNP as 0 in form analysis.**
- **Read form in CONTEXT, not just raw runs.** A long innings at low SR on a tough pitch is a contribution, not poor form.
- **Don't concentrate bowling overs in the strongest bowlers if it leaves others marginalized.**
- **Don't match bowling target to batting target.** Apply the asymmetry: bowl to restrict 10-15 below average if bowling is your strength.
- **Don't lower batting target out of fear of overshooting.** The risk of under-batting is just as real.
