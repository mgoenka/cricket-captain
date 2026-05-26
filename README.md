# Cricket Captain — Cursor Plugin

A T20 cricket match strategy assistant for club-level captains. Builds your toss strategy, batting order, bowling rotation, field plans, opposition matchups, and a WhatsApp-ready team summary — every week, in seconds.

Built for tennis-ball / club leagues like **CricBay** (San Francisco Bay Area), but the methodology applies to most amateur T20 leagues.

## What you get

- A **`cricket-strategy` skill** that activates when you ask Cursor to plan a match. It knows the standard CricBay rules (BaPP/BoPP timing, distribution patterns, field conventions for BB / 360T / 360M grounds, tennis-ball assumptions, etc.).
- **Templates** for your team roster, opposition profiles, ground profiles, and scorecards. Fill them in once; the skill reads them automatically every match.
- A **Python script** that generates a custom umpiring score sheet PDF with your team's roster pre-printed.

## Install

### Option A — Install from GitHub (recommended)

In Cursor:

1. Open Settings → Plugins → Install from URL
2. Paste: `https://github.com/mgoenka/cricket-captain`
3. Restart Cursor or reload the window.

### Option B — Install locally for testing

```bash
# Clone the plugin
git clone https://github.com/mgoenka/cricket-captain ~/.cursor/plugins/local/cricket-captain

# Or for development:
ln -s /path/to/cricket-captain ~/.cursor/plugins/local/cricket-captain
```

Then restart Cursor.

## Setup (one command)

Run the included installer:

```bash
~/.cursor/plugins/cricket-captain/install.sh
```

That will:
1. Create `~/Dev/cricket/` with subfolders for team, opponents, grounds, scorecards, and plans
2. Copy the templates into the right places (without overwriting anything you've already filled in)
3. Check for Python + PyMuPDF (used by the umpiring sheet generator)
4. Print next steps

Now just fill in the templates:

| File | What to put in it |
|---|---|
| `~/Dev/cricket/team/roster.md` | Your 11-player squad with batting + bowling + fielding profiles |
| `~/Dev/cricket/opponents/<team>.md` | One file per regular opponent (batting threats, bowling tiers, recent form) |
| `~/Dev/cricket/grounds/<ground>.md` | One file per ground (type, average scores, recent results) |
| `~/Dev/cricket/scorecards/<year>/...` | Past match scorecards (optional, but improves form analysis) |

**Pro tip**: don't write these from scratch. Paste content from your league's website (player pages, head-to-head pages) into a Cursor chat and ask the agent to summarize into the template format.

## Usage

### Before each match

In Cursor, just ask:

> Help me plan Saturday's match. Opposition: Valley Thunders. Ground: Glenmoor. Lineup: [11 names]. Pitch tip: tough pitch with low scores expected.

The skill will:
1. Read each player's profile from your roster
2. Read the opposition file (or ask if it doesn't exist and create it)
3. Read the ground file (or ask if missing)
4. Run a weather check
5. Apply all the team rules + CricBay defaults
6. Produce a full Captain's Summary + a WhatsApp-ready Team Summary
7. Save the plan to `~/Dev/cricket/plans/2026/MM-DD-vs-opponent.md`

### After each match

Either paste the scorecard and say "save this and update player form" — or ask the agent to fetch from your league site.

The agent will:
- Save the scorecard to `~/Dev/cricket/scorecards/`
- Update player form notes in `team/roster.md`
- Update the opponent profile if new threats emerged
- Update the ground profile with the new data point

### Generate a custom umpiring sheet (optional)

```bash
python3 ~/.cursor/plugins/cricket-captain/scripts/generate_umpiring_sheet.py \\
  --source /path/to/cricbay-Umpiring.pdf \\
  --output ~/Desktop/Umpiring-MyTeam.pdf \\
  --roster ~/Dev/cricket/team/umpiring-roster.txt \\
  --team-name "Alpha Lions"
```

Get the source umpiring PDF from CricBay (or your league). The script overlays a custom Playing XI section with your 20 most frequent players + 10 blank slots for substitutions.

Sample output:

![Sample umpiring sheet](docs/screenshots/umpiring-sheet-sample.png)

## Customization

### Team-wide rules

The skill reads team-wide settings from `~/Dev/cricket/team/roster.md`. Edit these in the file:

- **First-over bowler** (if your team has one)
- **Equipment** (tennis-ball / leather-ball)
- **BaPP/BoPP timing defaults**
- **Bowling distribution preferences** (4-4-3-3-3-3 default, 4-4-4-4-2-2 with part-timers)
- **Field position conventions** (which positions your team uses)

### Skill rules

Don't like a default? Tell the agent in-chat:

> Update the skill: our team prefers gully over short cover.

The agent will update `~/.cursor/plugins/cricket-captain/skills/cricket-strategy/SKILL.md` (or your local override at `~/.cursor/skills/cricket-strategy/SKILL.md` if you've forked it).

## Philosophy

This skill encodes a few opinionated principles from years of running a club team:

1. **Fair-chance principle**: pure batters get top-6 batting slots; bowlers get even over distribution. Nobody is marginalized for a roster decision.
2. **Form trumps stats, but context trumps form**: a long innings at low SR on a tough pitch is a contribution, not a failure.
3. **The team sees the WHAT, not the WHY**: the WhatsApp summary is operational — positions, targets, simple rules. The captain holds the strategic reasoning.
4. **Asymmetric targets**: if bowling is your strength, your bowling restrict target should be 10-15 runs below the ground average, not the same as your batting target.
5. **Plan for unknowns**: opposition won't share their lineup. Build flexibility into the bowling plan.

## Contributing

Found a rule that's wrong, missing, or works differently in your league? Open an issue or PR at `github.com/mgoenka/cricket-captain`.

## License

MIT
