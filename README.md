# Python Learning Project

A comprehensive Python learning repository with practice exercises and a student management system.

## 📁 Project Structure

```
├── learning_basics/     # Learning scripts and exercises
├── src/                 # Project source code
│   ├── my_lib/         # Utility library helpers
│   └── student_management/  # Student management package
│       ├── __init__.py
│       ├── models.py    # Data models
│       ├── repository.py  # Data persistence (CSV)
│       ├── service.py     # Business logic
│       └── main.py        # CLI entry point
├── tests/               # Unit tests
├── docs/                # Documentation
├── data/                # CSV data files
├── bin/                 # Executable scripts
├── README.md            # This file
├── LICENSE
└── pyproject.toml       # Project configuration
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd python-learning-project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## 📚 Learning Basics

The `learning_basics/` directory contains fundamental Python exercises including:


| File | Topic |
|------|-------|
| `one.py`, `two.py` | Basic operations |
| `list_set_tuple.py` | Data structures |
| `day_7.py` | Day 7 exercises |
| `learn_decorators.py` | Python decorators |
| `example.py` | General examples |
| `file_handling.py` | File I/O operations |
| `calculator.py` | Calculator application |

### Mini Projects

| Project | Description |
|---------|-------------|
| `mini_project_1.py` | First mini project |
| `mini_project_2.py` | Second mini project |
| `mini_project_3.py` | Third mini project |

## 🎓 Student Management System

A full-featured student management application demonstrating OOP principles, layered architecture, and CSV-based data persistence.

### Features
- Add, update, delete students
- Track attendance
- Manage grades
- Search and filter students
- Export/import data

### Run the Application
```bash
python -m src.student_management.main
```

## 🧪 Running Tests

```bash
pytest tests/
```

## 📖 Documentation

Detailed documentation is available in the `docs/` directory.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Built as a Python learning resource.
