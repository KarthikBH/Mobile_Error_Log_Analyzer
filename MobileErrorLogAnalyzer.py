import os
import re
import subprocess
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from time import sleep

img_edit = None
helper = ""

# OPEN FILE PROMPT
def file_open():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    img_edit.delete("1.0", tk.END)

    openedfile = open(filepath, "r")
    contents = openedfile.read()
    openedfile.close()
    contents = contents.split("\n")
    for content in contents:
        img_edit.insert(tk.END, content)
        img_edit.insert(tk.END, "\n")

    btn_analyze.config(state = "active")
    btn_save.config(state="active")

# New FILE PROMPT
def file_new():
    clear()
    btn_analyze.config(state = "disabled")
    btn_save.config(state="disabled")
    btn_stop.config(state="disabled")
    btn_start.config(state="active")

# CLEAR ALL TEXT
def clear():
    img_edit.delete("1.0", tk.END)

# SAVE FILE PROMPT
def save():
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = img_edit.get("1.0", tk.END)
        output_file.write(text)

    messagebox.showinfo(title="Saved", message="Saved at " + filepath )

# START ADB LOGS
def start():
    adb_output = subprocess.check_output(["adb", "devices"])
    output = str(adb_output).split('\\n')
    if ("List of devices attached" in output[0]) and ("device" in output[1] or "emulator" in output[1]):
        img_edit.delete("1.0", tk.END)
        img_edit.insert(tk.END, "Device detected.\nClick Stop after reproducing issue")
        img_edit.insert(tk.END, "\n")

        btn_start.config(state="disabled")
        btn_stop.config(state = "active")

        subprocess.check_output(["adb", "logcat", "-c"])
    else:
        img_edit.delete("1.0", tk.END)
        img_edit.insert(tk.END, "No Device detected.\nCheck if device is properly connected and USB debugging turned ON")
        img_edit.insert(tk.END, "\n")

# STOP ADB LOGS
def stop():

    btn_stop.config(state="disabled")
    btn_start.config(state="active")
    btn_analyze.config(state="active")
    btn_save.config(state="active")

    if os.path.exists("logcat.txt"):
        os.remove('logcat.txt')

    subprocess.call(["adb", "logcat", "-d", ">", "logcat.txt"], shell=True)
    sleep(2)

    img_edit.delete("1.0", tk.END)

    openedfile = open("logcat.txt", "r")
    contents = openedfile.read()
    openedfile.close()
    contents = contents.split("\n")
    for content in contents:
        img_edit.insert(tk.END, content)
        img_edit.insert(tk.END, "\n")

# FILTER ADB LOGS
def analyze():
    img_edit.delete("1.0", tk.END)

    # OPEN LOG FILE
    logFile1 = open("logcat.txt", "r")
    logFile = logFile1.read()

    my_list = []

    # FIND ERRORS IN LOG FILE AND TAKE ABOVE AND BELOW DATA
    logFile = logFile.split("\n")
    for l in range(len(logFile)):
        if " E " in logFile[l]:
            for x in range(5, -1, -1):
                if not l - x == l:
                    my_list.append(logFile[l - x])
            my_list.append((logFile[l]))
            for x in range(1, 5):
                if not l - x == 0:
                    my_list.append(logFile[l + x])

    # REMOVE DUPLICATES CAUSED BY ABOVE FILTERING
    my_list = list(dict.fromkeys(my_list))

    # REMOVE TIME AND DATE OF LOGS FOR FILTERING PURPOSE
    # WILL ADD AGAIN LATER
    second_list = []
    for l in range(len(my_list)):
        try:
            res = re.search(r'[A-Z]', my_list[l])
            digit = res.group(0)
            res = my_list[l].partition(digit)[2]
            second_list.append(digit + res)
        except AttributeError:
            pass

    # COUNT THE OCCURRENCE OF LOGS (CHECK FOR REPETITIONS)
    from collections import Counter
    third_list = dict(Counter(second_list))

    for key, value in dict.items(third_list):
        for a in third_list:
            if key in a:
                res = re.search(r'[A-Z]', a)
                digit = res.group(0)

    for l in range(len(third_list)):
        for key, value in dict.items(third_list):
            if key in second_list[l]:
                res = re.search(r'[A-Z]', second_list[l])
                digit = res.group(0)
                res = second_list[l].partition(digit)[0]

                img_edit.insert(tk.END, res + str(key) + "  Repetitions : " + str(value))
                img_edit.insert(tk.END, "\n")

    # ADD DATE , TIME , LOG DATA AND NUMBER OF REPETITIONS
    for l in range(len(second_list)):
        for key, value in dict.items(third_list):
            if key in second_list[l]:
                res = re.search(r'[A-Z]', second_list[l])
                digit = res.group(0)

                img_edit.insert(tk.END, second_list[l] + str(key) + "  Repetitions : " + str(value))
                img_edit.insert(tk.END, "\n")

    logFile1.close()

def onclosing():
    if os.path.exists("logcat.txt"):
        os.remove("logcat.txt")
    window.destroy()

#SHOW HOW TO USE AT START
if os.path.exists("Help.txt"):
    openedfile = open("Help.txt", "r")
    contents = openedfile.read()
    openedfile.close()
    contents = contents.split("\n")
    for content in contents:
        helper += content
        helper += '\n'

####
# UI
####
window = tk.Tk()
window.title("Mobile Error Log Analyzer")
window.resizable(0,0)
if os.path.exists("icon.ico"):
    window.iconbitmap('icon.ico')

menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=False)
filemenu.add_command(label="New", command=file_new)
filemenu.add_command(label="Open", command=file_open)
filemenu.add_command(label="Quit", command=window.quit)
menubar.add_cascade(label="Options", menu=filemenu)
fr_header = tk.Frame(window, bg = "#5a5a5e")
fr_header.grid(row=0, column=0, sticky = 'nsew')

fr_header = tk.Frame(window, bg = "#5a5a5e")
labelTitle = tk.Label(fr_header, bg = "#5a5a5e", fg = "#edd06f", text = "Mobile Error Log Analyzer", font = "Helvetica 18 bold italic")
labelTitle.grid(row=0, column=1, sticky="ew", padx=20, pady=5)
fr_header.grid(row=0, column=1, sticky = 'nsew')

fr_top = tk.Frame(window, bg = "#5a5a5e")
btn_start = tk.Button(fr_top, text="Start", bg = "#62db2e",width = 8,font = "Helvetica 14 italic", activebackground = "black", activeforeground = "#62db2e", command = start)
btn_stop = tk.Button(fr_top, text="Stop", bg = '#db5c2e',width = 8, font = "Helvetica 14 italic", activebackground = "black", activeforeground = "#db5c2e", state = "disabled", command = stop)
btn_analyze = tk.Button(fr_top, text="Analyze", bg = "#f2b263",width = 8, font = "Helvetica 14 italic", activebackground = "black", activeforeground = "#f2b263", state = "disabled", command = analyze)
btn_save = tk.Button(fr_top, text="Save", bg = "#2e51db",width = 8, font = "Helvetica 14 italic", activebackground = "black", activeforeground = "#2e51db", state = "disabled", command = save)
btn_clear = tk.Button(fr_top, text="Clear", bg = "#ab8d2b",width = 8, font = "Helvetica 14 italic", activebackground = "black", activeforeground = "#ab8d2b", command = clear)
btn_start.grid(row=2, column=0, sticky="ns", ipadx = 30, padx=5 , pady=20)
btn_stop.grid(row=3, column=0, sticky="ns", ipadx = 30, padx=5, pady=20)
btn_analyze.grid(row=4, column=0, sticky="ns", ipadx = 30, padx=5, pady=20)
btn_save.grid(row=5, column=0, sticky="ns", ipadx = 30, padx=5, pady=20)
btn_clear.grid(row=6, column=0, sticky="ns", ipadx = 30, padx=5, pady=20)
fr_top.grid(row=1, column=0, sticky="nsew")

fr_bottom = tk.Frame(window, bg = "black", padx = 5, pady=5)
img_edit = tk.Text(fr_bottom)
img_edit.grid(row=0, column=1, sticky="nsew")
scroll_bar = tk.Scrollbar(fr_bottom, bg = "black")
scroll_bar.grid(row=0, column=2, sticky="nsew")
fr_bottom.grid(row=1, column=1, sticky="nsew")
scroll_bar.config(command=img_edit.yview, width = 20)
img_edit.config(yscrollcommand = scroll_bar.set)
img_edit.insert(tk.END, helper)
window.protocol("WM_DELETE_WINDOW", onclosing)
window.config(menu=menubar)
window.mainloop()