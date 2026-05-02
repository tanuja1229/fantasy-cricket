# Fantasy Cricket Game 🏏

## About
A Fantasy Cricket desktop application built with Python, 
Tkinter and SQLite. This is the final project for the 
Internshala Programming with Python course.

## Features
- ✅ Create and manage fantasy cricket teams
- ✅ Select players by category (BAT, BOW, AR, WK)
- ✅ Points based player selection system
- ✅ Save and load teams from database
- ✅ Evaluate team score based on match performance
- ✅ Game rules validation (max players per category)

## How to Run
```bash
pip install tkinter
python database.py
python main.py
```

## Game Rules
### Batting
- 1 point for 2 runs scored
- 5 bonus points for half century
- 10 bonus points for century
- 2 points for strike rate 80-100
- 6 points for strike rate > 100

### Bowling
- 10 points per wicket
- 5 bonus points for 3 wickets
- 10 bonus points for 5 wickets
- Economy rate bonus points

### Fielding
- 10 points each for catch/stumping/run out

## Team Selection Rules
- Maximum 11 players
- Maximum 5 batsmen
- Maximum 4 bowlers
- Maximum 3 allrounders
- Maximum 1 wicket keeper
- Total points budget: 1000

## Tech Stack
- Python 3.11
- Tkinter (GUI)
- SQLite (Database)
- 3 Database tables: stats, match, teams

## Database Design
- **stats** — Player statistics and category
- **match** — Match performance data
- **teams** — Saved fantasy teams

## Author
K T Tanuja | Python Developer | Bangalore
github.com/tanuja1229