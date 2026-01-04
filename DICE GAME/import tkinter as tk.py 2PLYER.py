import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import time
import threading

class DiceArena2P:
    def __init__(self, root):
        self.root = root
        root.title("Yeezy Dice Arena - 2 Players")
        root.geometry("450x650")
        root.config(bg="#050814")
        
        self.players = {}   # {player_name: roll}
        self.user_names = []  # List of human players
        self.ai_count = 0
        self.current_turn = 0
        self.winner = None

        # ================== UI ==================
        self.title_label = tk.Label(root, text="YEEZY DICE ARENA", font=("Poppins", 20), fg="#ffb703", bg="#050814")
        self.title_label.pack(pady=20)

        self.start_btn = tk.Button(root, text="Start Game", command=self.start_game, font=("Poppins", 14))
        self.start_btn.pack(pady=10)

        self.turn_label = tk.Label(root, text="", font=("Poppins", 14), fg="white", bg="#050814")
        self.turn_label.pack(pady=10)

        self.dice_label = tk.Label(root, text="🎲", font=("Helvetica", 100), bg="#050814", fg="white")
        self.dice_label.pack(pady=20)

        self.roll_btn = tk.Button(root, text="Roll Dice", command=self.roll_dice, font=("Poppins", 14))
        self.roll_btn.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Poppins", 16), fg="white", bg="#050814")
        self.result_label.pack(pady=20)

        self.players_list = tk.Listbox(root, bg="#12163a", fg="white", font=("Poppins",12))
        self.players_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # ================== START GAME ==================
    def start_game(self):
        self.user_names = []
        for i in range(1,3):
            name = simpledialog.askstring("Username", f"Enter Player {i} name:")
            if not name:
                messagebox.showerror("Error", "All players must enter a name")
                return
            self.user_names.append(name)
            self.players[name] = 0

        self.ai_count = simpledialog.askinteger("AI Bots", "Enter number of AI bots (0-3):", minvalue=0, maxvalue=3)
        for i in range(1, self.ai_count+1):
            bot_name = f"AI_Bot_{i}"
            self.players[bot_name] = 0

        self.current_turn = 0
        self.update_players_list()
        self.update_turn_label()
        self.result_label.config(text="Game Started! Roll the dice!")

    # ================== ROLL DICE ==================
    def roll_dice(self):
        if not self.players:
            messagebox.showinfo("Info", "Start the game first!")
            return

        # Determine current player
        current_player = self.get_current_player()
        threading.Thread(target=self.animate_roll, args=(current_player,)).start()

    def animate_roll(self, player):
        for _ in range(10):
            temp_roll = random.randint(1,6)
            self.dice_label.config(text=str(temp_roll))
            time.sleep(0.1)

        # Final roll
        roll = random.randint(1,6)
        self.players[player] = roll
        self.update_players_list()

        # Move turn
        self.next_turn()

        # Randomize winner after everyone has rolled once
        if self.current_turn == 0:  # All players had a turn
            self.randomize_winner()

    # ================== TURN LOGIC ==================
    def get_current_player(self):
        human_count = len(self.user_names)
        all_players = self.user_names + [f"AI_Bot_{i+1}" for i in range(self.ai_count)]
        return all_players[self.current_turn]

    def next_turn(self):
        total_players = len(self.user_names) + self.ai_count
        self.current_turn = (self.current_turn + 1) % total_players
        self.update_turn_label()

        # Auto-roll AI if it's AI's turn
        current_player = self.get_current_player()
        if "AI_Bot" in current_player:
            self.roll_dice()

    def update_turn_label(self):
        self.turn_label.config(text=f"Current Turn: {self.get_current_player()}")

    # ================== RANDOMIZE WINNER ==================
    def randomize_winner(self):
        winner = random.choice(list(self.players.keys()))
        self.winner = winner
        if winner in self.user_names:
            self.result_label.config(text=f"{winner} WINS! 🎉")
        else:
            self.result_label.config(text=f"{winner} WINS! 💀 (AI)")

    # ================== UPDATE PLAYER LIST ==================
    def update_players_list(self):
        self.players_list.delete(0, tk.END)
        for name, roll in self.players.items():
            self.players_list.insert(tk.END, f"{name} | Roll: {roll}")


# ================== RUN APP ==================
root = tk.Tk()
app = DiceArena2P(root)
root.mainloop()
