import random
import tkinter as tk
from tkinter import messagebox

MAX_ATTEMPTS = 6

WORD_BANK = {
    "adventure": ("An exciting or unusual experience.", "It often involves exploring or taking a risk."),
    "beautiful": ("A word used to describe something pleasing to the eyes.", "It is the opposite of ugly."),
    "butterfly": ("A colourful insect with large wings.", "It begins as a caterpillar."),
    "computer": ("An electronic machine used to process data.", "You may use it for coding and browsing."),
    "creative": ("Having the ability to make new or original things.", "Artists and inventors often show this quality."),
    "dinosaur": ("An ancient animal that lived millions of years ago.", "A T-rex is one example."),
    "elephant": ("A very large animal with a trunk.", "It is known for its excellent memory."),
    "galaxy": ("A huge collection of stars, gas, and dust.", "The Milky Way is one."),
    "rainbow": ("A coloured arc sometimes seen after rain.", "It is commonly described as having seven colours.")
}

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Worlds")
        self.root.geometry("380x720")
        self.root.config(bg="#0c0817")

        self.words = list(WORD_BANK.keys())
        
        # Outer wrapper to keep the card nicely centered and spacious
        outer_frame = tk.Frame(root, bg="#0c0817")
        outer_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Main Card Container Frame
        self.card_frame = tk.Frame(outer_frame, bg="#151024", bd=0)
        self.card_frame.pack(fill=tk.BOTH, expand=True)

        self.welcome_frame = tk.Frame(self.card_frame, bg="#151024")
        self.game_frame = tk.Frame(self.card_frame, bg="#151024")

        self.create_welcome_screen()
        self.create_game_screen()

        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

    def create_welcome_screen(self):
        badge = tk.Label(self.welcome_frame, text=" H ", font=("Helvetica", 18, "bold"), bg="#ffd166", fg="#1a153b")
        badge.pack(pady=(35, 10))

        title_lbl = tk.Label(self.welcome_frame, text="HANGMAN WORLDS", font=("Helvetica", 18, "bold"), fg="#ffd166", bg="#151024")
        title_lbl.pack(pady=5)

        sub_lbl = tk.Label(self.welcome_frame, text="A WORD GAME LIKE NO OTHER", font=("Helvetica", 9, "bold"), fg="#a0aec0", bg="#151024")
        sub_lbl.pack(pady=(0, 20))

        hero_title = tk.Label(self.welcome_frame, text="GUESS THE WORD.\nUNLOCK A WORLD.", font=("Helvetica", 18, "bold"), fg="#ffffff", bg="#151024", justify=tk.CENTER)
        hero_title.pack(pady=15)

        desc_lbl = tk.Label(self.welcome_frame, text="A little mystery. A lot of adventure. Think fast, guess smart, and discover where words can take you.", font=("Helvetica", 10), fg="#cbd5e0", bg="#151024", wraplength=280, justify=tk.CENTER)
        desc_lbl.pack(pady=15)

        start_btn = tk.Button(self.welcome_frame, text="START GAME", font=("Helvetica", 12, "bold"), bg="#ffd166", fg="#1a153b", activebackground="#f4a261", activeforeground="#1a153b", bd=0, padx=30, pady=12, cursor="hand2", command=self.start_game_action)
        start_btn.pack(pady=20)

        footer_lbl = tk.Label(self.welcome_frame, text="FREE TO PLAY  •  MADE FOR CURIOUS MINDS", font=("Helvetica", 8, "bold"), fg="#718096", bg="#151024")
        footer_lbl.pack(side=tk.BOTTOM, pady=15)

    def create_game_screen(self):
        badge = tk.Label(self.game_frame, text=" H ", font=("Helvetica", 14, "bold"), bg="#ffd166", fg="#1a153b")
        badge.pack(pady=(10, 5))

        self.game_title = tk.Label(self.game_frame, text="HANGMAN WORLDS", font=("Helvetica", 13, "bold"), fg="#ffd166", bg="#151024")
        self.game_title.pack(pady=2)

        sub_title = tk.Label(self.game_frame, text="A WORD GAME LIKE NO OTHER", font=("Helvetica", 8, "bold"), fg="#a0aec0", bg="#151024")
        sub_title.pack(pady=(0, 8))

        self.word_label = tk.Label(self.game_frame, text="", font=("Helvetica", 18, "bold"), fg="#ffd166", bg="#151024")
        self.word_label.pack(pady=5)

        self.clue_label = tk.Label(self.game_frame, text="", font=("Helvetica", 9, "italic"), fg="#e2e8f0", bg="#1b1233", wraplength=300, justify=tk.CENTER, padx=8, pady=6)
        self.clue_label.pack(pady=5, fill=tk.X, padx=15)

        self.status_label = tk.Label(self.game_frame, text="", font=("Helvetica", 9, "bold"), fg="#a0aec0", bg="#151024")
        self.status_label.pack(pady=3)

        self.hint_btn = tk.Button(self.game_frame, text="Get Hint (-1 Life)", font=("Helvetica", 9, "bold"), bg="#ffd166", fg="#1a153b", activebackground="#f4a261", bd=0, padx=12, pady=5, command=self.use_hint)
        self.hint_btn.pack(pady=3)

        self.keyboard_frame = tk.Frame(self.game_frame, bg="#151024")
        self.keyboard_frame.pack(pady=5)
        self.create_virtual_keyboard()

        back_btn = tk.Button(self.game_frame, text="Back to Home", font=("Helvetica", 9, "bold"), bg="#2d3748", fg="#cbd5e0", bd=0, padx=12, pady=5, command=self.show_welcome_screen)
        back_btn.pack(pady=8)

    def create_virtual_keyboard(self):
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()

        self.key_buttons = {}
        letters = "abcdefghijklmnopqrstuvwxyz"
        
        row = 0
        col = 0
        for l in letters:
            btn = tk.Button(self.keyboard_frame, text=l.upper(), font=("Helvetica", 9, "bold"), 
                            width=3, height=1, bg="#2d3748", fg="#ffffff", 
                            activebackground="#ffd166", activeforeground="#1a153b",
                            bd=0, command=lambda char=l: self.make_guess(char))
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.key_buttons[l] = btn
            col += 1
            if col > 6:  # 7 columns per row for balanced card layout
                col = 0
                row += 1

    def start_game_action(self):
        self.reset_game()
        self.update_ui()
        self.welcome_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)

    def show_welcome_screen(self):
        self.game_frame.pack_forget()
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

    def reset_game(self):
        self.secret_word = random.choice(self.words)
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.hint_used = False
        if hasattr(self, 'key_buttons'):
            for btn in self.key_buttons.values():
                btn.config(state=tk.NORMAL, bg="#2d3748", fg="#ffffff")
        if hasattr(self, 'hint_btn'):
            self.hint_btn.config(state=tk.NORMAL)

    def update_ui(self):
        masked = " ".join(l.upper() if l in self.guessed_letters else "_" for l in self.secret_word)
        self.word_label.config(text=masked)
        
        self.clue_label.config(text=f"Clue: {WORD_BANK[self.secret_word][0]}")
        self.status_label.config(text=f"Lives: {MAX_ATTEMPTS - self.wrong_guesses}   |   Hint Used: {'Yes' if self.hint_used else 'No'}")

    def make_guess(self, letter):
        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        
        if letter in self.key_buttons:
            self.key_buttons[letter].config(state=tk.DISABLED, bg="#231f3d", fg="#4a5568")

        if letter not in self.secret_word:
            self.wrong_guesses += 1

        self.update_ui()
        self.check_game_over()

    def use_hint(self):
        if self.hint_used:
            messagebox.showinfo("Hint", "You have already used your hint in this round.")
            return

        self.hint_used = True
        self.wrong_guesses += 1
        hidden = [l for l in self.secret_word if l not in self.guessed_letters]
        if hidden:
            revealed = random.choice(hidden)
            self.guessed_letters.add(revealed)
            if revealed in self.key_buttons:
                self.key_buttons[revealed].config(state=tk.DISABLED, bg="#231f3d", fg="#4a5568")
        
        self.hint_btn.config(state=tk.DISABLED)
        messagebox.showinfo("Hint", f"Hint: {WORD_BANK[self.secret_word][1]}")
        self.update_ui()
        self.check_game_over()

    def check_game_over(self):
        won = all(l in self.guessed_letters for l in self.secret_word)
        lost = self.wrong_guesses >= MAX_ATTEMPTS

        if won:
            if messagebox.askyesno("You Win!", f"Amazing! The word was {self.secret_word.upper()}.\n\nPlay Again?"):
                self.start_game_action()
            else:
                self.show_welcome_screen()
        elif lost:
            if messagebox.askyesno("Game Over", f"Better luck next time! The word was {self.secret_word.upper()}.\n\nPlay Again?"):
                self.start_game_action()
            else:
                self.show_welcome_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()

