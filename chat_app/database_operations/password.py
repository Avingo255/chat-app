def get_password():
    try:
        with open("password.txt", "r") as file:
            password = file.read().strip()
            return password
    except FileNotFoundError:
        print("Password file not found.")
        return None