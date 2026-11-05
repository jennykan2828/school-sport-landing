from datetime import datetime, timedelta

def get_optimal_christmas_offset(christmas_date, public_holidays_set):
    """
    Dynamically determines whether leaning 'forward' or 'backward' 
    requires fewer annual leave requests for a 9-day holiday block.
    """
    best_offset = 0
    min_leave_days = 9  # Worst case scenario
    
    # We test every possible starting offset from 0 days to 8 days back
    for offset in range(9):
        start_date = christmas_date - timedelta(days=offset)
        leave_count = 0
        
        # Evaluate the 9-day block starting from this date
        for day_idx in range(9):
            current_day = start_date + timedelta(days=day_idx)
            is_weekend = current_day.weekday() in (5, 6)  # Sat, Sun
            is_ph = current_day in public_holidays_set
            
            if not is_weekend and not is_ph:
                leave_count += 1
                
        # We want the offset that minimizes leave. 
        # If tied, leaning forward (smaller offset from Dec 25) usually captures New Year.
        if leave_count <= min_leave_days:
            min_leave_days = leave_count
            best_offset = offset

    return best_offset


def plan_christmas_break(year):
    """
    Calculates, formats, and displays the optimal 9-day Christmas break itinerary
    for a given year, minimizing annual leave requirements.
    """
    christmas = datetime(year, 12, 25)

    # Map public holidays dynamically (New Year's Day belongs to year + 1)
    hong_kong_ph = {
        datetime(year, 12, 25),      # Christmas Day
        datetime(year, 12, 26),      # Day after Christmas / Boxing Day
        datetime(year + 1, 1, 1)     # New Year's Day (Following Year)
    }

    optimal_offset = get_optimal_christmas_offset(christmas, hong_kong_ph)
    print(f"\nOptimal shift back from Dec 25: {optimal_offset} days")

    start_date = christmas - timedelta(days=optimal_offset)
    holiday_days = [start_date + timedelta(days=i) for i in range(9)]

    # Public holiday and weekend checking formatting logic
    format_day = lambda dt: (
        dt.date().isoformat(),
        dt.strftime('%A'),
        "Public Holiday" if dt in hong_kong_ph else ("Weekend" if dt.weekday() in [5, 6] else "Leave Required")
    )

    print(f"\n--- Weekend-Optimized 9-Day Christmas Break for {year} ---")

    leave_count = 0
    for index, dt in enumerate(holiday_days, 1):
        iso_date, day_name, status = format_day(dt)
        
        if status == "Leave Required":
            leave_count += 1
            status_str = "💼 Leave Needed"
        elif status == "Public Holiday":
            status_str = "🎉 Public Holiday"
        else:
            status_str = "🏖️ Weekend"
            
        # Context markers
        marker = ""
        if dt.month == 12 and dt.day == 25:
            marker = " 🎄 [Christmas Day]"
        elif dt.month == 12 and dt.day == 26:
            marker = " 🎁 [Boxing Day]"
        elif dt.month == 1 and dt.day == 1:
            marker = " 🎆 [New Year's Day]"

        print(f"Day {index}: {iso_date} ({day_name:9}) -> {status_str}{marker}")
        
    print(f"\n🎯 Total annual leave days you need to request: {leave_count} days")


# --- Execution Block ---
if __name__ == "__main__":
    try:
        user_year = int(input("Enter the year (e.g., 2026): "))
    except ValueError:
        print("Invalid year. Using 2026 as default.")
        user_year = 2026

    plan_christmas_break(user_year)
