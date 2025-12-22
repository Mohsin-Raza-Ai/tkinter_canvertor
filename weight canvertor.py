import tkinter as tk
from tkinter import ttk

CONVERSION_RATES = {
    "Kilogram (kg)": 1,
    "Gram (g)": 1000,
    "Ounce (oz)": 35.274,
    "Pound (lb)": 2.20462,
    "Metric Ton (t)": 0.001,
    "Stone (st)": 0.157473,
    "Milligram (mg)": 1_000_000
}

class WeightConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Weight Converter")
        self.root.geometry("700x550")
        self.root.configure(bg="#1e1e2f")

        self.history = []
        self.history_visible = False

        self.create_ui()
        self.bind_keys()

    def create_ui(self):
        tk.Label(
            self.root, text="🌈 Weight Converter",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f", fg="#00ffd5"
        ).pack(pady=10)

        # Input
        tk.Label(self.root, text="Enter Value",
                 bg="#1e1e2f", fg="white").pack()
        self.entry = tk.Entry(self.root, font=("Arial", 12))
        self.entry.pack()

        tk.Label(self.root, text="Input Unit",
                 bg="#1e1e2f", fg="white").pack(pady=5)
        self.input_unit = ttk.Combobox(
            self.root, values=list(CONVERSION_RATES.keys()),
            state="readonly"
        )
        self.input_unit.set("Kilogram (kg)")
        self.input_unit.pack()

        # Output selection
        tk.Label(self.root, text="Select Output Units",
                 bg="#1e1e2f", fg="white").pack(pady=5)

        self.vars = {}
        unit_frame = tk.Frame(self.root, bg="#1e1e2f")
        unit_frame.pack()

        for unit in CONVERSION_RATES:
            var = tk.BooleanVar()
            tk.Checkbutton(
                unit_frame, text=unit,
                variable=var,
                bg="#1e1e2f", fg="#ffda79",
                selectcolor="#333"
            ).pack(anchor="w")
            self.vars[unit] = var

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Convert",
                  bg="#00c853", fg="white",
                  command=self.convert).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text="Clear",
                  bg="#d50000", fg="white",
                  command=self.clear).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text="History",
                  bg="#2962ff", fg="white",
                  command=self.toggle_history).grid(row=0, column=2, padx=5)

        # Results
        tk.Label(self.root, text="Results",
                 bg="#1e1e2f", fg="white").pack()
        self.result_box = tk.Text(
            self.root, height=7,
            bg="#121212", fg="#00e5ff"
        )
        self.result_box.pack(pady=5)

        # History (Hidden by default)
        self.history_frame = tk.Frame(self.root, bg="#1e1e2f")

        tk.Label(self.history_frame, text="Conversion History",
                 bg="#1e1e2f", fg="#ff9100").pack()

        self.history_box = tk.Text(
            self.history_frame, height=6,
            bg="#121212", fg="#76ff03"
        )
        self.history_box.pack()

    def convert(self):
        self.result_box.delete("1.0", tk.END)

        try:
            value = float(self.entry.get())
            if value < 0:
                return
        except:
            return

        input_unit = self.input_unit.get()
        value_kg = value / CONVERSION_RATES[input_unit]

        history_text = f"{value} {input_unit}\n"

        for unit, var in self.vars.items():
            if var.get():  # ✅ sirf selected units
                result = value_kg * CONVERSION_RATES[unit]
                self.result_box.insert(tk.END, f"{unit}: {result:.4f}\n")
                history_text += f"{unit}: {result:.4f}, "

        if history_text.strip() != "":
            self.history.append(history_text)
            self.update_history()

    def clear(self):
        self.entry.delete(0, tk.END)
        self.result_box.delete("1.0", tk.END)
        for var in self.vars.values():
            var.set(False)

    def toggle_history(self):
        if self.history_visible:
            self.history_frame.pack_forget()
        else:
            self.history_frame.pack(pady=10)
        self.history_visible = not self.history_visible

    def update_history(self):
        self.history_box.delete("1.0", tk.END)
        for item in self.history[-5:]:
            self.history_box.insert(tk.END, item + "\n\n")

    def bind_keys(self):
        self.root.bind("<Return>", lambda e: self.convert())
        self.root.bind("<Escape>", lambda e: self.clear())


if __name__ == "__main__":
    root = tk.Tk()
    WeightConverter(root)
    root.mainloop()
