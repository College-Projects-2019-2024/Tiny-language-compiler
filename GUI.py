from tkinter import *
from tkinter import filedialog
from Scanner import Scanner

root = Tk()

root.title('Tiny Language Compiler')

file_frame = LabelFrame(root, text="Open your file:", padx=20, pady=25)
file_frame.grid(row=0, column=0)

file_field = Text(file_frame, width=60, height=20)
file_field.insert(END, "Please Load File")
file_field.grid(row=0, column=0, columnspan=10, pady=10)

filepath = StringVar


def open_file():
    global filepath
    filepath = filedialog.askopenfilename(title="Select A File", filetypes=(("text files", "*.txt"),))
    if filepath:
        global file_opened
        file_opened = True
        with open(filepath, 'r') as file:
            file_content = file.read()
            file_field.delete("1.0", END)
            file_field.insert(END, file_content)



file_opened = False
file_button = Button(file_frame, text="Open File", command=open_file, width=68)
file_button.grid(row=1, column=0)

options_frame = LabelFrame(root, text="OPTIONS:", padx=20, pady=20)
options_frame.grid(row=0, column=1)

output_text = Text(options_frame, width=60, height=20)
output_text.insert(END, "Output")
output_text.config(state="disabled")
output_text.grid(row=0, column=0, columnspan=3, pady=5)


def scan():
    global filepath
    obj = Scanner()
    obj.tokenize(filepath)
    obj.export()
    f = open("output.txt", "r", encoding='utf-8').read()
    output_text.config(state="normal")
    output_text.delete("1.0", END)
    output_text.insert(END, f)
    output_text.config(state="disabled")


error_button = Button(options_frame, text="Show Errors", pady=10, padx=20, width=15)
error_button.grid(row=7, column=0, padx=4)

scan_button = Button(options_frame, text="SCAN", pady=10, padx=20, width=15, command=scan)
scan_button.grid(row=7, column=1, padx=4)

parse_button = Button(options_frame, text="PARSE", pady=10, padx=20, width=15)
parse_button.grid(row=7, column=2, padx=4)

root.mainloop()
