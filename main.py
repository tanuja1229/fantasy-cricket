import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
from database import create_database

# Create database on startup
create_database()

# ─── Database Helper Functions ───────────────────────────
def get_players_by_category(category):
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute("SELECT player FROM stats WHERE category=?", (category,))
    players = [row[0] for row in cursor.fetchall()]
    conn.close()
    return players

def get_player_value(player):
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM stats WHERE player=?", (player,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def save_team(team_name, selected_players, total_value):
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teams WHERE name=?", (team_name,))
    players_str = ','.join(selected_players)
    cursor.execute("INSERT INTO teams VALUES (?,?,?)",
                   (team_name, players_str, total_value))
    conn.commit()
    conn.close()

def load_teams():
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM teams")
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    return teams

def load_team_players(team_name):
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute("SELECT players FROM teams WHERE name=?", (team_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0].split(',') if result else []

def get_matches():
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT match_name FROM match")
    matches = [row[0] for row in cursor.fetchall()]
    conn.close()
    return matches

# ─── Score Calculation ────────────────────────────────────
def calculate_player_score(player, match_name):
    conn = sqlite3.connect('cricket.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT scored, faced, fours, sixes, bowled,
               maiden, given, wkts, catches, stumping, runout
        FROM match WHERE player=? AND match_name=?
    """, (player, match_name))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return 0

    scored, faced, fours, sixes, bowled, maiden, given, wkts, catches, stumping, runout = row
    points = 0

    # Batting points
    points += scored // 2
    if scored >= 50:
        points += 5
    if scored >= 100:
        points += 10
    if faced > 0:
        strike_rate = (scored / faced) * 100
        if 80 <= strike_rate <= 100:
            points += 2
        elif strike_rate > 100:
            points += 6
    points += fours * 1
    points += sixes * 2

    # Bowling points
    points += wkts * 10
    if wkts >= 3:
        points += 5
    if wkts >= 5:
        points += 10
    if bowled > 0:
        economy = (given / bowled) * 6
        if 3.5 <= economy <= 4.5:
            points += 4
        elif 2 <= economy < 3.5:
            points += 7
        elif economy < 2:
            points += 10

    # Fielding points
    points += catches * 10
    points += stumping * 10
    points += runout * 10

    return points

# ─── Main Application ─────────────────────────────────────
class FantasyCricketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy Cricket")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.team_name = None
        self.selected_players = []
        self.total_value = 1000
        self.points_used = 0

        self.bat_count = 0
        self.bow_count = 0
        self.ar_count  = 0
        self.wk_count  = 0

        self.build_ui()

    def build_ui(self):
        # ── Menu Bar
        menubar = tk.Menu(self.root)
        manage_menu = tk.Menu(menubar, tearoff=0)
        manage_menu.add_command(label="NEW Team",      command=self.new_team)
        manage_menu.add_command(label="OPEN Team",     command=self.open_team)
        manage_menu.add_command(label="SAVE Team",     command=self.save_team)
        manage_menu.add_command(label="EVALUATE Team", command=self.evaluate_team)
        menubar.add_cascade(label="Manage Teams", menu=manage_menu)
        self.root.config(menu=menubar)

        # ── Top: Selection counts
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(top_frame, text="Your Selections", 
                 bg="#f0f0f0", font=("Arial", 10, "bold")).pack(anchor="w")

        counts_frame = tk.Frame(top_frame, bg="#f0f0f0")
        counts_frame.pack(fill=tk.X)

        self.bat_label = tk.Label(counts_frame, text="Batsmen (BAT) 0",
                                   bg="#f0f0f0", font=("Arial", 9))
        self.bat_label.pack(side=tk.LEFT, padx=10)

        self.bow_label = tk.Label(counts_frame, text="Bowlers (BOW) 0",
                                   bg="#f0f0f0", font=("Arial", 9))
        self.bow_label.pack(side=tk.LEFT, padx=10)

        self.ar_label = tk.Label(counts_frame, text="Allrounders (AR) 0",
                                  bg="#f0f0f0", font=("Arial", 9))
        self.ar_label.pack(side=tk.LEFT, padx=10)

        self.wk_label = tk.Label(counts_frame, text="Wicket-keeper (WK) 0",
                                  bg="#f0f0f0", font=("Arial", 9))
        self.wk_label.pack(side=tk.LEFT, padx=10)

        # ── Points bar
        points_frame = tk.Frame(self.root, bg="#f0f0f0")
        points_frame.pack(fill=tk.X, padx=10)

        self.points_avail_label = tk.Label(points_frame,
                                            text="Points Available: 1000",
                                            bg="#f0f0f0", font=("Arial", 9))
        self.points_avail_label.pack(side=tk.LEFT)

        self.points_used_label = tk.Label(points_frame,
                                           text="Points Used: 0",
                                           bg="#f0f0f0", font=("Arial", 9))
        self.points_used_label.pack(side=tk.RIGHT)

        # ── Radio buttons
        radio_frame = tk.Frame(self.root, bg="#f0f0f0")
        radio_frame.pack(fill=tk.X, padx=10, pady=5)

        self.category_var = tk.StringVar(value="BAT")
        for cat in [("BAT", "BAT"), ("BOW", "BWL"),
                    ("AR",  "AR"),  ("WK",  "WK")]:
            tk.Radiobutton(radio_frame, text=cat[0],
                           variable=self.category_var,
                           value=cat[1],
                           bg="#f0f0f0",
                           command=self.load_players,
                           state=tk.DISABLED).pack(side=tk.LEFT, padx=5)

        self.radio_buttons = radio_frame.winfo_children()

        # ── Main area: two listboxes
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left listbox — available players
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(left_frame, text="Available Players",
                 bg="#f0f0f0", font=("Arial", 9, "bold")).pack()

        self.players_listbox = tk.Listbox(left_frame, width=30, height=20,
                                           selectmode=tk.SINGLE)
        self.players_listbox.pack(fill=tk.BOTH, expand=True)
        self.players_listbox.bind("<Double-Button-1>", self.add_player)

        # Arrow button
        arrow_frame = tk.Frame(main_frame, bg="#f0f0f0")
        arrow_frame.pack(side=tk.LEFT, padx=5)
        tk.Button(arrow_frame, text=">", width=3,
                  command=self.add_player).pack(pady=5)
        tk.Button(arrow_frame, text="<", width=3,
                  command=self.remove_player).pack(pady=5)

        # Right listbox — selected players
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.team_name_label = tk.Label(right_frame,
                                         text="Team Name: -",
                                         bg="#f0f0f0",
                                         font=("Arial", 9, "bold"))
        self.team_name_label.pack()

        self.selected_listbox = tk.Listbox(right_frame, width=30, height=20,
                                            selectmode=tk.SINGLE)
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)
        self.selected_listbox.bind("<Double-Button-1>", self.remove_player)

    # ─── Team Actions ─────────────────────────────────────
    def new_team(self):
        name = simpledialog.askstring("New Team", "Enter team name:")
        if not name:
            return
        self.team_name = name
        self.selected_players = []
        self.points_used = 0
        self.bat_count = self.bow_count = self.ar_count = self.wk_count = 0

        self.selected_listbox.delete(0, tk.END)
        self.team_name_label.config(text=f"Team Name: {name}")
        self.update_points()
        self.update_counts()

        # Enable radio buttons
        for rb in self.radio_buttons:
            rb.config(state=tk.NORMAL)

        self.load_players()

    def open_team(self):
        teams = load_teams()
        if not teams:
            messagebox.showinfo("Open Team", "No saved teams found!")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Open Team")
        popup.geometry("300x200")

        tk.Label(popup, text="Select a team:").pack(pady=10)
        team_var = tk.StringVar(value=teams[0])
        for t in teams:
            tk.Radiobutton(popup, text=t,
                           variable=team_var, value=t).pack()

        def load():
            self.team_name = team_var.get()
            self.selected_players = load_team_players(self.team_name)
            self.points_used = sum(get_player_value(p)
                                   for p in self.selected_players)
            self.bat_count = sum(1 for p in self.selected_players
                                 if self.get_category(p) == 'BAT')
            self.bow_count = sum(1 for p in self.selected_players
                                 if self.get_category(p) == 'BWL')
            self.ar_count  = sum(1 for p in self.selected_players
                                 if self.get_category(p) == 'AR')
            self.wk_count  = sum(1 for p in self.selected_players
                                 if self.get_category(p) == 'WK')

            self.selected_listbox.delete(0, tk.END)
            for p in self.selected_players:
                self.selected_listbox.insert(tk.END, p)

            self.team_name_label.config(
                text=f"Team Name: {self.team_name}")
            self.update_points()
            self.update_counts()

            for rb in self.radio_buttons:
                rb.config(state=tk.NORMAL)
            self.load_players()
            popup.destroy()

        tk.Button(popup, text="Open", command=load).pack(pady=10)

    def save_team(self):
        if not self.team_name:
            messagebox.showerror("Error", "Please create a team first!")
            return
        save_team(self.team_name, self.selected_players, self.points_used)
        messagebox.showinfo("Saved", f"Team '{self.team_name}' saved!")

    def evaluate_team(self):
        teams  = load_teams()
        matches = get_matches()

        if not teams or not matches:
            messagebox.showerror("Error", "No teams or matches found!")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Evaluate Team Performance")
        popup.geometry("500x500")

        tk.Label(popup,
                 text="Evaluate the Performance of your Fantasy Team",
                 font=("Arial", 11, "bold")).pack(pady=10)

        select_frame = tk.Frame(popup)
        select_frame.pack()

        tk.Label(select_frame, text="Select Team:").grid(
            row=0, column=0, padx=5)
        team_var = ttk.Combobox(select_frame, values=teams, width=15)
        team_var.grid(row=0, column=1, padx=5)
        team_var.current(0)

        tk.Label(select_frame, text="Select Match:").grid(
            row=0, column=2, padx=5)
        match_var = ttk.Combobox(select_frame, values=matches, width=10)
        match_var.grid(row=0, column=3, padx=5)
        match_var.current(0)

        result_frame = tk.Frame(popup)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        players_list = tk.Listbox(result_frame, width=25, height=15)
        players_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        points_list = tk.Listbox(result_frame, width=10, height=15)
        points_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        total_label = tk.Label(popup, text="Total Points: 0",
                                font=("Arial", 12, "bold"))
        total_label.pack()

        def calculate():
            players_list.delete(0, tk.END)
            points_list.delete(0, tk.END)

            team    = team_var.get()
            match   = match_var.get()
            players = load_team_players(team)
            total   = 0

            for p in players:
                score = calculate_player_score(p, match)
                total += score
                players_list.insert(tk.END, p)
                points_list.insert(tk.END, score)

            total_label.config(text=f"Total Points: {total}")

        tk.Button(popup, text="Calculate Score",
                  command=calculate,
                  bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold")).pack(pady=5)

    # ─── Player List ──────────────────────────────────────
    def load_players(self):
        category = self.category_var.get()
        players  = get_players_by_category(category)
        self.players_listbox.delete(0, tk.END)
        for p in players:
            if p not in self.selected_players:
                self.players_listbox.insert(tk.END, p)

    def get_category(self, player):
        conn = sqlite3.connect('cricket.db')
        cursor = conn.cursor()
        cursor.execute("SELECT category FROM stats WHERE player=?",
                       (player,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else ''

    # ─── Add / Remove ─────────────────────────────────────
    def add_player(self, event=None):
        if not self.team_name:
            messagebox.showerror("Error", "Please create a team first!")
            return

        selection = self.players_listbox.curselection()
        if not selection:
            return

        player   = self.players_listbox.get(selection[0])
        category = self.get_category(player)
        value    = get_player_value(player)

        # Validation rules
        if len(self.selected_players) >= 11:
            messagebox.showerror("Error", "Team already has 11 players!")
            return
        if self.points_used + value > self.total_value:
            messagebox.showerror("Error", "Not enough points!")
            return
        if category == 'WK' and self.wk_count >= 1:
            messagebox.showerror("Error",
                "You can't select more than one wicket-keeper.")
            return
        if category == 'BAT' and self.bat_count >= 5:
            messagebox.showerror("Error",
                "Maximum 5 batsmen allowed!")
            return
        if category == 'BWL' and self.bow_count >= 4:
            messagebox.showerror("Error",
                "Maximum 4 bowlers allowed!")
            return
        if category == 'AR' and self.ar_count >= 3:
            messagebox.showerror("Error",
                "Maximum 3 allrounders allowed!")
            return

        # Add player
        self.selected_players.append(player)
        self.selected_listbox.insert(tk.END, player)
        self.players_listbox.delete(selection[0])

        self.points_used += value
        if category == 'BAT': self.bat_count += 1
        if category == 'BWL': self.bow_count += 1
        if category == 'AR':  self.ar_count  += 1
        if category == 'WK':  self.wk_count  += 1

        self.update_points()
        self.update_counts()

    def remove_player(self, event=None):
        selection = self.selected_listbox.curselection()
        if not selection:
            return

        player   = self.selected_listbox.get(selection[0])
        category = self.get_category(player)
        value    = get_player_value(player)

        self.selected_players.remove(player)
        self.selected_listbox.delete(selection[0])
        self.players_listbox.insert(tk.END, player)

        self.points_used -= value
        if category == 'BAT': self.bat_count -= 1
        if category == 'BWL': self.bow_count -= 1
        if category == 'AR':  self.ar_count  -= 1
        if category == 'WK':  self.wk_count  -= 1

        self.update_points()
        self.update_counts()

    # ─── UI Updates ───────────────────────────────────────
    def update_points(self):
        avail = self.total_value - self.points_used
        self.points_avail_label.config(
            text=f"Points Available: {avail}")
        self.points_used_label.config(
            text=f"Points Used: {self.points_used}")

    def update_counts(self):
        self.bat_label.config(text=f"Batsmen (BAT) {self.bat_count}")
        self.bow_label.config(text=f"Bowlers (BOW) {self.bow_count}")
        self.ar_label.config( text=f"Allrounders (AR) {self.ar_count}")
        self.wk_label.config( text=f"Wicket-keeper (WK) {self.wk_count}")

# ─── Run App ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = FantasyCricketApp(root)
    root.mainloop()