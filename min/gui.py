import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import sys

class URLValidatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Validator")
        self.root.geometry("600x500")

        # Input file
        tk.Label(root, text="Input Excel File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.select_input_file).grid(row=0, column=2, padx=10, pady=5)

        # Output file
        tk.Label(root, text="Output File:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.insert(0, "validated_urls.xlsx")
        self.output_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.select_output_file).grid(row=1, column=2, padx=10, pady=5)

        # Concurrency
        tk.Label(root, text="Max Concurrency:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.concurrency_entry = tk.Entry(root, width=50)
        self.concurrency_entry.insert(0, "10")
        self.concurrency_entry.grid(row=2, column=1, padx=10, pady=5)

        # Rate limit
        tk.Label(root, text="Rate Limit (seconds):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.rate_limit_entry = tk.Entry(root, width=50)
        self.rate_limit_entry.insert(0, "0.1")
        self.rate_limit_entry.grid(row=3, column=1, padx=10, pady=5)

        # Run button
        self.run_button = tk.Button(root, text="Validate URLs", command=self.run_validation)
        self.run_button.grid(row=4, column=0, columnspan=3, pady=20)

        # Output text area
        tk.Label(root, text="Output:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.output_text = scrolledtext.ScrolledText(root, width=70, height=15)
        self.output_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def run_validation(self):
        input_file = self.input_entry.get()
        output = self.output_entry.get()
        concurrency = self.concurrency_entry.get()
        rate_limit = self.rate_limit_entry.get()

        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return

        # Build command
        cmd = [
            sys.executable, "url_validator.py", input_file,
            "--output", output,
            "--concurrency", concurrency,
            "--rate_limit", rate_limit
        ]

        self.run_button.config(state="disabled")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Starting validation...\n")

        # Run in thread to avoid blocking GUI
        thread = threading.Thread(target=self.execute_command, args=(cmd,))
        thread.start()

    def execute_command(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
            self.output_text.insert(tk.END, result.stdout)
            if result.stderr:
                self.output_text.insert(tk.END, "Errors:\n" + result.stderr)
            self.output_text.insert(tk.END, "\nValidation complete.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error running command: {e}\n")
        finally:
            self.run_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = URLValidatorGUI(root)
    root.mainloop()