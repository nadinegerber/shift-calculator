# ==============================================================================
# 4-DAY ON / 4-DAY OFF SHIFT SCHEDULE CALCULATOR
# ==============================================================================
# This script calculates a repeating 8-day shift cycle (4 work days followed
# by 4 off days) for any given date range, while handling vacation overrides
# and ensuring workers always return on Work Day 1 after a vacation.
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
    Determines whether a specific date is a Work Day, Off Day, or Vacation Day.

    Enhanced Logic for Vacations:
    1. If the target date is during a vacation, it returns vacation status.
    2. For any date after a vacation, it calculates a timeline offset so that
       the day immediately following the vacation end date always aligns to
       Work Day 1 (cycle index 0).
    """
    # Priority Step 1: Check if this target date is an approved vacation/holiday
    if is_date_in_vacation(target_date, vacation_ranges):
        return {
            "status": "Vacation / Holiday",
            "cycle_day": "N/A",
            "is_work": False,
        }

    # Step 2: Calculate baseline total number of days elapsed between anchor and target
    raw_elapsed_days = (target_date - anchor_date).days

    # Step 3: Calculate cumulative timeline offset caused by past vacations.
    # We sort vacations chronologically to process them in the order they occurred.
    total_offset = 0
    if vacation_ranges:
        sorted_vacations = sorted(vacation_ranges, key=lambda x: x[0])

        for vac_start, vac_end in sorted_vacations:
            # If the vacation ended before our target date, it shifts all subsequent dates
            if target_date > vac_end:
                # The return day is the day immediately following the vacation end date
                return_date = vac_end + datetime.timedelta(days=1)

                # Calculate what the raw elapsed days would be on that return date without prior offsets
                raw_at_return = (return_date - anchor_date).days - total_offset
                remainder_at_return = raw_at_return % 8

                # If the return day does not land on Work Day 1 (remainder 0),
                # we add an offset to force it to align perfectly to remainder 0.
                if remainder_at_return != 0:
                    total_offset += remainder_at_return

    # Step 4: Apply the vacation offset to get the final adjusted elapsed days
    adjusted_elapsed_days = raw_elapsed_days - total_offset
    cycle_index = adjusted_elapsed_days % 8

    # Step 5: Map the adjusted remainder index to shift position
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
    print("    TESTING SHIFT SCHEDULE CALCULATION ENGINE          ")
    print("=========================================================\n")

    KNOWN_ANCHOR_DATE = datetime.date(2026, 10, 13)
    SAMPLE_VACATIONS = [
        (datetime.date(2026, 10, 17), datetime.date(2026, 10, 24)),
    ]

    TEST_YEAR = 2026
    TEST_MONTH = 10  # October

    month_schedule = generate_monthly_schedule(
        year=TEST_YEAR,
        month=TEST_MONTH,
        anchor_date=KNOWN_ANCHOR_DATE,
        vacation_ranges=SAMPLE_VACATIONS,
    )

    print(f"{'DATE':<12} | {'DAY':<10} | {'SCHEDULE STATUS'}")
    print("-" * 50)

    for record in month_schedule:
        date_str = record["date"].strftime("%Y-%m-%d")
        day_name = record["day_name"]
        status = record["status"]

        if "Work Day" in status:
            tag = "[WORK]"
        elif "Vacation" in status:
            tag = "[VACATION]"
        else:
            tag = "[OFF]"

        print(f"{date_str:<12} | {day_name:<10} | {tag:<10} {status}")

    print("\n[+] Calculation engine test executed successfully!")
