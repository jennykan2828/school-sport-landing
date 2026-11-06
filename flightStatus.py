import requests
from datetime import date, timedelta
from prettytable import PrettyTable
from art import text2art
from pprint import pprint


def get_hko_flights(
    target_date: str, arrival: bool = False, cargo: bool = False, lang: str = "en"
):
    """Fetch flights from Hong Kong Airport open data API"""
    base_url = "https://www.hongkongairport.com/flightinfo-rest/rest/flights/past"

    params = {
        "date": target_date,
        "arrival": str(arrival).lower(),
        "cargo": str(cargo).lower(),
        "lang": lang,
    }

    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Find the matching day
        for day in data:
            if day.get("date") == target_date:
                return day.get("list", [])
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []


def filter_flights(flights, keyword: str, is_arrival: bool):
    """Filter by destination (departure) or origin (arrival)"""
    keyword = keyword.upper().strip()
    results = []

    for f in flights:
        # For departures → look in "destination"
        # For arrivals   → look in "origin"
        places = f.get("destination" if not is_arrival else "origin", [])
        places_str = " ".join(places).upper()

        if keyword in places_str:
            results.append(f)

    return results


def display_flights(flights, target_date, is_arrival, keyword):
    """Pretty table + art"""
    print("\n" + text2art("HK Flights", font="small"))
    print(f"📅 Date        : {target_date}")
    print(f"🛫 Type        : {'Arrival' if is_arrival else 'Departure'}")
    print(f"🔍 Filter      : {keyword.upper()}")
    print(f"✅ Found       : {len(flights)} flight(s)\n")

    if not flights:
        print("😢 No matching flights found.")
        return

    table = PrettyTable()
    table.field_names = [
        "Time",
        "Flight No.",
        "Airline",
        "Destination/Origin",
        "Terminal",
        "Gate",
        "Status",
    ]
    table.align = "l"

    for f in flights:
        # Flight numbers (can be codeshare)
        flight_nos = " / ".join([fl["no"] for fl in f.get("flight", [])])
        airlines = " / ".join([fl["airline"] for fl in f.get("flight", [])])

        place = ", ".join(f.get("destination" if not is_arrival else "origin", []))

        table.add_row(
            [
                f.get("time", "-"),
                flight_nos,
                airlines,
                place,
                f.get("terminal", "-"),
                f.get("gate", "-"),
                f.get("status", "-"),
            ]
        )

    print(table)


def main():
    print(text2art("HK Airport", font="small"))
    print("=== Hong Kong International Airport Flight Finder ===\n")

    # --- User Input ---
    target_date = input("Enter date (YYYY-MM-DD) [default = yesterday]: ").strip()
    if not target_date:
        target_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    direction = input("Arrival or Departure? (a/d) [default = d]: ").strip().lower()
    is_arrival = direction in ("a", "arrival", "arr")

    keyword = input(
        "Enter destination / origin code or city (e.g. TPE, Tokyo, ICN): "
    ).strip()
    if not keyword:
        print("❌ You must enter a destination/origin.")
        return

    print("\n⏳ Searching...\n")

    # --- Fetch & Filter ---
    flights = get_hko_flights(target_date, arrival=is_arrival, cargo=False)
    matched = filter_flights(flights, keyword, is_arrival)

    # --- Display ---
    display_flights(matched, target_date, is_arrival, keyword)


if __name__ == "__main__":
    main()
