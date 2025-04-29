import openai
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Set your OpenAI API key
openai.api_key = 'YOUR_API_KEY_HERE'  # Replace with your actual API key

# Function to generate a response from OpenAI
def generate_response(prompt, original=False):
    try:
        # Modify the prompt based on whether the user requested an original response
        if original:
            prompt = f"Provide a creative and original response to: {prompt}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change the model if needed
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred: {e}"

# Function to log conversation to a file
def log_conversation(user_input, ai_response):
    with open("conversation_log.txt", "a") as log_file:
        log_file.write(f"You: {user_input}\nAI: {ai_response}\n\n")

# Function to handle sending messages
def send_message():
    user_input = user_input_field.get()
    if user_input.strip() == "":
        messagebox.showwarning("Input Error", "Please enter a message.")
        return

    # Check if the user requested an original response
    original_response = user_input.lower().startswith("original:")
    if original_response:
        user_input = user_input[len("original:"):].strip()  # Remove the command from the input

    # Display user input
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {user_input}\n")
    chat_area.config(state=tk.DISABLED)

    # Generate AI response
    ai_response = generate_response(user_input, original=original_response)

    # Display AI response
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"AI: {ai_response}\n")
    chat_area.config(state=tk.DISABLED)

    # Log the conversation
    log_conversation(user_input, ai_response)

    # Clear the input field
    user_input_field.delete(0, tk.END)

# Create the main application window
app = tk.Tk()
app.title("OpenAI Chatbot")

# Create a text area for chat display
chat_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
chat_area.grid(column=0, row=0, padx=10, pady=10)

# Create an input field for user messages
user_input_field = tk.Entry(app, width=48)
user_input_field.grid(column=0, row=1, padx=10, pady=10)

# Create a send button
send_button = tk.Button(app, text="Send", command=send_message)
send_button.grid(column=0, row=2, padx=10, pady=10)

# Start the application
app.mainloop()