import sqlite3

def create_database():
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()

    # Create stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            player TEXT PRIMARY KEY,
            matches INTEGER,
            runs INTEGER,
            hundreds INTEGER,
            fifties INTEGER,
            value INTEGER,
            category TEXT
        )
    ''')

    # Create match table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match (
            player TEXT,
            match_name TEXT,
            scored INTEGER,
            faced INTEGER,
            fours INTEGER,
            sixes INTEGER,
            bowled INTEGER,
            maiden INTEGER,
            given INTEGER,
            wkts INTEGER,
            catches INTEGER,
            stumping INTEGER,
            runout INTEGER,
            PRIMARY KEY (player, match_name)
        )
    ''')

    # Create teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            name TEXT,
            players TEXT,
            value INTEGER
        )
    ''')

    # Player stats data
    players_data = [
        ('Kohli',        189, 8257, 28, 43, 120, 'BAT'),
        ('Yuvraj',       86,  3589, 10, 21, 100, 'BAT'),
        ('Rahane',       158, 5435, 11, 31, 100, 'BAT'),
        ('Dhawan',       25,  565,  2,  1,  85,  'AR'),
        ('Dhoni',        78,  2573, 3,  19, 75,  'BAT'),
        ('Axar',         67,  208,  0,  0,  100, 'BWL'),
        ('Pandya',       70,  77,   0,  0,  75,  'BWL'),
        ('Jadeja',       16,  1,    0,  0,  85,  'BWL'),
        ('Kedar',        111, 675,  0,  1,  90,  'BWL'),
        ('Ashwin',       136, 1914, 0,  10, 100, 'AR'),
        ('Umesh',        296, 9496, 10, 64, 110, 'WK'),
        ('Bumrah',       73,  1365, 0,  8,  60,  'WK'),
        ('Bhuwaneshwar', 17,  289,  0,  2,  75,  'AR'),
        ('Rohit',        304, 8701, 14, 52, 85,  'BAT'),
        ('Kartick',      11,  111,  0,  0,  75,  'AR'),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO stats VALUES (?,?,?,?,?,?,?)
    ''', players_data)

    # Match data
    match_data = [
        ('Kohli',        'Match1', 102,98, 8,2, 0, 0,0, 0,0,1,0),
        ('Yuvraj',       'Match1', 12, 20, 1,0, 48,0,36,1,0,0,0),
        ('Rahane',       'Match1', 49, 75, 3,0, 0, 0,0, 0,1,0,0),
        ('Dhawan',       'Match1', 32, 35, 4,0, 0, 0,0, 0,0,0,0),
        ('Dhoni',        'Match1', 56, 45, 1,0, 0, 0,0, 3,2,0,0),
        ('Axar',         'Match1', 8,  4,  2,0, 48,2,35,1,0,0,0),
        ('Pandya',       'Match1', 42, 36, 3,3, 30,0,25,1,0,0,0),
        ('Jadeja',       'Match1', 18, 10, 1,1, 60,3,50,2,0,1,0),
        ('Kedar',        'Match1', 65, 60, 7,0, 24,0,24,0,0,0,0),
        ('Ashwin',       'Match1', 23, 42, 3,0, 60,2,45,6,0,0,0),
        ('Umesh',        'Match1', 0,  0,  0,0, 54,0,50,4,1,0,0),
        ('Bumrah',       'Match1', 0,  0,  0,0, 60,2,49,1,0,0,0),
        ('Bhuwaneshwar', 'Match1', 15, 12, 2,0, 60,1,46,2,0,0,0),
        ('Rohit',        'Match1', 46, 65, 5,1, 0, 0,0, 0,1,0,0),
        ('Kartick',      'Match1', 29, 42, 3,0, 0, 0,0, 2,0,1,0),

        ('Kohli',        'Match2', 85, 76, 6,3, 0, 0,0, 0,1,0,0),
        ('Yuvraj',       'Match2', 65, 45, 4,2, 30,0,28,2,0,0,0),
        ('Rahane',       'Match2', 32, 48, 2,0, 0, 0,0, 0,0,0,0),
        ('Dhawan',       'Match2', 78, 65, 8,1, 0, 0,0, 0,0,0,0),
        ('Dhoni',        'Match2', 44, 38, 3,1, 0, 0,0, 0,2,1,0),
        ('Axar',         'Match2', 15, 12, 1,0, 36,1,28,2,0,0,0),
        ('Pandya',       'Match2', 38, 30, 2,2, 24,0,22,1,1,0,0),
        ('Jadeja',       'Match2', 22, 18, 2,0, 48,2,42,3,0,0,0),
        ('Kedar',        'Match2', 42, 38, 3,0, 18,0,18,0,0,0,1),
        ('Ashwin',       'Match2', 18, 25, 1,0, 54,3,48,4,0,0,0),
        ('Umesh',        'Match2', 0,  0,  0,0, 48,0,45,3,0,0,0),
        ('Bumrah',       'Match2', 0,  0,  0,0, 54,1,46,2,1,0,0),
        ('Bhuwaneshwar', 'Match2', 8,  6,  1,0, 48,2,40,3,0,0,0),
        ('Rohit',        'Match2', 92, 78, 9,2, 0, 0,0, 0,0,0,0),
        ('Kartick',      'Match2', 15, 20, 1,0, 0, 0,0, 0,1,0,0),

        ('Kohli',        'Match3', 58, 62, 4,1, 0, 0,0, 0,1,0,0),
        ('Yuvraj',       'Match3', 76, 58, 6,3, 0, 0,0, 0,0,0,0),
        ('Rahane',       'Match3', 34, 45, 3,0, 0, 0,0, 0,0,0,0),
        ('Dhawan',       'Match3', 43, 38, 4,0, 0, 0,0, 0,0,0,0),
        ('Dhoni',        'Match3', 21, 25, 1,0, 0, 0,0, 0,2,0,0),
        ('Axar',         'Match3', 87, 65, 7,3, 36,1,32,1,0,0,0),
        ('Pandya',       'Match3', 43, 38, 3,1, 24,0,20,2,0,0,0),
        ('Jadeja',       'Match3', 26, 22, 2,0, 42,2,38,2,1,0,0),
        ('Kedar',        'Match3', 56, 48, 4,1, 18,0,16,1,0,0,0),
        ('Ashwin',       'Match3', 12, 18, 1,0, 48,2,42,3,0,0,0),
        ('Umesh',        'Match3', 0,  0,  0,0, 42,0,40,2,0,0,0),
        ('Bumrah',       'Match3', 0,  0,  0,0, 48,1,44,3,0,0,0),
        ('Bhuwaneshwar', 'Match3', 6,  8,  0,0, 42,1,36,2,0,0,0),
        ('Rohit',        'Match3', 46, 52, 4,1, 0, 0,0, 0,1,0,0),
        ('Kartick',      'Match3', 18, 24, 1,0, 0, 0,0, 0,0,0,1),
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO match VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', match_data)

    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

if __name__ == "__main__":
    create_database()