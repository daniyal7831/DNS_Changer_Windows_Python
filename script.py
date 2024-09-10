import tkinter as tk
from tkinter import messagebox
import subprocess

def set_dns(primary_dns, secondary_dns):
    try:
        subprocess.run(f'netsh interface ip set dns "Wi-Fi" static {primary_dns}', shell=True, check=True)
        if secondary_dns:
            subprocess.run(f'netsh interface ip add dns "Wi-Fi" {secondary_dns} index=2', shell=True, check=True)
        messagebox.showinfo("Success", "DNS successfully set.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to set DNS.")

def reset_dns():
    try:
        subprocess.run(f'netsh interface ip set dns "Wi-Fi" dhcp', shell=True, check=True)
        messagebox.showinfo("Success", "DNS reset to automatic.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to reset DNS.")

def check_dns():
    try:
        result = subprocess.run('netsh interface ip show dns', shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to retrieve DNS information.")
        return ""

def update_dns_status():
    dns_status = check_dns()
    
    if "178.22.122.100" in dns_status and "185.51.200.2" in dns_status:
        status_label.config(text="Connected to: Shecan")
    elif "10.202.10.202" in dns_status and "10.202.10.102" in dns_status:
        status_label.config(text="Connected to: 403online")
    elif "DNS servers configured" in dns_status:
        status_label.config(text="Connected to: Unknown")
    else:
        status_label.config(text="Not connected to a specific DNS")

def on_connect():
    if dns_var.get() == 1:
        set_dns("178.22.122.100", "185.51.200.2")
    elif dns_var.get() == 2:
        set_dns("10.202.10.202", "10.202.10.102")

    update_dns_status()

def on_disconnect():
    reset_dns()
    update_dns_status()

def show_dns_info():
    dns_status = check_dns()
    
    dns_lines = [line for line in dns_status.splitlines() if "DNS" in line]
    
    if dns_lines:
        dns_info = "\n".join(dns_lines)
    else:
        dns_info = "No DNS information available"
    
    messagebox.showinfo("Current DNS Settings", dns_info)

root = tk.Tk()
root.title("DNS Manager")

dns_var = tk.IntVar()
tk.Radiobutton(root, text="Shecan", variable=dns_var, value=1).grid(row=0, column=0, sticky='w')
tk.Radiobutton(root, text="403online", variable=dns_var, value=2).grid(row=1, column=0, sticky='w')

status_label = tk.Label(root, text="Checking DNS status...")
status_label.grid(row=2, column=0, columnspan=2)

connect_button = tk.Button(root, text="Connect", command=on_connect)
connect_button.grid(row=3, column=0)

disconnect_button = tk.Button(root, text="Disconnect", command=on_disconnect)
disconnect_button.grid(row=3, column=1)

dns_info_button = tk.Button(root, text="Show DNS Info", command=show_dns_info)
dns_info_button.grid(row=4, column=0, columnspan=2)

update_dns_status()

root.mainloop()