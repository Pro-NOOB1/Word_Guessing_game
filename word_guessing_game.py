import tkinter as tk
from tkinter import messagebox
import random

# Word bank with categories and difficulties
word_bank = {
    "Animals": {
        "easy": ["cat", "dog", "cow", "bat"],
        "medium": ["tiger", "zebra", "sheep", "camel"],
        "hard": ["elephant", "giraffe", "alligator", "kangaroo"]
    },
    "Technology": {
        "easy": ["app", "code", "data", "web"],
        "medium": ["python", "server", "binary", "module"],
        "hard": ["algorithm", "compiler", "database", "encryption"]
    },
    "Sports": {
        "easy": ["run", "ball", "goal", "race"],
        "medium": ["cricket", "boxing", "tennis", "kabaddi"],
        "hard": ["gymnastics", "basketball", "wrestling", "badminton"]
    }
}

class WordGuessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Guessing Game")
        self.category = tk.StringVar()
        self.difficulty = tk.StringVar()
        self.create_start_screen()

    def create_start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select Category", font=("Arial", 16)).pack(pady=5)
        for cat in word_bank:
            tk.Radiobutton(self.root, text=cat, variable=self.category, value=cat).pack(anchor='w')

        tk.Label(self.root, text="Select Difficulty", font=("Arial", 16)).pack(pady=5)
        for diff in ["easy", "medium", "hard"]:
            tk.Radiobutton(self.root, text=diff.capitalize(), variable=self.difficulty, value=diff).pack(anchor='w')

        tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 14)).pack(pady=10)

    def start_game(self):
        cat = self.category.get()
        diff = self.difficulty.get()

        if not cat or not diff:
            messagebox.showerror("Selection Error", "Please select both category and difficulty.")
            return

        self.word = random.choice(word_bank[cat][diff])
        self.hint_used = False
        self.guesses = ''
        self.max_wrong = 6
        self.wrong_guesses = 0
        self.turns = {"easy": 15, "medium": 12, "hard": 10}[diff]

        self.play_screen()

    def play_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.label = tk.Label(self.root, text="Guess the Word!", font=("Arial", 20))
        self.label.pack()

        self.word_display = tk.Label(self.root, text=self.get_display_word(), font=("Arial", 24))
        self.word_display.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Arial", 16), width=5, justify='center')
        self.entry.pack()

        self.guess_btn = tk.Button(self.root, text="Guess", command=self.process_guess)
        self.guess_btn.pack(pady=5)

        self.info = tk.Label(self.root, text=f"Turns Left: {self.turns}", font=("Arial", 14))
        self.info.pack()

        self.message = tk.Label(self.root, text="", font=("Arial", 14))
        self.message.pack(pady=5)

        self.hint_btn = tk.Button(self.root, text="Use Hint", command=self.use_hint)
        self.hint_btn.pack(pady=5)

        self.restart_btn = tk.Button(self.root, text="Restart", command=self.create_start_screen)
        self.restart_btn.pack(pady=5)

    def get_display_word(self):
        return ' '.join([char if char in self.guesses else '_' for char in self.word])

    def process_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not guess.isalpha() or len(guess) != 1:
            self.message.config(text="Enter a single letter!", fg="red")
            return

        if guess in self.guesses:
            self.message.config(text="Already guessed!", fg="orange")
            return

        self.guesses += guess

        if guess in self.word:
            self.message.config(text="Correct!", fg="green")
        else:
            self.turns -= 1
            self.wrong_guesses += 1
            self.message.config(text="Wrong guess!", fg="red")

        self.word_display.config(text=self.get_display_word())
        self.info.config(text=f"Turns Left: {self.turns}")

        if '_' not in self.get_display_word():
            self.message.config(text=f"You Win! Word was: {self.word}", fg="blue")
            self.guess_btn.config(state="disabled")
            self.hint_btn.config(state="disabled")

        elif self.turns == 0:
            self.message.config(text=f"You Lose! Word was: {self.word}", fg="black")
            self.guess_btn.config(state="disabled")
            self.hint_btn.config(state="disabled")

    def use_hint(self):
        if self.hint_used:
            self.message.config(text="Hint already used!", fg="orange")
            return
        unrevealed = [c for c in self.word if c not in self.guesses]
        if unrevealed:
            hint_char = random.choice(unrevealed)
            self.guesses += hint_char
            self.hint_used = True
            self.message.config(text=f"Hint: '{hint_char}' revealed", fg="blue")
            self.word_display.config(text=self.get_display_word())
        else:
            self.message.config(text="Nothing to reveal", fg="green")

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = WordGuessApp(root)
    root.mainloop()
