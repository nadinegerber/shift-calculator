# ==============================================================================
# 4-DAY ON / 4-DAY OFF SHIFT SCHEDULE CALCULATOR
# ==============================================================================
# This script calculates a repeating 8-day shift cycle (4 work days followed
# by 4 off days) for any given date range, while handling vacation overrides.
# ==============================================================================

import calendar
import datetime


def is_date_in_vacation(target_date, vacation_ranges):
    """
    Checks if a specific target date falls within any defined vacation period.

    Parameters:
        target_date (datetime.date): The specific calendar date to check.
        vacation_ranges (list of tuples): A list containing (start_date, end_date)
                                         tuples representing approved leave.

    Returns:
        bool: True if target_date is inside a vacation range, False otherwise.
    """
    # Loop through each tuple in our list of vacation periods
    for start_date, end_date in vacation_ranges:
        # Check if target_date is on or between start_date and end_date
        if start_date <= target_date <= end_date:
            return True

    # If the date did not match any vacation period, return False
    return False


def get_shift_status(target_date, anchor_date, vacation_ranges):
    """
    The get_shift_status() function is designed to answer a single question: "What is the schedule status for this one specific date?" It cannot process multiple dates at once on its own.

    Determines whether a specific date is a Work Day, Off Day, or Vacation Day.

    Math Logic:
    1. Check if the target_date is inside a vacation range.
    2. Subtract anchor_date from target_date to get total elapsed days.
    3. Calculate (elapsed_days % 8) to determine position in the 8-day cycle:
       - Remainders 0, 1, 2, 3 = Work Day (Days 1 to 4)
       - Remainders 4, 5, 6, 7 = Off Day (Days 1 to 4)

    Parameters:
        target_date (datetime.date): The date to evaluate.
        anchor_date (datetime.date): Known starting date (Day 1 of Work).
        vacation_ranges (list): List of (start_date, end_date) tuples.

    Returns:
        dict: Information containing status string, cycle day number, and type.
    """
    # Priority Step: Check if this target date is an approved vacation/holiday
    if is_date_in_vacation(target_date, vacation_ranges):
        return {
            "status": "Vacation / Holiday",
            "cycle_day": "N/A",
            "is_work": False,
        }

    # Step 1: Calculate total number of days elapsed between anchor and target
    elapsed_days = (target_date - anchor_date).days

    # Step 2: Modulo arithmetic - divide total days by 8 and take the remainder
    cycle_index = elapsed_days % 8

    # Step 3: Map remainder index to shift position
    if cycle_index < 4:
        # Remainders 0, 1, 2, 3 correspond to Work Days 1, 2, 3, 4
        return {
            "status": f"Work Day (Day {cycle_index + 1} of 4)",
            "cycle_day": cycle_index + 1,
            "is_work": True,
        }
    else:
        # Remainders 4, 5, 6, 7 correspond to Off Days 1, 2, 3, 4
        return {
            "status": f"Off Day (Day {cycle_index - 3} of 4)",
            "cycle_day": cycle_index - 3,
            "is_work": False,
        }


def generate_monthly_schedule(year, month, anchor_date, vacation_ranges):
    """
    Generates a full month's shift schedule as a list of dictionary records.

    Parameters:
        year (int): Four-digit year (e.g., 2026).
        month (int): Month number (1 through 12).
        anchor_date (datetime.date): Shift start reference date.
        vacation_ranges (list): List of vacation tuple date ranges.

    Returns:
        list: Collection of dictionaries containing details for every day of the month.
    """
    # Get the total number of days in the specified month (handles leap years automatically)
    _, total_days_in_month = calendar.monthrange(year, month)

    monthly_records = []

    
# The for day in range(...) loop inside generate_monthly_schedule() acts as the engine that powers the program by calling get_shift_status() repeatedly for every day of the month and gathering all those individual outputs into one organized dataset.

    # Iterate through every day of the month from 1 to total_days_in_month
    for day in range(1, total_days_in_month + 1):
        current_date = datetime.date(year, month, day)

        # Query our calculation engine for this specific date
        shift_info = get_shift_status(
            target_date=current_date,
            anchor_date=anchor_date,
            vacation_ranges=vacation_ranges,
        )

        # Assemble detailed daily record
        day_record = {
            "date": current_date,
            "day_name": current_date.strftime("%A"),  # e.g., 'Monday'
            "status": shift_info["status"],
            "is_work": shift_info["is_work"],
        }

        monthly_records.append(day_record)

    return monthly_records


# ==============================================================================
# SCRIPT TESTING AND DEMONSTRATION
# ==============================================================================
if __name__ == "__main__":
    print("=========================================================")
    print("      TESTING SHIFT SCHEDULE CALCULATION ENGINE          ")
    print("=========================================================\n")

    # Step A: Define your reference anchor date (Day 1 of Work)
    # Example: Assume January 1st, 2026 was Day 1 of a 4-day work shift
    KNOWN_ANCHOR_DATE = datetime.date(2026, 1, 1)

    # Step B: Define vacation/holiday ranges (Start Date, End Date)
    # Example: A 1-week vacation from October 10th to October 17th, 2026
    SAMPLE_VACATIONS = [
        (datetime.date(2026, 10, 10), datetime.date(2026, 10, 17)),
    ]

    # Step C: Target year and month to display
    TEST_YEAR = 2026
    TEST_MONTH = 10  # October

    print(f"[*] Anchor Date Set: {KNOWN_ANCHOR_DATE} (Day 1 of Work)")
    print(
        f"[*] Vacation Period: {SAMPLE_VACATIONS[0][0]} to {SAMPLE_VACATIONS[0][1]}"
    )
    print(f"[*] Generating schedule for: {TEST_YEAR}-{TEST_MONTH:02d}\n")

    # Step D: Run monthly calculation function
    month_schedule = generate_monthly_schedule(
        year=TEST_YEAR,
        month=TEST_MONTH,
        anchor_date=KNOWN_ANCHOR_DATE,
        vacation_ranges=SAMPLE_VACATIONS,
    )

    # Step E: Print formatted schedule to terminal
    print(f"{'DATE':<12} | {'DAY':<10} | {'SCHEDULE STATUS'}")
    print("-" * 50)

    for record in month_schedule:
        date_str = record["date"].strftime("%Y-%m-%d")
        day_name = record["day_name"]
        status = record["status"]

        # Visual indicator for terminal output
        if "Work Day" in status:
            tag = "[WORK]"
        elif "Vacation" in status:
            tag = "[VACATION]"
        else:
            tag = "[OFF]"

        print(f"{date_str:<12} | {day_name:<10} | {tag:<10} {status}")

    print("\n[+] Calculation engine test executed successfully!")