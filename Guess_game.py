import random
import tkinter as tk
from tkinter import messagebox

class GuessingGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("400x450")
        self.root.configure(bg="#2C3E50")  # Dark elegant background
        self.root.resizable(False, False)

        # Initialize Game Variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 10
        self.score = 100
        
        # Create UI Elements
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(
            self.root, text="🎯 Number Guesser", 
            font=("Arial", 22, "bold"), fg="#ECF0F1", bg="#2C3E50"
        )
        self.title_label.pack(pady=20)

        # Instructions Label
        self.instruction_label = tk.Label(
            self.root, text="I'm thinking of a number between 1 and 100.\nCan you guess it?", 
            font=("Arial", 12), fg="#BDC3C7", bg="#2C3E50", justify="center"
        )
        self.instruction_label.pack(pady=10)

        # Status and Score Tracking Frame
        self.stats_frame = tk.Frame(self.root, bg="#2C3E50")
        self.stats_frame.pack(pady=10)

        self.attempts_label = tk.Label(
            self.stats_frame, text="Attempts Left: 10", 
            font=("Arial", 11, "bold"), fg="#E74C3C", bg="#2C3E50"
        )
        self.attempts_label.grid(row=0, column=0, padx=20)

        self.score_label = tk.Label(
            self.stats_frame, text="Score: 100", 
            font=("Arial", 11, "bold"), fg="#2ECC71", bg="#2C3E50"
        )
        self.score_label.grid(row=0, column=1, padx=20)

        # Input Entry Box
        self.entry = tk.Entry(
            self.root, font=("Arial", 16), justify="center", 
            width=10, bd=3, relief="groove"
        )
        self.entry.pack(pady=15)
        self.entry.bind("<Return>", lambda event: self.check_guess()) # Press Enter to submit

        # Feedback Message Label
        self.feedback_label = tk.Label(
            self.root, text="Enter a number and click Guess!", 
            font=("Arial", 12, "italic"), fg="#F1C40F", bg="#2C3E50"
        )
        self.feedback_label.pack(pady=10)

        # Action Buttons Frame
        self.btn_frame = tk.Frame(self.root, bg="#2C3E50")
        self.btn_frame.pack(pady=20)

        self.guess_button = tk.Button(
            self.btn_frame, text="Submit Guess", font=("Arial", 12, "bold"),
            bg="#3498DB", fg="white", width=12, command=self.check_guess,
            activebackground="#2980B9", activeforeground="white", cursor="hand2"
        )
        self.guess_button.grid(row=0, column=0, padx=10)

        self.reset_button = tk.Button(
            self.btn_frame, text="Restart", font=("Arial", 12, "bold"),
            bg="#95A5A6", fg="white", width=10, command=self.reset_game,
            activebackground="#7F8C8D", activeforeground="white", cursor="hand2"
        )
        self.reset_button.grid(row=0, column=1, padx=10)

    def reset_game(self):
        """Resets the internal logic backend and clears the screen data."""
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.score = 100
        
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.guess_button.config(state="normal")
        
        self.update_ui_stats()
        self.feedback_label.config(text="Game restarted! Good luck!", fg="#F1C40F")

    def update_ui_stats(self):
        """Refreshes the live numbers displayed on the visual panel."""
        self.attempts_label.config(text=f"Attempts Left: {self.max_attempts - self.attempts}")
        self.score_label.config(text=f"Score: {self.score}")

    def check_guess(self):
        """Processes user input strings and executes win/loss logic loops."""
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        # Input validation framework
        if not user_input.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a whole number between 1 and 100.")
            return

        guess = int(user_input)

        if guess < 1 or guess > 100:
            messagebox.showwarning("Out of Bounds", "Your guess must be between 1 and 100.")
            return

        self.attempts += 1

        # Primary logical resolution pathways
        if guess == self.secret_number:
            self.feedback_label.config(text=f"🎉 Correct! The number was {self.secret_number}!", fg="#2ECC71")
            self.end_game(True)
        else:
            self.score -= 10
            if guess < self.secret_number:
                self.feedback_label.config(text="📈 Too low! Try a higher number.", fg="#E67E22")
            else:
                self.feedback_label.config(text="📉 Too high! Try a lower number.", fg="#E67E22")
            
            self.update_ui_stats()

            if self.attempts >= self.max_attempts:
                self.feedback_label.config(text=f"💀 Game Over! The number was {self.secret_number}.", fg="#E74C3C")
                self.end_game(False)

    def end_game(self, won):
        """Disables controls and triggers an alert pop-up menu."""
        self.entry.config(state="disabled")
        self.guess_button.config(state="disabled")
        
        if won:
            messagebox.showinfo("Victory!", f"You won in {self.attempts} attempts!\nFinal Score: {self.score}")
        else:
            messagebox.showinfo("Defeat", f"Out of tries! The correct answer was {self.secret_number}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessingGameUI(root)
    root.mainloop()
