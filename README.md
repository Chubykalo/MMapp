# MMApp - MMA Scorecard Generator

A Windows desktop application for generating PDF scorecards for MMA events.

## Features

- 📋 Import fightcard data from CSV files
- ✏️ Manually add, edit, and remove matches
- 🔢 Sort matches by number
- 📄 Generate professional PDF scorecards
- 🖥️ Standalone executable - no Python installation required!

## Download

**[Download Latest Release (v1.00)](https://github.com/Chubykalo/MMapp/releases/latest)**

Extract the zip file and run `MMApp.exe` - it's that simple!

## For Developers

### Requirements
- Python 3.10+
- See `requirements.txt` for dependencies

### Installation

1. Clone the repository:
```bash
   git clone https://github.com/Chubykalo/MMapp.git
   cd MMapp
```

2. Create a virtual environment and install dependencies:
```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
```

3. Run the application:
```bash
   python gui.py
```

### Building the Executable

To build a standalone .exe:
```bash
pyinstaller --clean gui.spec
```

The executable will be in the `dist/` folder.

## CSV Format

Your fightcard CSV should have three columns:
```csv
match_number,blue_fighter,red_fighter
1,Fighter A,Fighter B
2,Fighter C,Fighter D
```

## Project Structure
```
MMapp/
├── core/              # Core business logic
│   ├── data_handling.py
│   ├── pdf_generation.py
│   └── utils.py
├── ui/                # GUI components
│   ├── main_window.py
│   └── dialogs.py
├── assets/            # Template and resources
├── gui.py            # Application entry point
└── main.py           # CLI/programmatic interface
```

## License
   
   GPL v3 License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Feel free to open issues or submit pull requests.