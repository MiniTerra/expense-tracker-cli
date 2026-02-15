# 💰 Expense Tracker CLI

A command-line expense tracker built with Python.

This project allows users to manage personal expenses directly from the terminal. Data is stored locally using JSON.

---

## 🚀 Features

- Add expenses
- Delete expenses
- Update existing expenses
- List all expenses
- Filter by category
- Sort by date or amount
- Calculate total spending
- Monthly summary
- Export data to CSV

---

## 🛠 Technologies Used

- Python 3
- argparse (CLI argument parsing)
- JSON (data persistence)
- CSV module (data exporting)

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/MiniTerra/expense-tracker-cli.git
cd expense-tracker-cli
```

Run the program:

```bash
python expense.py
```

---

## 📌 Example Usage

Add an expense:

```bash
python expense.py add 19.99 --category food --desc pizza
```

List expenses:

```bash
python expense.py list
```

Sort by amount:

```bash
python expense.py list --sort amount
```

Delete an expense:

```bash
python expense.py delete 2
```

Calculate total:

```bash
python expense.py total
```

Export to CSV:

```bash
python expense.py export
```

---

## 📚 Concepts Practiced

- File handling with JSON
- CLI application design
- CRUD operations
- Data filtering and sorting
- Aggregation logic
- Basic data export pipeline

---

## 🎯 Future Improvements

- Yearly summary
- Category-based analytics
- Data visualization with pandas
- Unit tests
- Packaging as installable CLI tool

---

## 👨‍💻 Author

Mini
