"""
Date parsing and formatting utilities

Handles natural language date parsing and human-readable formatting (FR-019 to FR-024).
"""

from datetime import date, datetime, timedelta
from typing import Optional
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta


def parse_due_date(user_input: str) -> Optional[date]:
    """
    Parse various date formats into date object

    Supports:
    - ISO format: "2025-12-25"
    - Natural language: "Dec 25, 2025", "December 25"
    - Relative: "+3d" (3 days from now), "+2w" (2 weeks)
    - Keywords: "today", "tomorrow", "yesterday"

    Args:
        user_input: User-provided date string

    Returns:
        Parsed date object, or None if parsing fails

    Examples:
        >>> parse_due_date("2025-12-25")
        date(2025, 12, 25)
        >>> parse_due_date("tomorrow")
        date(2025, 12, 10)  # If today is Dec 9
        >>> parse_due_date("+3d")
        date(2025, 12, 12)  # 3 days from Dec 9
    """
    if not user_input:
        return None

    user_input = user_input.strip().lower()

    # Handle keywords
    if user_input == 'today':
        return date.today()
    elif user_input == 'tomorrow':
        return date.today() + timedelta(days=1)
    elif user_input == 'yesterday':
        return date.today() - timedelta(days=1)

    # Handle relative dates (+3d, +2w, +1m, +1y)
    if user_input.startswith('+') or user_input.startswith('-'):
        try:
            return parse_relative_date(user_input)
        except ValueError:
            pass

    # Parse natural language and ISO dates
    try:
        parsed = date_parser.parse(user_input)
        return parsed.date()
    except (ValueError, date_parser.ParserError):
        return None


def parse_relative_date(relative_str: str) -> date:
    """
    Parse relative date string like "+3d", "-2w", "+1m"

    Args:
        relative_str: Relative date string (e.g., "+3d", "-2w")

    Returns:
        Calculated date

    Raises:
        ValueError: If format is invalid

    Examples:
        >>> parse_relative_date("+3d")
        date(2025, 12, 12)
        >>> parse_relative_date("-1w")
        date(2025, 12, 2)
    """
    if not relative_str or relative_str[0] not in ('+', '-'):
        raise ValueError("Relative date must start with + or -")

    sign = 1 if relative_str[0] == '+' else -1
    value_str = relative_str[1:-1]
    unit = relative_str[-1].lower()

    try:
        value = int(value_str) * sign
    except ValueError:
        raise ValueError(f"Invalid number: {value_str}")

    today = date.today()

    if unit == 'd':  # days
        return today + timedelta(days=value)
    elif unit == 'w':  # weeks
        return today + timedelta(weeks=value)
    elif unit == 'm':  # months
        return today + relativedelta(months=value)
    elif unit == 'y':  # years
        return today + relativedelta(years=value)
    else:
        raise ValueError(f"Invalid unit: {unit} (use d/w/m/y)")


def format_relative_date(due: Optional[date], format_str: str = "%Y-%m-%d") -> str:
    """
    Format date relative to today (FR-020)

    Displays human-readable relative dates when close to today,
    otherwise uses configured format.

    Args:
        due: Due date to format
        format_str: Date format string (default ISO format)

    Returns:
        Formatted date string

    Examples:
        >>> format_relative_date(date.today())
        "Today"
        >>> format_relative_date(date.today() + timedelta(days=1))
        "Tomorrow"
        >>> format_relative_date(date.today() - timedelta(days=1))
        "Yesterday"
        >>> format_relative_date(date.today() - timedelta(days=3))
        "3d ago"
        >>> format_relative_date(date.today() + timedelta(days=10))
        "2025-12-19"
    """
    if due is None:
        return "No date"

    today = date.today()
    delta = (due - today).days

    if delta == 0:
        return "Today"
    elif delta == 1:
        return "Tomorrow"
    elif delta == -1:
        return "Yesterday"
    elif delta < -1:
        return f"{abs(delta)}d ago"
    elif delta < 7:
        # Show day of week for next few days
        return due.strftime("%A")  # "Monday", "Tuesday", etc.
    else:
        # Use configured format for distant dates
        return due.strftime(format_str)


def calculate_days_overdue(due: date) -> int:
    """
    Calculate how many days a task is overdue (FR-021)

    Args:
        due: Due date

    Returns:
        Number of days overdue (positive = overdue, negative = future, 0 = today)

    Examples:
        >>> calculate_days_overdue(date.today() - timedelta(days=3))
        3  # 3 days overdue
        >>> calculate_days_overdue(date.today() + timedelta(days=2))
        -2  # Due in 2 days
    """
    today = date.today()
    delta = (today - due).days
    return delta


def is_overdue(due: Optional[date]) -> bool:
    """
    Check if a task is overdue

    Args:
        due: Due date

    Returns:
        True if task is overdue (past due and not completed)
    """
    if due is None:
        return False
    return due < date.today()


def get_week_dates(start_date: Optional[date] = None) -> list[date]:
    """
    Get list of dates for a week (7 days)

    Args:
        start_date: Starting date (default: today)

    Returns:
        List of 7 date objects
    """
    if start_date is None:
        start_date = date.today()

    return [start_date + timedelta(days=i) for i in range(7)]


def get_month_dates(year: int, month: int) -> list[date]:
    """
    Get all dates in a month

    Args:
        year: Year
        month: Month (1-12)

    Returns:
        List of date objects for the month
    """
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    dates = []
    current = first_day
    while current <= last_day:
        dates.append(current)
        current += timedelta(days=1)

    return dates


def group_by_date_bucket(due: Optional[date]) -> str:
    """
    Group date into bucket for calendar view (FR-020)

    Buckets:
    - "Overdue": Past due
    - "Today": Today
    - "Tomorrow": Tomorrow
    - "Next 7 days": Within next week
    - "Later": Beyond next week

    Args:
        due: Due date

    Returns:
        Bucket name
    """
    if due is None:
        return "No Date"

    today = date.today()
    delta = (due - today).days

    if delta < 0:
        return "Overdue"
    elif delta == 0:
        return "Today"
    elif delta == 1:
        return "Tomorrow"
    elif delta <= 7:
        return "Next 7 days"
    else:
        return "Later"


def format_datetime(dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M") -> str:
    """
    Format datetime with fallback for None

    Args:
        dt: Datetime to format
        format_str: Format string

    Returns:
        Formatted datetime string, or "N/A" if None
    """
    if dt is None:
        return "N/A"
    return dt.strftime(format_str)


__all__ = [
    "parse_due_date",
    "parse_relative_date",
    "format_relative_date",
    "calculate_days_overdue",
    "is_overdue",
    "get_week_dates",
    "get_month_dates",
    "group_by_date_bucket",
    "format_datetime",
]
