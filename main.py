from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

BLUE = "#0D1282"
RED = "#D71313"
LIGHT_GRAY = "#EEEDED"
FONT_NAME = "Courier"
is_ok = None


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def password_generator():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for i in range(nr_letters)]
    password_symbol = [random.choice(symbols) for i in range(nr_symbols)]
    password_number = [random.choice(numbers) for i in range(nr_numbers)]

    password_list = password_letter + password_symbol + password_number

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_txt_file():
    global is_ok
    fetch_web = website_entry.get()
    fetch_email = email_entry.get()
    fetch_pass = password_entry.get()
    new_data = {
        fetch_web: {
            "email": fetch_email,
            "password": fetch_pass,
        }
    }

    if len(fetch_web) == 0 or len(fetch_pass) == 0:
        messagebox.askokcancel(title=fetch_web, message=f"Missing entries.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH BUTTON ------------------------------- #

def search():
    fetch_web = website_entry.get()
    in_file = False
    temp_dict = {}
    if len(fetch_web) == 0:
        messagebox.askokcancel(title=fetch_web, message=f"Website Entry is blank.")
    else:
        try:
            with open("data.json", "r") as data_file:
                y = data_file.read()
                dict_file = json.loads(y)
                for x, key in dict_file.items():
                    if fetch_web == x:
                        temp_dict['email'] = key['email']
                        temp_dict['password'] = key['password']
                        in_file = True

                if in_file:
                    messagebox.askokcancel(title=fetch_web, message=f"{temp_dict['email']} and {temp_dict['password']}")
                else:
                    messagebox.askokcancel(title=fetch_web, message=f"No credentials found under {fetch_web}")

        except FileNotFoundError:
            messagebox.askokcancel(title=fetch_web, message=f"Data File Not Found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=LIGHT_GRAY)

canvas = Canvas(width=200, height=200, bg=LIGHT_GRAY)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_text = Label(text="Website:", bg=LIGHT_GRAY, foreground=RED, font=(FONT_NAME, 12, "normal"))
website_text.grid(column=0, row=1)
email_text = Label(text="Email/Username:", bg=LIGHT_GRAY, foreground=RED, font=(FONT_NAME, 12, "normal"))
email_text.grid(column=0, row=2)
password_text = Label(text="Password:", bg=LIGHT_GRAY, foreground=RED, font=(FONT_NAME, 12, "normal"))
password_text.grid(column=0, row=3)

website_entry = Entry(width=35)
website_entry.insert(END, "")
website_entry.grid(column=1, columnspan=2, row=1, sticky="EW")
email_entry = Entry(width=35)
email_entry.grid(column=1, columnspan=2, row=2, sticky="EW")
password_entry = Entry(width=35)
password_entry.grid(column=1, columnspan=2, row=3, sticky="EW")

search_but = Button(text="Search", command=search)
search_but.grid(column=3, row=1, sticky="EW")
gen_pass_but = Button(text="Generate Password", command=password_generator)
gen_pass_but.grid(column=2, row=3, sticky="EW")
add_but = Button(text="Add", width=36, command=add_txt_file)
add_but.grid(column=1, columnspan=2, row=5, sticky="EW")

window.mainloop()
