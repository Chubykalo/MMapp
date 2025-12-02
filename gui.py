import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from core.data_handling import load_matches_from_csv


class ScorecardGUI:
    def __init__(self):

        # Create the main window
        self.root = tk.Tk()
        self.root.title('MMA Scorecard Generator')
        self.root.geometry('800x600')

        self.fightcard_path = None # Store the CSV path
        # self.output_dir = os.path.join(os.getcwd(), "output") # Store output directory
        self.matches = [] # Store loaded match data

        # Build the GUI
        self.create_widgets()


    def create_widgets(self):
        
        ##### Top frame section #####

        # Create a frame for the top section
        top_frame = tk.Frame(self.root, bg='lightgray', padx=10, pady=10)
        top_frame.pack(fill='x') # fill='x' means to stretch horizontally
        top_frame.columnconfigure(1, weight=1)

        # Event name row
        tk.Label(top_frame, text='Event Name', bg='lightgray').grid(row=0, column=0, sticky='w', padx=5)
        self.event_entry = tk.Entry(top_frame)
        self.event_entry.grid(row=0, column=1, sticky='we', padx=5)

        # Import fightcard row
        tk.Label(top_frame, text='Import Fightcard:', bg='lightgray').grid(row=1, column=0, sticky='w', padx=5)
        self.fightcard_entry = tk.Entry(top_frame)
        self.fightcard_entry.grid(row=1, column=1, sticky='we', padx=5)
        tk.Button(top_frame, text='Browse', command=self.browse_fightcard).grid(row=1,column=2, padx=5)

        # # Set output directory
        # tk.Label(top_frame, text='Output Directory', bg='lightgray').grid(row=2, column=0, sticky='w', padx=5)
        # self.output_dir_entry = tk.Entry(top_frame)
        # self.output_dir_entry.insert(0, self.output_dir) # Set the default directory as a pre-selected text
        # self.output_dir_entry.grid(row=2, column=1, sticky='we', padx=5)
        # tk.Button(top_frame, text='Browse', command=self.browse_output_dir).grid(row=2,column=2, padx=5)

        ##### Middle frame section #####

        # Create a frame for the middle section
        middle_frame = tk.Frame(self.root, padx=10, pady=10)
        middle_frame.pack(fill='both', expand=True)

        tk.Label(middle_frame, text='Match List Preview', font=('Arial', 10, 'bold')).pack(anchor='w')

        # Create treeview Table
        columns = ('match', 'blue', 'red')
        self.match_table = ttk.Treeview(middle_frame, columns=columns, show='headings', height=10)

        # Define column headings
        self.match_table.heading('match', text='Match #')
        self.match_table.heading('blue', text='Blue Athlete')
        self.match_table.heading('red', text='Red Athlete')

        # Define column widths
        self.match_table.column('match', width=80)
        self.match_table.column('blue', width=200)
        self.match_table.column('red', width=200)

        self.match_table.pack(fill='both', expand=True)


    def browse_fightcard(self):
        """ Open file dialog to select CSV and load the data"""

        filename = filedialog.askopenfilename(
            title = "Select Fightcard CSV",
            filetypes = [("CSV files", "*.csv")]
        )
        if filename:
            self.fightcard_path = filename
            self.fightcard_entry.delete(0, tk.END) # Clear the entry first
            self.fightcard_entry.insert(0, filename) # Show the path

            # Load and display matches
            self.load_and_display_matches()
        

    def load_and_display_matches(self):
        """Load matches from CSV and populate the table"""
        # Clear existing table
        for item in self.match_table.get_children():
            self.match_table.delete(item)

        # Load matches from CSV
        self.matches = load_matches_from_csv(self.fightcard_path)

        # Populate table with match data
        for match_num, blue, red in self.matches:
            self.match_table.insert('', 'end', values=(match_num, blue, red))

    # def browse_output_dir(self):
    #     directory = filedialog.askdirectory(
    #         title = "Select Output directory"
    #     )

    #     if directory:
    #         self.output_dir = directory
    #         self.output_dir_entry.delete(0, tk.END) # Clear the entry first
    #         self.output_dir_entry.insert(0, directory) # Show the path


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScorecardGUI()
    app.run()
