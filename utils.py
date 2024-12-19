def get_user_input(prompt):
    return input(prompt)

def get_user_choice(prompt, options):
    while True:
        choice = get_user_input(prompt)
        if choice in options:
            return choice
        else:
            print("Invalid choice. Please try again.")
