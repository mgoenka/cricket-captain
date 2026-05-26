#!/usr/bin/env bash
# Cricket Captain plugin — first-time setup script.
#
# Creates the data directory at ~/Dev/cricket/ and copies the templates so
# you can fill in your team's data and start using the cricket-strategy skill
# in Cursor immediately.
#
# Usage:
#   ./install.sh                       # use default location ~/Dev/cricket/
#   ./install.sh /custom/data/path     # use a custom data location
#
# Safe to run multiple times — it never overwrites existing files.

set -euo pipefail

DATA_DIR="${1:-$HOME/Dev/cricket}"
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$PLUGIN_DIR/assets/templates"

# Colors for output (skipped if not a TTY)
if [ -t 1 ]; then
  BOLD='\033[1m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  NC='\033[0m'
else
  BOLD='' GREEN='' YELLOW='' BLUE='' NC=''
fi

YEAR="$(date +%Y)"

echo ""
echo -e "${BOLD}Cricket Captain — Plugin Setup${NC}"
echo ""

# 1. Create directory structure
echo -e "${BLUE}1.${NC} Creating data directory at ${BOLD}$DATA_DIR${NC}..."
mkdir -p \
  "$DATA_DIR/team" \
  "$DATA_DIR/opponents" \
  "$DATA_DIR/grounds" \
  "$DATA_DIR/scorecards/$YEAR" \
  "$DATA_DIR/plans/$YEAR"
echo -e "   ${GREEN}✓${NC} Done."
echo ""

# 2. Copy templates (without overwriting)
copy_template() {
  local src="$1"
  local dst="$2"
  if [ -f "$dst" ]; then
    echo -e "   ${YELLOW}↷${NC} ${dst#$HOME/} already exists, skipping."
  else
    cp "$src" "$dst"
    echo -e "   ${GREEN}✓${NC} ${dst#$HOME/}"
  fi
}

echo -e "${BLUE}2.${NC} Copying templates (will skip files that already exist)..."
copy_template "$TEMPLATES_DIR/team-roster-template.md"  "$DATA_DIR/team/roster.md"
copy_template "$TEMPLATES_DIR/opponent-template.md"     "$DATA_DIR/opponents/example-opponent.md"
copy_template "$TEMPLATES_DIR/ground-template.md"       "$DATA_DIR/grounds/example-ground.md"
copy_template "$TEMPLATES_DIR/scorecard-template.md"    "$DATA_DIR/scorecards/$YEAR/example-scorecard.md"
echo ""

# 3. Check Python + dependencies for the umpiring sheet generator
echo -e "${BLUE}3.${NC} Checking dependencies for the umpiring sheet generator..."
if command -v python3 >/dev/null 2>&1; then
  echo -e "   ${GREEN}✓${NC} python3 found ($(python3 --version 2>&1))"
  if python3 -c "import fitz" 2>/dev/null; then
    echo -e "   ${GREEN}✓${NC} PyMuPDF (fitz) installed"
  else
    echo -e "   ${YELLOW}↷${NC} PyMuPDF not installed. Install with:"
    echo -e "      ${BOLD}pip3 install --user PyMuPDF${NC}"
    echo "      (Only needed for the umpiring sheet generator.)"
  fi
else
  echo -e "   ${YELLOW}↷${NC} python3 not found. The umpiring sheet generator won't work without it."
fi
echo ""

# 4. Print next steps
echo -e "${BOLD}Setup complete!${NC}"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo ""
echo -e "  ${BOLD}1.${NC} Fill in your team:"
echo -e "       Open ${BOLD}$DATA_DIR/team/roster.md${NC} in Cursor and replace the"
echo -e "       example player profiles with your actual 11-player squad."
echo ""
echo -e "  ${BOLD}2.${NC} Add opponent profiles:"
echo -e "       Rename ${BOLD}example-opponent.md${NC} to your opposition's name and fill in."
echo -e "       Repeat for each regular opponent."
echo ""
echo -e "  ${BOLD}3.${NC} Add ground profiles:"
echo -e "       Rename ${BOLD}example-ground.md${NC} to your ground's name and fill in."
echo ""
echo -e "  ${BOLD}4.${NC} (Optional) Pro tip:"
echo -e "       Paste content from your league's website (player pages, head-to-head)"
echo -e "       into a chat with Cursor and ask the agent to summarize into the"
echo -e "       template format. The agent will do it in seconds."
echo ""
echo -e "  ${BOLD}5.${NC} Plan your first match:"
echo -e "       In Cursor, ask: ${BOLD}\"Help me plan Saturday's match.\"${NC}"
echo -e "       Give it the opponent, ground, lineup, and any pitch intel."
echo ""
echo -e "Full docs: ${BOLD}$PLUGIN_DIR/README.md${NC}"
echo ""
