import tkinter as tk
from tkinter import *
import sqlite3 as db

# Model
class DatabaseModel:
    def __init__(self):
        self.conn = db.connect("UserInfo.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Info
            (
                Brecieved TEXT,
                Crecieved TEXT,
                StoreNumber TEXT,
                Bdelivered TEXT,
                Cdelivered TEXT
            )
            """
        )
        self.conn.commit()

    def insert_data(self, data):
        self.cur.execute(
            "INSERT INTO Info VALUES (?, ?, ?, ?, ?)", data
        )
        self.conn.commit()

    def get_all_data(self):
        self.cur.execute(
            "SELECT Brecieved, Crecieved, StoreNumber, Bdelivered, Cdelivered FROM Info"
        )
        return self.cur.fetchall()

    def get_latest_data(self):
        self.cur.execute(
            "SELECT Brecieved, Crecieved, StoreNumber, Bdelivered, Cdelivered FROM Info ORDER BY rowid DESC LIMIT 1"
        )
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()


# Views
class LoginView(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        Label(self, text = 'Welcome to D and S Distributors',
              font=("Arial", 20), fg="black", bg="white").grid(row =1, column= 1)

        Label(self, text="Username:", font=("Arial", 15)).grid(row=2, column=0, sticky="e", pady=10, padx=10)
        self.username_entry = Entry(self, font=("Arial", 15))
        self.username_entry.grid(row=2, column=1, sticky="w", pady=10, padx=10)

        Label(self, text="Password:", font=("Arial", 15)).grid(row=4, column=0, sticky="e", pady=10, padx=10)
        self.password_entry = Entry(self, show="*", font=("Arial", 15))
        self.password_entry.grid(row=4, column=1, sticky="w", pady=10, padx=10)

        Button(self, text="Login", command=self.controller.login, bg="skyblue", font=("Arial", 15)).grid(row=7, column=0, columnspan=2, pady=10, padx=10)

    def get_credentials(self):
        return self.username_entry.get(), self.password_entry.get()
    

class SecondView(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        Label(self, text="Will you be making any deliveries today?", font=("Arial", 15), fg="black", bg="white").grid(row=1, column=0)

        Button(self, text="Yes", command=self.controller.show_third_view, bg="skyblue", font=("Arial", 15)).grid(row=4, column=0, columnspan=2)
        Label(self, text= 'OR', font=("Arial", 15)).grid(row=5,column=0)
        Button(self, text="No", command=self.controller.show_fourth_view, bg="skyblue", font=("Arial", 15)).grid(row=6, column=0, columnspan=2)

class ThirdView(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        Label(self, text="Details", font=("Arial", 15), fg="black", bg="white").grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        
        Label(self, text="Boxes Recieved(BR):", font=("Arial", 15), fg="black", bg="white").grid(row=1, column=0)
        self.entry1 = Entry(self, font=("Arial", 15))
        self.entry1.grid(row=1, column=1)

        Label(self, text="Crates Received(CR):", font=("Arial", 15), fg="black", bg="white").grid(row=2, column=0)
        self.entry2 = Entry(self, font=("Arial", 15))
        self.entry2.grid(row=2, column=1)

        Label(self, text="Store Number(S#):", font=("Arial", 15), fg="black", bg="white").grid(row=3, column=0)
        self.entry3 = Entry(self, font=("Arial", 15))
        self.entry3.grid(row=3, column=1)

        Label(self, text="Boxes Delivered(BD):", font=("Arial", 15), fg="black", bg="white").grid(row=4, column=0)
        self.entry4 = Entry(self, font=("Arial", 15))
        self.entry4.grid(row=4, column=1)

        Label(self, text="Crates Delivered(CD):", font=("Arial", 15), fg="black", bg="white").grid(row=5, column=0)
        self.entry5 = Entry(self, font=("Arial", 15))
        self.entry5.grid(row=5, column=1)

        Button(self, text="Back", command=self.controller.show_second_view, bg="skyblue", font=("Arial", 15)).grid(row=9, column=0)
        Button(self, text="Add Data", command=self.controller.add_data_to_database, bg="skyblue", font=("Arial", 15)).grid(row=9, column=1)
        Button(self, text="Next", command=self.controller.show_fourth_view, bg="skyblue", font=("Arial", 15)).grid(row=9, column=2)

    def get_data(self):
        return (
            self.entry1.get(),
            self.entry2.get(),
            self.entry3.get(),
            self.entry4.get(),
            self.entry5.get(),
        )
class FourthView(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        self.label = tk.Label(master, text="")
        self.label.pack()

        Label(self, text=" BR    CR    S#     BD    CD").grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        Button(self, text="Back", command=self.controller.show_third_view, bg="skyblue", font=("Arial", 15)).grid(row=11, column=0)
        Button(self, text="Main Menu", command=self.controller.show_login_view, bg="skyblue", font=("Arial", 15)).grid(row=11, column=1)
        Button(self, text="Get All Records", command=self.controller.get_all_records, bg="skyblue", font=("Arial", 15)).grid(row=9, column=0)
        Button(self, text="Get Latest Record", command=self.controller.get_latest_record, bg="skyblue", font=("Arial", 15)).grid(row=9, column=1)

    def update_label(self, data):
        self.label.config(text="\n".join([str(row) for row in data]))

    def show_all_records(self):
        records = self.controller.get_all_records()
        self.update_label(records)

    def show_latest_record(self):
        record = self.controller.get_latest_record()
        self.update_label([record])

# Controller
class Controller:
    def __init__(self, master):
        self.model = DatabaseModel()

        self.login_view = LoginView(master, self)
        self.second_view = SecondView(master, self)
        self.third_view = ThirdView(master, self)
        self.fourth_view = FourthView(master, self)

        self.login_view.pack()

    def login(self):
        username, password = self.login_view.get_credentials()
        valid_users = {
            "user": "pass",
            "Guest": "",
            "Daniel": "BigDawg32",
            "Andrew": "Letzgo",
        }

        if valid_users.get(username) == password:
            self.login_view.pack_forget()
            self.second_view.pack()
        else:
            Label(
                self.login_view,
                text="Invalid Password.\n Enter Guest with No Password to continue",
            ).grid(row=8, column=0, columnspan=2)

    def show_second_view(self):
        self.third_view.pack_forget()
        self.second_view.pack()

    def show_third_view(self):
        self.second_view.pack_forget()
        self.fourth_view.pack_forget()
        self.third_view.pack()

    def show_fourth_view(self):
        self.second_view.pack_forget()
        self.third_view.pack_forget()
        self.fourth_view.pack()

    def show_login_view(self):
        self.fourth_view.pack_forget()
        self.login_view.pack()

    def add_data_to_database(self):
        data = self.third_view.get_data()
        self.model.insert_data(data)

    def get_all_records(self):
        data = self.model.get_all_data()
        self.fourth_view.update_label(data)

    def get_latest_record(self):
        data = self.model.get_latest_data()
        self.fourth_view.update_label(data)


# Main program
root = Tk()
root.geometry("700x600")
app = Controller(root)
root.mainloop() 
