from datetime import datetime, date
from typing import List, Dict

def get_entries_by_date_range(
    journal_entries: List[Dict], start_date: str, end_date: str
) -> List[Dict]:
    """
    Filters a list of journal entries to return only those within a specified date range.

    Args:
        journal_entries: A list of journal entry dictionaries.
        start_date: The start date of the range (inclusive), in 'yyyy-mm-dd' format.
        end_date: The end date of the range (inclusive), in 'yyyy-mm-dd' format.

    Returns:
        A list of journal entry dictionaries within the specified date range.
    """
    if not journal_entries:
        return []

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Invalid date format. Dates must be in 'yyyy-mm-dd' format.")
        return []

    filtered_entries = []
    for entry in journal_entries:
        try:
            entry_date_str = entry.get("date")
            if entry_date_str: #check for existence of date
                entry_date_obj = datetime.strptime(entry_date_str, "%Y-%m-%d").date()
                if start_date_obj <= entry_date_obj <= end_date_obj:
                    filtered_entries.append(entry)
            else:
                print(f"Warning: missing date in entry: {entry}")

        except (ValueError, TypeError):
            print(f"Warning: Invalid date format or missing date in entry: {entry}")

    return filtered_entries
