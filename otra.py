import tkinter as tk


def main() -> None:
    root = tk.Tk()
    root.title("Isaac")
    root.geometry("500x400")

    title = tk.Label(root, text="Isaac", font=("Helvetica", 24, "bold"))
    title.pack(pady=(30, 8))

    subtitle = tk.Label(root, text="LEC", font=("Helvetica", 14))
    subtitle.pack()

    welcome = tk.Label(root, text="BIENVENIDO", font=("Helvetica", 26, "bold"))
    welcome.pack(pady=(0, 30))
    welcome.pack_forget()

    def on_click() -> None:
        welcome.pack(pady=(0, 30))

    button = tk.Button(center_frame, text="Click",
                       command=on_click, font=("Helvetica", 14))
    button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
