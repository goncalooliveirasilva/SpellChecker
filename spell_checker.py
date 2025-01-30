import tkinter as tk
from bloom_filter import BloomFilter
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file(window, text):
    file_path = askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    text.delete(1.0, tk.END)
    with open(file_path, "r") as f:
        content = f.read()
        text.insert(tk.END, content)
    window.title(f"{file_path}")


def save_file(window, text):
    file_path = asksaveasfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    with open(file_path, "w") as f:
        content = text.get(1.0, tk.END)
        f.write(content)
    window.title(f"{file_path}")
    

def main():
    window = tk.Tk()
    window.title("Bloom Filter Spell Checker")
    window.geometry("600x500")

    text = tk.Text(window, font="Arial 15")
    text.grid(row=0, column=0, pady=10, sticky="nsew")

    buttons = tk.Frame(window, bd=3)
    save_button = tk.Button(buttons, text="Save", command=lambda: save_file(window, text))
    open_button = tk.Button(buttons, text="Open", command=lambda: open_file(window, text))
    save_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    open_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    buttons.grid(row=1, column=0, sticky="ns")


    window.bind("<Control-s>", lambda x: save_file(window, text))
    window.bind("<Control-o>", lambda x: open_file(window, text))
    window.mainloop()


if __name__ == "__main__":
    main()