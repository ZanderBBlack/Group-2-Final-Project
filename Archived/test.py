# Ethan Zodek
# Lab 3
# 2/11/2026

# List of credentials [username, password]
credentials = [
    ['admin', '1234'],
    ['user1', 'pass1'],
    ['user2', 'password']
]

# List of failed attempts for each user. 
# Index 0 corresponds to 'admin', Index 1 to 'user1', etc.
failed_attempts = [0, 0, 0] 

MAX_ATTEMPTS = 3

while True:
    print("\n--- Login ---")
    username = input("Username: ")
    
    # Simple exit condition
    if username == "exit":
        break

    # Find user index
    user_index = -1
    for i in range(len(credentials)):
        if credentials[i][0] == username:
            user_index = i
            break
    
    if user_index == -1:
        print("User not found.")
        continue

    # Check lock status
    if failed_attempts[user_index] >= MAX_ATTEMPTS:
        print("Account Locked. Type 'exit' to quit.")
        continue

    password = input("Password: ")

    if password == credentials[user_index][1]:
        print("Access Granted.")
        failed_attempts[user_index] = 0 # Reset attempts
        break # Exit on success for simplicity
    else:
        print("Access Denied.")
        failed_attempts[user_index] += 1
        
        if failed_attempts[user_index] >= MAX_ATTEMPTS:
            print("Account Locked. Type 'exit' to quit.")

print("Goodbye")