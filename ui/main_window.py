import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from core.data_handling import load_matches_from_csv
from .dialogs import EditMatchDialog


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
        tk.Label(top_frame, text='Event Name', bg='lightgray').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.event_entry = tk.Entry(top_frame)
        self.event_entry.grid(row=0, column=1, sticky='we', padx=5)

        # Import fightcard row
        tk.Label(top_frame, text='Import Fightcard:', bg='lightgray').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.fightcard_entry = tk.Entry(top_frame)
        self.fightcard_entry.grid(row=1, column=1, sticky='we', padx=5)
        tk.Button(top_frame, text='Browse', command=self.browse_fightcard).grid(row=1,column=2, padx=5)

        # Add Match field
        tk.Label(top_frame, text='Add New Match', bg='lightgray').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        
        self.add_match_entry = tk.Entry(top_frame, width=10)
        self.add_match_entry.grid(row=2, column=1, sticky='w', padx=5)
        self.add_match_entry.insert(0, 'Match #')
        self.add_match_entry.config(fg='gray')

        self.add_blue_entry = tk.Entry(top_frame, width=40)    
        self.add_blue_entry.grid(row=2, column=1, sticky='w', padx=(95,5))
        self.add_blue_entry.insert(0, 'Blue Athlete')
        self.add_blue_entry.config(fg='gray')

        self.add_red_entry = tk.Entry(top_frame, width=40)
        self.add_red_entry.grid(row=2, column=1, sticky='w', padx=(365,5))
        self.add_red_entry.insert(0, 'Red Athlete')
        self.add_red_entry.config(fg='gray')

        self.add_button = tk.Button(top_frame, text='ADD', command=self.add_match)
        self.add_button.grid(row=2, column=2, padx=5)
        

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

        # Edit Selected Match button
        tk.Button(button_frame, text='Edit Selected Match', command=self.edit_match).pack(side='left', padx=5)

        # Remove Selected Match button
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
        """Add a new match to the table and match list """
        # Get values from entry fields
        match_text = self.add_match_entry.get()
        blue_text = self.add_blue_entry.get()
        red_text = self.add_red_entry.get()

        match_placeholder = self.placeholders[self.add_match_entry]
        blue_placeholder =self.placeholders[self.add_blue_entry]
        red_placeholder = self.placeholders[self.add_red_entry]

        # Compare placeholders and assign values
        if match_text == match_placeholder:
            match_value = ""
        else:
            match_value = match_text

        if blue_text == blue_placeholder:
            blue_value = ""
        else:
            blue_value = blue_text

        if red_text == red_placeholder:
            red_value = ""
        else:
            red_value = red_text

        # Check if match_value is empty so we don't add fully empty matches
        if match_value == blue_value == red_value == "":
            return

        # Add to list
        self.matches.append((match_value, blue_value, red_value))

        # Add to table
        self.match_table.insert('', 'end', values=(match_value, blue_value, red_value))

        # Clear empty fields and restore placeholders
        for entry in self.placeholders.keys():
            entry.delete(0, tk.END)
            entry.insert(0, self.placeholders[entry])
            entry.config(fg='gray')
        
        # Set focus to the Add button after clicking on it
        self.add_button.focus_set()

    def edit_match(self):
        """Edit selected match from list."""
        # Check if a row is selected
        selected = self.match_table.selection()

        if not selected:
            return

        # Get the indexes
        item_data = self.match_table.item(selected[0])
        row_index = self.match_table.index(selected[0])

        # Get the current values from that row  
        current_match, current_blue, current_red = item_data['values']
 
        # Show dialog with current values pre-filled
        dialog = EditMatchDialog(self.root, current_match, current_blue, current_red)
        
        # Save the new values 
        if dialog.result: # User edits and clicks save
            new_match, new_blue, new_red = dialog.result
            self.matches[row_index] = (new_match, new_blue, new_red) # Updating the match list with new values
            self.match_table.item(selected[0], values = (new_match, new_blue, new_red))


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
