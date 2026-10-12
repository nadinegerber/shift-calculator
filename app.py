# ==============================================================================
# 4-DAY ON / 4-DAY OFF SHIFT SCHEDULE WEB APPLICATION (STREAMLIT)
# ==============================================================================
# This application integrates our Stage 1 mathematical calculation engine
# with Streamlit's visual web framework to present an interactive shift dashboard.
# ==============================================================================

import calendar
import datetime
import pandas as pd
import streamlit as st

# ------------------------------------------------------------------------------
# SECTION 1: PAGE CONFIGURATION
# ------------------------------------------------------------------------------
# How: st.set_page_config() configures browser-level settings.
# Where: Placed at the very top of the script before any visual elements.
# Why: Streamlit requires page layout settings (title, wide screen mode)
# to be established before it renders text or tables in the browser window.
st.set_page_config(
    page_title="Shift Schedule Dashboard", page_icon="📅", layout="wide"
)


# ------------------------------------------------------------------------------
# SECTION 2: CORE CALCULATION ENGINE (STAGE 1 CODE REUSED)
# ------------------------------------------------------------------------------
def is_date_in_vacation(target_date, vacation_ranges):
    """
    Checks if a target date falls inside any active vacation start/end range.

    Parameters:
        target_date (datetime.date): The specific date being evaluated.
        vacation_ranges (list of tuples): Approved leave start and end dates.

    Returns:
        bool: True if the date falls within any vacation range, otherwise False.
    """
    # Iterate through each tuple in the vacation list
    for start_date, end_date in vacation_ranges:
        # Check if target date is on or between the vacation bounds
        if start_date <= target_date <= end_date:
            return True
    return False


def get_shift_status(target_date, anchor_date, vacation_ranges):
    """
    Determines work, off, or vacation status using (elapsed_days % 8) modulo arithmetic.

    Parameters:
        target_date (datetime.date): The date to evaluate.
        anchor_date (datetime.date): Reference starting date (Work Day 1).
        vacation_ranges (list): List of vacation tuple date ranges.

    Returns:
        dict: Contains status description, cycle day number, work flag, and visual badge.
    """
    # Priority check: If the date is a vacation day, return vacation details immediately
    if is_date_in_vacation(target_date, vacation_ranges):
        return {
            "status": "Vacation / Holiday",
            "cycle_day": "N/A",
            "is_work": False,
            "badge": "🌴 Vacation",
        }

    # Calculate raw elapsed days from the anchor date
    elapsed_days = (target_date - anchor_date).days

    # Apply modulo 8 arithmetic to find position in the repeating shift cycle
    cycle_index = elapsed_days % 8

    # Map remainder index to work or off status
    if cycle_index < 4:
        return {
            "status": f"Work Day (Day {cycle_index + 1} of 4)",
            "cycle_day": cycle_index + 1,
            "is_work": True,
            "badge": "💼 Work Day",
        }
    else:
        return {
            "status": f"Off Day (Day {cycle_index - 3} of 4)",
            "cycle_day": cycle_index - 3,
            "is_work": False,
            "badge": "🏠 Off Day",
        }


def generate_monthly_schedule(year, month, anchor_date, vacation_ranges):
    """
    Loops through every day of the requested month and builds an array of
    formatted dictionaries optimized for Streamlit table display.

    Parameters:
        year (int): Four-digit target year.
        month (int): Numeric target month (1 to 12).
        anchor_date (datetime.date): Shift start reference date.
        vacation_ranges (list): List of vacation date tuples.

    Returns:
        list: Collection of dictionaries containing daily schedule records.
    """
    # Retrieve total days in the specified month (automatically handles leap years)
    _, total_days_in_month = calendar.monthrange(year, month)
    monthly_records = []

    # Iterate through each day of the month sequentially
    for day in range(1, total_days_in_month + 1):
        current_date = datetime.date(year, month, day)

        # Query calculation engine for current date status
        shift_info = get_shift_status(
            target_date=current_date,
            anchor_date=anchor_date,
            vacation_ranges=vacation_ranges,
        )

        # Append formatted dictionary record to list with capitalized headers
        monthly_records.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Day Name": current_date.strftime("%A"),
            "Status": shift_info["badge"],
            "Shift Detail": shift_info["status"],
        })

    return monthly_records


# ------------------------------------------------------------------------------
# SECTION 3: STREAMLIT SIDEBAR INPUT CONTROLS
# ------------------------------------------------------------------------------
# How: st.sidebar creates a collapsible settings panel on the left side of the screen.
# Where: Located on the left screen margin.
# Why: Moving controls to the sidebar prevents inputs from cluttering the main screen.

st.sidebar.header("⚙️ Schedule Settings")

# Sidebar Control 1: Anchor Date Selector (Set to October 13, 2026 based on brother's shift)
default_anchor = datetime.date(2026, 10, 13)
anchor_date = st.sidebar.date_input(
    label="Anchor Date (Work Day 1):",
    value=default_anchor,
    help="Select a known historical date that was Day 1 of a 4-day work shift.",
)

st.sidebar.markdown("---")
st.sidebar.header("🌴 Vacation Settings")

# Sidebar Control 2: Vacation Toggle & Date Range Selectors
enable_vacation = st.sidebar.checkbox("Enable Vacation Period", value=False)

vacation_ranges = []
if enable_vacation:
    vac_start = st.sidebar.date_input(
        "Vacation Start Date", datetime.date(2026, 10, 17)
    )
    vac_end = st.sidebar.date_input(
        "Vacation End Date", datetime.date(2026, 10, 24)
    )

    # Validation check: Ensure start date precedes or equals end date
    if vac_start <= vac_end:
        vacation_ranges.append((vac_start, vac_end))
    else:
        st.sidebar.error("Error: Start date must come before end date.")

st.sidebar.markdown("---")

# Sidebar Control 3: View Selector (Year and Month Dropdown)
st.sidebar.header("🗓️ Viewing Period")
selected_year = st.sidebar.number_input(
    "Year", min_value=2020, max_value=2035, value=2026, step=1
)

# Convert numeric months (1-12) to text names ("January", "October") for user selection
selected_month = st.sidebar.selectbox(
    "Month",
    options=list(range(1, 13)),
    format_func=lambda m: datetime.date(2000, m, 1).strftime("%B"),
    index=9,  # Default selection set to October (index 9 = 10th month)
)


# ------------------------------------------------------------------------------
# SECTION 4: MAIN DASHBOARD DISPLAY
# ------------------------------------------------------------------------------
# Main Page Header
st.title("📅 4-On / 4-Off Shift Schedule Dashboard")
st.caption(
    "Interactive schedule viewer for 4 days on, 4 days off shift cycles."
)
st.markdown("---")

# Execute calculation engine using inputs selected in the sidebar
schedule_data = generate_monthly_schedule(
    year=selected_year,
    month=selected_month,
    anchor_date=anchor_date,
    vacation_ranges=vacation_ranges,
)

# Display High-Level Summary Metrics
# How: st.columns(3) splits the main display into 3 side-by-side metric cards.
# Why: Gives immediate total counts of work, off, and vacation days for the month.
col1, col2, col3 = st.columns(3)

work_days_count = sum(
    1 for row in schedule_data if "Work Day" in row["Status"]
)
off_days_count = sum(1 for row in schedule_data if "Off Day" in row["Status"])
vacation_days_count = sum(
    1 for row in schedule_data if "Vacation" in row["Status"]
)

col1.metric(label="Total Work Days", value=f"{work_days_count} Days")
col2.metric(label="Total Off Days", value=f"{off_days_count} Days")
col3.metric(label="Vacation Days", value=f"{vacation_days_count} Days")

st.markdown("---")

# Render Monthly Table Header
month_name = datetime.date(2000, selected_month, 1).strftime("%B")
st.subheader(f"Schedule for {month_name} {selected_year}")

# How: We convert our list of Python dictionaries into a Pandas DataFrame
# and assign the "Date" column as the table index using .set_index("Date").
# Why: This completely removes the default numeric index column (0, 1, 2...)
# and places the Date column at the very front of the display table.
df_schedule = pd.DataFrame(schedule_data).set_index("Date")

# Render the modified table in the web application interface
st.table(df_schedule)
