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

        # Add Match field
        tk.Label(top_frame, text='Add New Match', bg='lightgray').grid(row=2, column=0, sticky='w', padx=5)
        
        self.add_match_entry = tk.Entry(top_frame, width=10)
        self.add_match_entry.grid(row=2, column=1, sticky='w', padx=5)
        self.add_match_entry.insert(0, 'Match #')
        self.add_match_entry.config(fg='gray')

        self.add_blue_entry = tk.Entry(top_frame, width=15)    
        self.add_blue_entry.grid(row=2, column=1, sticky='w', padx=(80,5))
        self.add_blue_entry.insert(0, 'Blue Athlete')
        self.add_blue_entry.config(fg='gray')

        self.add_red_entry = tk.Entry(top_frame, width=15)
        self.add_red_entry.grid(row=2, column=1, sticky='w', padx=(220,5))
        self.add_red_entry.insert(0, 'Red Athlete')
        self.add_red_entry.config(fg='gray')

        tk.Button(top_frame, text='ADD', command=self.add_match).grid(row=2, column=2, padx=5)

        # Store placeholder text for each entry
        self.placeholders = {
            self.add_match_entry: 'Match #',
            self.add_blue_entry: 'Blue Athlete',
            self.add_red_entry: 'Red Athlete'
        }

        # Bind focus events to all three entries
        for entry in self.placeholders.keys():
            entry.bind('<FocusIn>', self.entry_focus_in)
            entry.bind('<FocusOut>', self.entry_focus_out)

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


        ##### Button frame section #####


        # Button frame below table
        button_frame = tk.Frame(middle_frame)
        button_frame.pack(fill='x', pady=5)

        tk.Button(button_frame, text='Remove Selected Match', command=self.remove_match).pack(side='left', padx=5)


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


    def add_match(self):
        pass

    
    def remove_match(self):
        """Remove selected match from list."""
        selected = self.match_table.selection()

        if not selected:
            return

        row_index = self.match_table.index(selected[0]) 
        answer = messagebox.askyesno(title='confirmation', message='Are you sure you want to remove?')
        
        if answer:
           del self.matches[row_index] # delete row from matches list
           self.match_table.delete(selected[0]) # delete row from preview table


    def entry_focus_in(self, event):
        """Remove placeholder text when user clicks in the field."""
        widget = event.widget
        current_text = widget.get()
        placeholder = self.placeholders[widget]

        # Check if the text is gray (placeholder)
        # If yes, clear it and change color to black
        if current_text == placeholder:
            widget.delete(0, tk.END)
            widget.config(fg='black')

    
    def entry_focus_out(self, event):
        """Restore placeholder text if unfocused and the field is empty."""
        widget = event.widget
        current_text = widget.get()
        placeholder = self.placeholders[widget]

        # Check if the field is empty
        # if yes, restore the placeholder and make it gray
        if current_text == '':
            widget.insert(0, placeholder)
            widget.config(fg='gray')


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScorecardGUI()
    app.run()
