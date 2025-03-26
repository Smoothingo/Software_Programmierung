
import tkinter as tk
import customtkinter as ctk

class TextAdventureGUI:
    def __init__(self, master):
        root.resizable(False, False)
        root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
        self.master = master
        master.title("Text Adventure")

        self.text_area = ctk.CTkTextbox(master, width=400, height=200)
        self.text_area.pack(pady=10)

        self.entry = ctk.CTkEntry(master, width=300)
        self.entry.pack(pady=5)

        self.submit_button = ctk.CTkButton(master, text="Submit", command=self.submit_action)
        self.submit_button.pack(pady=5)

        self.buttons_frame = ctk.CTkFrame(master)
        self.buttons_frame.pack(pady=10)

        self.button1 = ctk.CTkButton(self.buttons_frame, text="Option 1", command=lambda: self.submit_action("Option 1"))
        self.button1.grid(row=0, column=0, padx=5, pady=5)

        self.button2 = ctk.CTkButton(self.buttons_frame, text="Option 2", command=lambda: self.submit_action("Option 2"))
        self.button2.grid(row=0, column=1, padx=5, pady=5)
        self.button3 = ctk.CTkButton(self.buttons_frame, text="Option 3", command=lambda: self.submit_action("Option 3"))
        self.button3.grid(row=0, column=2, padx=5, pady=5)

        self.button4 = ctk.CTkButton(self.buttons_frame, text="Option 4", command=lambda: self.submit_action("Option 4"))
        self.button4.grid(row=1, column=0, padx=5, pady=5)

        self.button5 = ctk.CTkButton(self.buttons_frame, text="Option 5", command=lambda: self.submit_action("Option 5"))
        self.button5.grid(row=1, column=1, padx=5, pady=5)


    def submit_action(self):
        action = self.entry.get()
        self.text_area.insert(tk.END, f"\nYou chose: {action}")
        self.entry.delete(0, tk.END)

root = ctk.CTk()
gui = TextAdventureGUI(root)
root.mainloop()

