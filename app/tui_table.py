"""Simple textual table editor TUI.

Usage: run from repository root:
    python app/tui_table.py [table_name]

Features:
- Loads a table from the DB using `DatabaseHandler.load_table(table_name)`
- Displays the table as plain text with row indices
- Allows editing a single cell by row index and column name
- Saves the whole table back with `DatabaseHandler.post_table`

Note: `post_table` replaces the table in the database (if_exists='replace').
"""
from __future__ import annotations
import sys
import os
from typing import Any

try:
    from src.utils.db.db_handling import DatabaseHandler
except Exception:
    # Fallback: try to import by adding project root to sys.path
    import os
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    from src.utils.db.db_handling import DatabaseHandler

import pandas as pd


def cast_value(old: Any, new_str: str) -> Any:
    """Try to cast new_str to the type of old value."""
    if pd.isna(old):
        # try to infer type
        for conv in (int, float):
            try:
                return conv(new_str)
            except Exception:
                continue
        if new_str.lower() in ("true", "false"):
            return new_str.lower() == "true"
        return new_str

    old_type = type(old)
    if old_type is bool:
        return new_str.lower() in ("1", "true", "yes", "y")
    if old_type is int:
        try:
            return int(new_str)
        except Exception:
            return new_str
    if old_type is float:
        try:
            return float(new_str)
        except Exception:
            return new_str
    return new_str


def show_table(df: pd.DataFrame, max_rows: int = 100) -> None:
    """Print the DataFrame to console with indices."""
    if df is None or df.empty:
        print("(empty table)")
        return
    with pd.option_context('display.max_rows', max_rows, 'display.max_columns', None):
        print(df.to_string(index=True))


def edit_cell_interactive(df: pd.DataFrame) -> pd.DataFrame:
    """Interactively edit a single cell in `df` and return modified df."""
    print("Columns:", ", ".join(df.columns.astype(str)))
    try:
        row_input = input("Enter row index to edit (the leftmost index shown): ").strip()
        if row_input == "":
            print("No row provided; aborting edit.")
            return df
        # try integer index first
        try:
            idx = int(row_input)
            if idx not in df.index:
                raise KeyError
            row_key = idx
        except Exception:
            # try as label
            if row_input in df.index:
                row_key = row_input
            else:
                print("Row not found.")
                return df

        col = input("Enter column name to edit: ").strip()
        if col not in df.columns:
            print("Unknown column")
            return df

        old_val = df.at[row_key, col]
        print(f"Old value: {old_val} (type: {type(old_val).__name__})")
        new_val_raw = input("New value: ").strip()
        new_val = cast_value(old_val, new_val_raw)
        df.at[row_key, col] = new_val
        print("Updated row:")
        print(df.loc[[row_key]].to_string())
        return df
    except KeyboardInterrupt:
        print("\nEdit cancelled")
        return df


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    table_name = argv[0] if argv else "etv_courses"

    # Determine DB URL: prefer environment, otherwise prompt or default to local sqlite
    db_url = os.getenv("DB_URL")
    if not db_url:
        print("No DB_URL environment variable found.")
        choice = input("Use local sqlite file 'etv_courses.db' in project root? (Y/n): ").strip().lower()
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if choice in ("", "y", "yes"):
            db_file = os.path.join(repo_root, "etv_courses.db")
            db_url = f"sqlite:///{db_file}"
            print(f"Using sqlite DB at: {db_file}")
        else:
            db_url = input("Enter DB URL (SQLAlchemy format), or leave empty to abort: ").strip()
            if not db_url:
                print("No DB URL provided — aborting.")
                return

    db = DatabaseHandler(db_url=db_url, table_name=table_name)

    while True:
        try:
            db.load_table(table_name)
            df = getattr(db, 'loaded_table', pd.DataFrame())
        except Exception as e:
            print(f"Error loading table '{table_name}': {e}")
            df = pd.DataFrame()

        print("\n--- Table Viewer/Editor ---")
        print(f"Loaded table: {table_name} (rows: {len(df)})")
        print("Commands: v=view, e=edit, s=save, r=refresh, q=quit, h=help")
        cmd = input("Command> ").strip().lower()

        if cmd in ("v", "view"):
            show_table(df)
        elif cmd in ("e", "edit"):
            df = edit_cell_interactive(df)
        elif cmd in ("s", "save"):
            confirm = input("Save current table back to DB? (yes/no): ").strip().lower()
            if confirm in ("y", "yes"):
                try:
                    db.post_table(df, table_name)
                    print("Table saved to DB.")
                except Exception as e:
                    print("Error saving table:", e)
        elif cmd in ("r", "refresh"):
            continue
        elif cmd in ("h", "help"):
            print("v/view - show table; e/edit - edit a cell; s/save - write table to DB; r/refresh - reload; q/quit")
        elif cmd in ("q", "quit"):
            print("Goodbye")
            break
        else:
            print("Unknown command. Type 'h' for help.")


if __name__ == "__main__":
    main()
