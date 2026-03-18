import requests
import tkinter as tk
from tkinter import scrolledtext, filedialog
import webbrowser
import threading
import time

last_result = ""
last_lat = None
last_lon = None

# ---------------- FUNCTIONS ---------------- #

def get_my_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        entry.delete(0, tk.END)
        entry.insert(0, ip)
    except:
        output.insert(tk.END, "⚠️ Error getting your IP\n")


def copy_result():
    app.clipboard_clear()
    app.clipboard_append(output.get(1.0, tk.END))


def clear_output():
    output.delete(1.0, tk.END)


def save_results():
    global last_result
    file = filedialog.asksaveasfile(defaultextension=".txt",
                                   filetypes=[("Text files", "*.txt")])
    if file:
        file.write(last_result)
        file.close()


def open_map():
    if last_lat and last_lon:
        url = f"https://www.google.com/maps?q={last_lat},{last_lon}"
        webbrowser.open(url)
    else:
        output.insert(tk.END, "\n⚠️ No location data.\n")


def loading_animation():
    output.delete(1.0, tk.END)

    steps = [
        "Initializing system...",
        "Connecting to global nodes...",
        "Bypassing firewalls...",
        "Decrypting packets...",
        "Accessing database...",
        "Fetching target data..."
    ]

    for step in steps:
        output.insert(tk.END, step + "\n")
        output.update()
        time.sleep(0.4)

    output.insert(tk.END, "\n✔ Access Granted\n\n")
    output.update()
    time.sleep(0.3)


def threaded_check():
    threading.Thread(target=run_check).start()


def run_check():
    loading_animation()
    get_ip_info()


def get_ip_info():
    global last_result, last_lat, last_lon

    ip = entry.get()
    url = f"http://ip-api.com/json/{ip}?fields=66846719"

    try:
        res = requests.get(url)
        data = res.json()

        if data["status"] == "success":

            last_lat = data.get("lat")
            last_lon = data.get("lon")

            last_result = f"""
==============================
      IP CHECKER - HysooZ
==============================
IP: {data.get('query')}
Hostname: {data.get('reverse')}

Country: {data.get('country')} ({data.get('countryCode')})
Region: {data.get('regionName')}
City: {data.get('city')}
ZIP: {data.get('zip')}

ISP: {data.get('isp')}
Org: {data.get('org')}

Timezone: {data.get('timezone')}

Location:
  Lat: {last_lat}
  Lon: {last_lon}

Security:
  Proxy: {data.get('proxy')}
  Hosting: {data.get('hosting')}
  Mobile: {data.get('mobile')}
==============================
"""

            output.delete(1.0, tk.END)
            output.insert(tk.END, last_result)

        else:
            output.insert(tk.END, "❌ Invalid IP or not found.")

    except Exception as e:
        output.insert(tk.END, f"⚠️ Error: {e}")


# ---------------- UI ---------------- #

app = tk.Tk()
app.title("IP Checker - HysooZ")
app.geometry("750x600")
app.configure(bg="black")

# Title
title = tk.Label(app, text="IP CHECKER", font=("Courier", 24, "bold"),
                 fg="#00ff00", bg="black")
title.pack(pady=10)

subtitle = tk.Label(app, text="by HysooZ", font=("Courier", 10),
                    fg="#00ff00", bg="black")
subtitle.pack()

# Entry
entry = tk.Entry(app, font=("Courier", 14), width=40,
                 bg="black", fg="#00ff00", insertbackground="#00ff00")
entry.pack(pady=10)

# Buttons
frame = tk.Frame(app, bg="black")
frame.pack(pady=5)

buttons = [
    ("CHECK", threaded_check),
    ("MY IP", get_my_ip),
    ("OPEN MAP", open_map),
    ("SAVE", save_results),
    ("COPY", copy_result),
    ("CLEAR", clear_output),
]

for i, (text, cmd) in enumerate(buttons):
    tk.Button(frame, text=text, command=cmd,
              font=("Courier", 10, "bold"),
              bg="#00ff00", fg="black").grid(row=0, column=i, padx=5)

# Output
output = scrolledtext.ScrolledText(app, width=85, height=25,
                                   bg="black", fg="#00ff00",
                                   font=("Courier", 10))
output.pack(pady=10)

app.mainloop()