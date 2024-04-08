import tkinter as tk
from tkinter import filedialog, messagebox
import argparse
import sys
from main import embed, extract


def embed_gui(root):
    input_file = filedialog.askopenfilename(title="Select input PNG file", filetypes=[("PNG files", "*.png")])
    output_file = filedialog.asksaveasfilename(title="Select output PNG file", defaultextension=".png", filetypes=[("PNG files", "*.png")])
    
    if input_file and output_file:
        file_to_embed = filedialog.askopenfilename(title="Select file to embed", defaultextension=[("PNG files", "*.png"), ("Text files", "*.txt")])
        
        if file_to_embed:
            try:
                embed(input_file, output_file, file_to_embed)
                messagebox.showinfo("Embedding Successful", "Data embedded successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))


def extract_gui():
    input_file = filedialog.askopenfilename(title="Select input PNG file", filetypes=[("PNG files", "*.png")])
    output_file = filedialog.asksaveasfilename(title="Select output file", defaultextension=".txt")

    if input_file and output_file:
        try:
            extract(input_file, output_file)
            messagebox.showinfo("Extraction Successful", "Data extracted successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def main():
    root = tk.Tk()
    root.title("PNG Processor GUI")

    embed_button = tk.Button(root, text="Embed Data", command=lambda: embed_gui(root))
    embed_button.pack(pady=10)

    extract_button = tk.Button(root, text="Extract Data", command=extract_gui)
    extract_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
