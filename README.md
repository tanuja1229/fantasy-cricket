# Fantasy Cricket Game 🏏

## About
A Fantasy Cricket desktop application built with Python,
Tkinter and SQLite. This is the final project for the
Internshala Programming in Python with AI course.

## Features
- ✅ Create and manage fantasy cricket teams
- ✅ Select players by category (BAT, BOW, AR, WK)
- ✅ Points based player selection system
- ✅ Save and load teams from database
- ✅ Evaluate team score based on match performance
- ✅ Game rules validation (max players per category)

## How to Run
> **Note:** `tkinter` and `sqlite3` come built-in with Python — no pip install needed!

```bash
# 1. Clone the repository
git clone https://github.com/shubhashreekt/fantasy-cricket.git
cd fantasy-cricket

# 2. Run the database setup
python database.py

# 3. Launch the app
python main.py
```

## Game Rules

### Batting
- 1 point for every 2 runs scored
- 5 bonus points for a half century
- 10 bonus points for a century
- 2 points for strike rate 80–100
- 6 points for strike rate > 100

### Bowling
- 10 points per wicket
- 5 bonus points for 3 wickets
- 10 bonus points for 5 wickets
- Economy rate bonus points

### Fielding
- 10 points each for catch / stumping / run out

## Team Selection Rules
- Maximum 11 players
- Maximum 5 batsmen
- Maximum 4 bowlers
- Maximum 3 allrounders
- Maximum 1 wicket keeper
- Total points budget: 1000

## Tech Stack
- Python 3.x
- Tkinter (GUI)
- SQLite (Database)
- 3 Database tables: stats, match, teams

## Database Design
- **stats** — Player statistics and category
- **match** — Match performance data per player
- **teams** — Saved fantasy teams

## Certificate
Built as part of the **Programming in Python with AI** certification by Internshala.
- Issued: April 2026 | Score: 71% | Cert No: `cip8ur2muf_`

## Author
**Shubha Shree K T** | Python Developer | Bengaluru
[github.com/shubhashreekt](https://github.com/shubhashreekt)
