import tkinter as tk
import random
import os
from playsound import playsound

class GuessingGame:
    def __init__(self, master):
        self.master = master
        self.master.title("🎯 Guessing Game")
        self.master.geometry("400x400")
        self.difficulty = tk.StringVar(value="Medium")
        self.max_number = 100
        self.number_to_guess = None
        self.attempts = 0
        self.high_score = self.load_high_score()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Choose Difficulty:", font=("Arial", 12)).pack(pady=5)
        for name in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(self.master, text=name, variable=self.difficulty, value=name, command=self.set_difficulty).pack()
        self.info_label = tk.Label(self.master, text="Click 'Start Game' to begin!", font=("Arial", 10))
        self.info_label.pack(pady=10)
        self.high_score_label = tk.Label(self.master, text=f"🏆 High Score: {self.high_score if self.high_score else 'None'}", font=("Arial", 10))
        self.high_score_label.pack(pady=5)
        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=5)
        self.entry = tk.Entry(self.master, state='disabled')
        self.entry.pack(pady=5)
        self.submit_button = tk.Button(self.master, text="Submit Guess", command=self.check_guess, state='disabled')
        self.submit_button.pack(pady=5)
        self.feedback = tk.Label(self.master, text="", font=("Arial", 12))
        self.feedback.pack(pady=10)
        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game, state='disabled')
        self.restart_button.pack(pady=5)

    def set_difficulty(self):
        self.max_number = {"Easy": 50, "Medium": 100, "Hard": 200}.get(self.difficulty.get(), 100)

    def start_game(self):
        self.set_difficulty()
        self.number_to_guess = random.randint(1, self.max_number)
        self.attempts = 0
        self.entry.config(state='normal')
        self.submit_button.config(state='normal')
        self.restart_button.config(state='normal')
        self.feedback.config(text="")
        self.entry.delete(0, tk.END)
        self.info_label.config(text=f"Guess a number between 1 and {self.max_number}.")

    def check_guess(self):
        guess = self.entry.get()
        if not guess.isdigit():
            self.feedback.config(text="❗ Please enter a valid number.")
            return
        guess = int(guess)
        self.attempts += 1
        if guess < self.number_to_guess:
            self.feedback.config(text="🔻 Too low!")
            playsound(os.path.join(os.path.dirname(__file__), "low.wav"))
        elif guess > self.number_to_guess:
            self.feedback.config(text="🔺 Too high!")
            playsound(os.path.join(os.path.dirname(__file__), "high.wav"))
        else:
            self.feedback.config(text=f"🎉 Correct! You guessed it in {self.attempts} attempts.")
            playsound(os.path.join(os.path.dirname(__file__), "correct.wav"))
            self.entry.config(state='disabled')
            self.submit_button.config(state='disabled')
            if self.high_score is None or self.attempts < self.high_score:
                self.feedback.config(text=self.feedback.cget("text") + "\n🏅 New high score!")
                self.save_high_score(self.attempts)
                self.high_score = self.attempts
                self.high_score_label.config(text=f"🏆 High Score: {self.high_score}")

    def restart_game(self):
        self.entry.delete(0, tk.END)
        self.start_game()

    def load_high_score(self):
        try:
            with open("highscore_gui.txt", "r") as file:
                return int(file.read())
        except:
            return None

    def save_high_score(self, score):
        with open("highscore_gui.txt", "w") as file:
            file.write(str(score))

root = tk.Tk()
app = GuessingGame(root)
root.mainloop()
