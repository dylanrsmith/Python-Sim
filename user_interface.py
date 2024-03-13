import tkinter as tk
from fluid_fill_client_1 import *

def run_command():
    # Implement what happens when RUN is clicked
    live_values_text.insert(tk.END, "Run clicked\n")
    debug_comments_text.insert(tk.END, "Execute run command...\n")
    web_port = web_port_entry.get()
    hostname = ip_address_entry.get()
    recipe = recipe_input_entry.get()
    fill_ports = fill_port_entry.get()
    
    

def clear_fields():
    # Clear all fields and textboxes
    web_port_entry.delete(0, tk.END)
    ip_address_entry.delete(0, tk.END)
    recipe_input_entry.delete(0, tk.END)
    fill_port_entry.delete(0, tk.END)
    live_values_text.delete('1.0', tk.END)
    debug_comments_text.delete('1.0', tk.END)

# Create the main window
root = tk.Tk()
icon = tk.PhotoImage(file="img/fei_icon.png")
root.iconphoto(True,icon)
root.title("Test Client - Fluid Fill")

# Configure the grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(5, weight=1)

# First row
tk.Label(root, text="Web Port").grid(row=0, column=0, padx=10, pady=10, sticky="w")
web_port_entry = tk.Entry(root)
web_port_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="IP Address").grid(row=0, column=2, padx=10, pady=10, sticky="w")
ip_address_entry = tk.Entry(root)
ip_address_entry.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

# Second row
tk.Label(root, text="Recipe Input").grid(row=1, column=0, padx=10, pady=10, sticky="w")
recipe_input_entry = tk.Entry(root)
recipe_input_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

tk.Label(root, text="Fill Port").grid(row=1, column=2, padx=10, pady=10, sticky="w")
fill_port_entry = tk.Entry(root)
fill_port_entry.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

# Third row for buttons
frame_buttons = tk.Frame(root)
frame_buttons.grid(row=2, column=0, columnspan=4, pady=20)

run_button = tk.Button(frame_buttons, text="RUN", command=run_command)
run_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(frame_buttons, text="CLEAR", command=clear_fields)
clear_button.pack(side=tk.LEFT, padx=10)

# Textboxes for live values and debugging
live_values_text = tk.Text(root, height=10)
live_values_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

debug_comments_text = tk.Text(root, height=10)
debug_comments_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

# Start the GUI event loop
root.mainloop()
