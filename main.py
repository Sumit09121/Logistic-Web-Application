print("Program started")
import tkinter as tk
from tkinter import messagebox
import os

FILE_NAME = "shipments.txt"


class LogisticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logistics Management System")
        self.root.geometry("520x460")
        self.root.configure(bg="#EAF2F8")

        # Header
        header = tk.Label(
            root,
            text="📦 Logistics Management System",
            font=("Helvetica", 18, "bold"),
            bg="#1F618D",
            fg="white",
            pady=10
        )
        header.pack(fill="x")

        # Main Frame
        self.frame = tk.Frame(root, bg="#EAF2F8")
        self.frame.pack(pady=15)

        # Shipment ID
        tk.Label(self.frame, text="Shipment ID", bg="#EAF2F8",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=20)
        self.entry_id = tk.Entry(self.frame, width=40, font=("Arial", 11))
        self.entry_id.pack(padx=20, pady=5)

        # Destination
        tk.Label(self.frame, text="Destination", bg="#EAF2F8",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=20)
        self.entry_destination = tk.Entry(self.frame, width=40, font=("Arial", 11))
        self.entry_destination.pack(padx=20, pady=5)

        # Status
        tk.Label(self.frame, text="Status", bg="#EAF2F8",
                 font=("Arial", 11, "bold")).pack(anchor="w", padx=20)
        self.entry_status = tk.Entry(self.frame, width=40, font=("Arial", 11))
        self.entry_status.pack(padx=20, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(root, bg="#EAF2F8")
        btn_frame.pack(pady=10)

        self.make_button(btn_frame, "Add Shipment", "#27AE60", self.add_shipment)
        self.make_button(btn_frame, "View Shipments", "#2980B9", self.view_shipments)
        self.make_button(btn_frame, "Update Status", "#F39C12", self.update_status)
        self.make_button(btn_frame, "Delete Shipment", "#C0392B", self.delete_shipment)

        # Output box
        self.output = tk.Text(root, height=7, width=60,
                              font=("Consolas", 10), bg="#FBFCFC")
        self.output.pack(pady=10)

    # -------- Button Creator --------
    def make_button(self, parent, text, color, command):
        tk.Button(
            parent,
            text=text,
            width=16,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold"),
            command=command,
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=5)

    # -------- Logic --------
    def add_shipment(self):
        sid = self.entry_id.get()
        dest = self.entry_destination.get()
        status = self.entry_status.get() or "Pending"

        if sid == "" or dest == "":
            messagebox.showerror("Error", "Shipment ID and Destination are required")
            return

        with open(FILE_NAME, "a") as file:
            file.write(f"{sid},{dest},{status}\n")

        messagebox.showinfo("Success", "Shipment added successfully")
        self.clear_fields()

    def view_shipments(self):
        self.output.delete(1.0, tk.END)

        if not os.path.exists(FILE_NAME):
            self.output.insert(tk.END, "No shipments found.")
            return

        with open(FILE_NAME, "r") as file:
            for line in file:
                self.output.insert(tk.END, line)

    def update_status(self):
        sid = self.entry_id.get()
        new_status = self.entry_status.get()

        if sid == "" or new_status == "":
            messagebox.showerror("Error", "Enter Shipment ID and Status")
            return

        if not os.path.exists(FILE_NAME):
            messagebox.showerror("Error", "No shipment data found")
            return

        updated = False

        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

        with open(FILE_NAME, "w") as file:
            for line in lines:
                parts = line.strip().split(",")
                if parts[0] == sid:
                    file.write(f"{parts[0]},{parts[1]},{new_status}\n")
                    updated = True
                else:
                    file.write(line)

        if updated:
            messagebox.showinfo("Success", "Shipment status updated")
        else:
            messagebox.showerror("Error", "Shipment not found")

    def delete_shipment(self):
        sid = self.entry_id.get()

        if sid == "":
            messagebox.showerror("Error", "Enter Shipment ID")
            return

        if not os.path.exists(FILE_NAME):
            messagebox.showerror("Error", "No shipment data found")
            return

        found = False

        with open(FILE_NAME, "r") as file:
            lines = file.readlines()

        with open(FILE_NAME, "w") as file:
            for line in lines:
                if not line.startswith(sid + ","):
                    file.write(line)
                else:
                    found = True

        if found:
            messagebox.showinfo("Success", "Shipment deleted successfully")
        else:
            messagebox.showerror("Error", "Shipment not found")

    def clear_fields(self):
        self.entry_id.delete(0, tk.END)
        self.entry_destination.delete(0, tk.END)
        self.entry_status.delete(0, tk.END)


# -------- RUN APP --------
root = tk.Tk()
app = LogisticsApp(root)
root.mainloop()
