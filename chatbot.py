import json
import re
import tkinter as tk
from tkinter import scrolledtext, ttk


# Load FAQ dataset from external JSON file
def load_faq_data():
  try:
    with open("faq.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except FileNotFoundError:
    return {
        "greeting": {
            "patterns": [r"\bhi\b", r"\bhello\b", r"\bhey\b"],
            "response": "Hello! How can I help you today?",
        }
    }


faq_data = load_faq_data()


def get_bot_response(user_input):
  normalized_input = user_input.lower().strip()

  for intent, data in faq_data.items():
    for pattern in data["patterns"]:
      if re.search(pattern, normalized_input):
        return data["response"]

  return (
      "I'm sorry, I didn't quite understand that. You can ask me about our"
      " business hours, shipping policy, return/refund policy, or contact"
      " details!"
  )


class ChatBotApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Customer Support Chatbot")
    self.root.geometry("400x520")
    self.root.minsize(350, 450)
    self.root.configure(bg="#f4f6f9")

    # Header Frame
    header_frame = tk.Frame(root, bg="#1E3A8A", height=50)
    header_frame.pack(fill=tk.X, side=tk.TOP)

    header_label = tk.Label(
        header_frame,
        text="Support Assistant",
        bg="#1E3A8A",
        fg="white",
        font=("Arial", 12, "bold"),
    )
    header_label.pack(pady=12)

    # Chat History Display Area with subtle styling
    self.chat_display = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, state="disabled", font=("Arial", 10), bg="#ffffff"
    )
    self.chat_display.pack(
        padx=12, pady=(12, 8), fill=tk.BOTH, expand=True
    )

    # Frame for Entry and Send Button
    self.input_frame = tk.Frame(root, bg="#f4f6f9")
    self.input_frame.pack(padx=12, pady=(0, 12), fill=tk.X)

    # User Input Field
    self.entry_field = tk.Entry(
        self.input_frame, font=("Arial", 11), relief=tk.SOLID, bd=1
    )
    self.entry_field.pack(
        side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8)
    )
    self.entry_field.bind("<Return>", self.send_message)

    # Send Button (Styled)
    self.send_btn = tk.Button(
        self.input_frame,
        text="Send",
        command=self.send_message,
        bg="#1E3A8A",
        fg="white",
        font=("Arial", 10, "bold"),
        relief=tk.FLAT,
        padx=12,
        pady=4,
    )
    self.send_btn.pack(side=tk.RIGHT)

    # Initial Bot Greeting
    self.display_message(
        "Bot: Hello! Loaded FAQ from JSON dataset successfully. Ask me anything"
        " about hours, shipping, or refunds. Type 'exit' to quit.\n"
    )

  def display_message(self, message):
    self.chat_display.config(state="normal")
    self.chat_display.insert(tk.END, message + "\n\n")
    self.chat_display.config(state="disabled")
    self.chat_display.see(tk.END)

  def send_message(self, event=None):
    user_text = self.entry_field.get().strip()
    if not user_text:
      return

    # Display User Message
    self.display_message(f"You: {user_text}")
    self.entry_field.delete(0, tk.END)

    # Check for exit commands (Ab yeh window khud band nahi karega)
    if user_text.lower() in ["bye", "exit", "quit"]:
      self.display_message(
          "Bot: Thank you for chatting with us! Have a wonderful day!"
      )
      return

    # Get and Display Bot Response
    bot_response = get_bot_response(user_text)
    self.display_message(f"Bot: {bot_response}")


if __name__ == "__main__":
  root = tk.Tk()
  app = ChatBotApp(root)
  root.mainloop()
