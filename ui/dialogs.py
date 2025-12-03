import tkinter as tk

class EditMatchDialog:
    def __init__(self, parent, current_match, current_blue, current_red):
        """
        Create an edit dialog pre-filled with current values.
        
        Args:
            parent: The parent window
            current_match: Current match number
            current_blue: Current blue athlete name
            current_red: Current red athlete name
        """

        self.result = None

        # Create the dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit MAtch")
        self.dialog.geometry("600x120")

        # Create input frame
        input_frame = tk.Frame(self.dialog)
        input_frame.pack(padx=10, pady=20)

        # Match number row
        self.match_entry = tk.Entry(input_frame, width=10)
        self.match_entry.grid(row=0, column=0, padx=5)
        self.match_entry.insert(0, current_match)
        tk.Label(input_frame, text="Match #", fg='gray').grid(row=1, column=0)

        # Blue fighter row
        self.blue_entry = tk.Entry(input_frame, width=20)
        self.blue_entry.grid(row=0, column=1, padx=5)
        self.blue_entry.insert(0, current_blue)
        tk.Label(input_frame, text="Blue Athlete", fg='gray').grid(row=1, column=1)

        # Red fighter row
        self.red_entry = tk.Entry(input_frame, width=20)
        self.red_entry.grid(row=0, column=2, padx=5)
        self.red_entry.insert(0, current_red)
        tk.Label(input_frame, text="Red Athlete", fg='gray').grid(row=1, column=2)

        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Save", command=self.save).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='left',padx=5)

        # Make dialog modal (blocks interaction with parent window)
        self.dialog.transient(parent) # Makes dialog stay on top of parent window
        self.dialog.grab_set() # Makes dialog "modal". It must be dealt with before returning to the main window
        parent.wait_window(self.dialog) # Pauses the code and waits until the dialog is closed

    def save(self):
        """User clicks Save -> store edited values """
        self.result = (
            self.match_entry.get(),
            self.blue_entry.get(),
            self.red_entry.get()
        )
        self.dialog.destroy()

    def cancel(self):
        """User clicks Cancel -> return None"""
        self.result = None
        self.dialog.destroy()
