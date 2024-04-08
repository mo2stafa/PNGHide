import tkinter.messagebox
import customtkinter
import pyperclip
from main import embed, extract

from tkinter import filedialog
from functools import partial

class GraphicalUserInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.controller = None

        self.configure_window()

        self.create_tabview()
        self.set_embedding_tab()
        self.set_extracting_tab()

    def configure_window(self):
        self.title("PNGHide")
        self.geometry(f"{500}x{250}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_tabview(self):
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, rowspan=3, padx=(0, 0), pady=(10, 0), sticky="nsew")
        self.tabview.add("Embed")
        self.tabview.add("Extract")
        self.tabview.tab("Embed").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Extract").grid_columnconfigure(0, weight=1)

    def set_embedding_tab(self):
        self.embedding_input_file_selection_button = customtkinter.CTkButton(self.tabview.tab("Embed"), text="Select input file",
                                                                      command=self.embedding_input_action)
        self.embedding_input_file_selection_button.grid(row=0, column=0, padx=(0, 250), pady=(10, 10))

        self.embedding_output_file_selection_button = customtkinter.CTkButton(self.tabview.tab("Embed"), text="Select output file",
                                                                      command=self.embedding_output_action)
        self.embedding_output_file_selection_button.grid(row=1, column=0, padx=(0, 250), pady=(10, 10))

        self.embedding_to_embed_file_selection_button = customtkinter.CTkButton(self.tabview.tab("Embed"), text="Select file to embed",
                                                                      command=self.embedding_to_embed_action)
        self.embedding_to_embed_file_selection_button.grid(row=0, column=0, padx=(250, 0), pady=(10, 10))

        self.embed_button = customtkinter.CTkButton(self.tabview.tab("Embed"), text="Embed",
                                                             command=self.attempt_Embed)
        self.embed_button.grid(row=2, column=0, padx=(150, 150), pady=(10, 10))

    def set_extracting_tab(self):
        self.extracting_input_file_selection_button = customtkinter.CTkButton(self.tabview.tab("Extract"), text="Select input file",
                                                                      command=self.extracting_input_action)
        self.extracting_input_file_selection_button.grid(row=0, column=0, padx=(0, 250), pady=(10, 10))

        self.extracting_output_file_selection_button = customtkinter.CTkButton(self.tabview.tab("Extract"), text="Select output file",
                                                                      command=self.extracting_output_action)
        self.extracting_output_file_selection_button.grid(row=0, column=0, padx=(250, 0), pady=(10, 10))

        self.extract_button = customtkinter.CTkButton(self.tabview.tab("Extract"), text="Extract",
                                                             command=self.attempt_Extract)
        self.extract_button.grid(row=2, column=0, padx=(150, 150), pady=(10, 10))

    def embedding_input_action(self):
        self.embedding_input_filename = filedialog.askopenfilename()

    def embedding_output_action(self):
        self.embedding_output_filename = filedialog.asksaveasfilename(defaultextension=".png")

    def embedding_to_embed_action(self):
        self.embedding_to_embed_filename = filedialog.askopenfilename()

    def extracting_input_action(self):
        self.extracting_input_filename = filedialog.askopenfilename()

    def extracting_output_action(self):
        self.extracting_output_filename = filedialog.asksaveasfilename(defaultextension=".txt")

    def attempt_Embed(self):
        try:
            embed(self.embedding_input_filename, self.embedding_output_filename, self.embedding_to_embed_filename)
            tkinter.messagebox.showinfo("Embedding", "Embedding completed successfully!")
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Embedding failed: {str(e)}")

    def attempt_Extract(self):
        try:
            extract(self.extracting_input_filename, self.extracting_output_filename)
            tkinter.messagebox.showinfo("Extraction", "Extraction completed successfully!")
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Extraction failed: {str(e)}")

if __name__ == "__main__":
    gui = GraphicalUserInterface()
    gui.mainloop()
