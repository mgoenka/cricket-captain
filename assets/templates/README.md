# Templates

These files are the data scaffolding the `cricket-strategy` skill expects at `~/Dev/cricket/`.

Copy them to your data directory and fill in your team's actual values:

```bash
# Initial setup
mkdir -p ~/Dev/cricket/{team,opponents,grounds,scorecards/2026,plans/2026}

# Copy templates
cp team-roster-template.md ~/Dev/cricket/team/roster.md
cp opponent-template.md   ~/Dev/cricket/opponents/<team-name>.md
cp ground-template.md     ~/Dev/cricket/grounds/<ground-name>.md
cp scorecard-template.md  ~/Dev/cricket/scorecards/2026/MM-DD-vs-<opponent>.md
```

## File guide

- **`team-roster-template.md`** — your team's 11 players (and rotation/bench). The skill cross-references each player on the playing XI you give it. The richer this file, the better the plan.
- **`opponent-template.md`** — one file per regular opponent. Captures their batting threats, bowling tiers, recent form. The skill reads this to build opposition matchups.
- **`ground-template.md`** — one file per ground you play. Ground type, average scores, recent results, time-of-day notes.
- **`scorecard-template.md`** — one file per past match. Optional but useful for form analysis.

## Pro tip

Don't write these from scratch — paste content from your league's website (CricBay player profile pages, head-to-head pages, etc.) into a chat with the agent and ask it to summarize into the template format. The agent can do this for you in seconds.
