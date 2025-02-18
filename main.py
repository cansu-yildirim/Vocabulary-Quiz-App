import tkinter as tk
import random
import pygame
from words import words  # Extract the words from the words.py file

pygame.mixer.init()
correct_sound = pygame.mixer.Sound("./sounds/positive.mp3")
fail_sound = pygame.mixer.Sound("./sounds/whoosh.mp3")

# Words known correctly
correct_words = []

def get_question():
    global correct_option  # Define the correct answer as a global variable
    
    remaining_words = [word for word in words if word not in correct_words]
    if not remaining_words:
        result_label.config(text="Congratulations! You knew all the words!", fg="green")
        return None

    question = random.choice(remaining_words)
    english_word, turkish_word = question
    correct_option = turkish_word  # Save the correct option

    options = [correct_option]
    while len(options) < 4:
        option = random.choice(words)[1]  # Turkish options
        if option not in options:
            options.append(option)
    
    random.shuffle(options)
    return english_word, options, correct_option

    
    random.shuffle(options)
    return english_word, options, correct_option

def check_answer(selected_index, correct_option):
    # Play a sound according to the selected answer
    if option_buttons[selected_index]["text"] == correct_option:
        correct_sound.play()  # Play the correct sound
        result_label.config(text=random.choice(["Nice work!", "Excellent!"]), fg="green")
    else:
        fail_sound.play()  # Play the wrong sound
        result_label.config(text="Not quite, you're still learning!", fg="red")
    
    # Select the options
    for i, btn in enumerate(option_buttons):
        if btn["text"] == correct_option:
            btn.config(text=f"✓ {btn['text']}", fg="green")
        elif i == selected_index:
            btn.config(text=f"✗ {btn['text']}", fg="red")
    
    root.after(1500, next_question)  # New question after 1.5 seconds

def reveal_answer():
    global correct_option  # To track the correct answer

    # Play the incorrect sound
    fail_sound.play()

    # Display the correct option
    for btn in option_buttons:
        if btn["text"] == correct_option:  # Mark the correct one
            btn.config(text=f"✓ {btn['text']}", fg="green")

    root.after(1500, next_question)  # A new question in 1.5 seconds


def next_question():
    question_data = get_question()
    if question_data is None:
        return
    
    english_word, options, correct_option = question_data
    question_label.config(text=f"{english_word}", anchor="w")  # Word aligned to the left
    result_label.config(text="Don't you have an idea?", fg="white")  # Reset when a new question arrives
    result_label.bind("<Button-1>", lambda event: reveal_answer())

    for i, btn in enumerate(option_buttons):
        btn.config(text=options[i], fg="black", command=lambda i=i: check_answer(i, correct_option))

# Interface
root = tk.Tk()
root.title("Kelime Sınavı")
root.geometry("800x450")
root.configure(bg="#363332")

# Text 'Study with Learn' in the top right corner
study_label = tk.Label(root, text="Study with Learn", font=("Lato", 16), bg="#363332", fg="white", anchor="e")
study_label.pack(anchor="ne", padx=10, pady=5)

# Question text (left-aligned)
question_label = tk.Label(root, text="Bir soru geliyor...", font=("Helvetica", 25), bg="#363332", fg="white", anchor="w")
question_label.pack(fill="x", padx=30, pady=10)

# "Choose matching term"
instruction_label = tk.Label(
    root,
    text="Choose matching term",
    font=("Helvetica", 12, "bold"),
    bg="#363332",
    fg="#646262",
    anchor="w",  
    justify="left"  
)
instruction_label.pack(fill="x", padx=30, pady=10)

# A frame for the options (for a 2x2 layout)
button_frame = tk.Frame(root, bg="#363332")
button_frame.pack(pady=20)

option_buttons = []
for row in range(2):
    for col in range(2):
        button = tk.Button(
            button_frame, 
            text="", 
            font=("Helvetica", 14), 
            width=35, 
            height=3, 
            bg="#464240",  
            fg="white",  
            activebackground="#5A534D",
            activeforeground="white", 
            relief="flat" 
        )
        button.grid(row=row, column=col, padx=10, pady=10)
        option_buttons.append(button)


# Result label
result_label = tk.Label(root, text="Do you have any idea?", font=("Helvetica", 14), bg="#363332", fg="white", cursor="hand2")
result_label.pack(pady=10)  
result_label.bind("<Button-1>", lambda event: next_question()) 



next_question()
root.mainloop()