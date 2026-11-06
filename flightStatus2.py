import requests
from datetime import date, timedelta
from prettytable import PrettyTable
from art import text2art

# ============================================================
# City / Airport name → IATA code mapping
# (you can keep adding more)
# ============================================================
CITY_TO_CODES = {
    # Japan
    "tokyo": ["NRT", "HND"],
    "narita": ["NRT"],
    "haneda": ["HND"],
    "osaka": ["KIX", "ITM"],
    "kansai": ["KIX"],
    "nagoya": ["NGO"],
    "fukuoka": ["FUK"],
    "sapporo": ["CTS"],
    "okinawa": ["OKA"],
    "naha": ["OKA"],
    # Korea
    "seoul": ["ICN", "GMP"],
    "incheon": ["ICN"],
    "busan": ["PUS"],
    "jeju": ["CJU"],
    # Taiwan
    "taipei": ["TPE", "TSA"],
    "kaohsiung": ["KHH"],
    # China
    "beijing": ["PEK", "PKX"],
    "shanghai": ["PVG", "SHA"],
    "guangzhou": ["CAN"],
    "shenzhen": ["SZX"],
    "chengdu": ["CTU", "TFU"],
    "hangzhou": ["HGH"],
    "xiamen": ["XMN"],
    "kunming": ["KMG"],
    "xi'an": ["XIY"],
    "xian": ["XIY"],
    "chongqing": ["CKG"],
    "nanjing": ["NKG"],
    "wuhan": ["WUH"],
    "qingdao": ["TAO"],
    "dalian": ["DLC"],
    "harbin": ["HRB"],
    "tianjin": ["TSN"],
    "sanya": ["SYX"],
    "haikou": ["HAK"],
    # Southeast Asia
    "bangkok": ["BKK", "DMK"],
    "singapore": ["SIN"],
    "kuala lumpur": ["KUL"],
    "kl": ["KUL"],
    "manila": ["MNL"],
    "cebu": ["CEB"],
    "jakarta": ["CGK"],
    "denpasar": ["DPS"],
    "bali": ["DPS"],
    "ho chi minh": ["SGN"],
    "saigon": ["SGN"],
    "hanoi": ["HAN"],
    "phuket": ["HKT"],
    "chiang mai": ["CNX"],
    # Others
    "sydney": ["SYD"],
    "melbourne": ["MEL"],
    "brisbane": ["BNE"],
    "auckland": ["AKL"],
    "london": ["LHR", "LGW"],
    "paris": ["CDG"],
    "frankfurt": ["FRA"],
    "amsterdam": ["AMS"],
    "dubai": ["DXB"],
    "doha": ["DOH"],
    "abu dhabi": ["AUH"],
    "los angeles": ["LAX"],
    "san francisco": ["SFO"],
    "new york": ["JFK", "EWR"],
    "vancouver": ["YVR"],
    "toronto": ["YYZ"],
}


def resolve_codes(user_input: str) -> list[str]:
    """
    Convert natural language or code into a list of IATA codes.
    """
    text = user_input.strip().lower()

    # 1. Exact city name match
    if text in CITY_TO_CODES:
        return CITY_TO_CODES[text]

    # 2. Partial match (e.g. "tok" → Tokyo)
    for city, codes in CITY_TO_CODES.items():
        if text in city or city in text:
            return codes

    # 3. User already typed a code (NRT, HND, TPE...)
    code = user_input.strip().upper()
    if len(code) == 3 and code.isalpha():
        return [code]

    # 4. Nothing found
    return []


def get_hko_flights(
    target_date: str, arrival: bool = False, cargo: bool = False, lang: str = "en"
):
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

        for day in data:
            if day.get("date") == target_date:
                return day.get("list", [])
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return []


def filter_flights(flights, codes: list[str], is_arrival: bool):
    """Filter flights by a list of airport codes"""
    codes = [c.upper() for c in codes]
    results = []

    for f in flights:
        places = f.get("origin" if is_arrival else "destination", [])
        if any(code in places for code in codes):
            results.append(f)

    return results


def display_flights(flights, target_date, is_arrival, keyword, codes):
    print("\n" + text2art("HK Flights", font="small"))
    print(f"📅 Date          : {target_date}")
    print(f"🛫 Type          : {'Arrival' if is_arrival else 'Departure'}")
    print(f"🔍 You typed     : {keyword}")
    print(f"✈️  Searching codes: {', '.join(codes)}")
    print(f"✅ Found         : {len(flights)} flight(s)\n")

    if not flights:
        print("😢 No matching flights found.")
        return

    table = PrettyTable()
    table.field_names = [
        "Time",
        "Flight No.",
        "Airline",
        "From/To",
        "Terminal",
        "Gate / Stand",
        "Status",
    ]
    table.align = "l"

    for f in flights:
        flight_nos = " / ".join(fl["no"] for fl in f.get("flight", []))
        airlines = " / ".join(fl["airline"] for fl in f.get("flight", []))
        place = ", ".join(f.get("origin" if is_arrival else "destination", []))

        gate_or_stand = f.get("gate") or f.get("stand") or "-"

        table.add_row(
            [
                f.get("time", "-"),
                flight_nos,
                airlines,
                place,
                f.get("terminal") or "-",
                gate_or_stand,
                f.get("status") or "-",
            ]
        )

    print(table)


def main():
    print(text2art("HK Airport", font="small"))
    print("=== Hong Kong International Airport Flight Finder ===\n")

    # --- Input ---
    target_date = input("Enter date (YYYY-MM-DD) [default = yesterday]: ").strip()
    if not target_date:
        target_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    direction = input("Arrival or Departure? (a/d) [default = d]: ").strip().lower()
    is_arrival = direction in ("a", "arrival", "arr")

    keyword = input("City or airport code (e.g. Tokyo, NRT, Seoul, TPE): ").strip()
    if not keyword:
        print("❌ Please enter a city or code.")
        return

    codes = resolve_codes(keyword)
    if not codes:
        print(f"❌ Cannot understand '{keyword}'. Try a city name or 3-letter code.")
        return

    print("\n⏳ Searching...\n")

    # --- Fetch & Filter ---
    flights = get_hko_flights(target_date, arrival=is_arrival, cargo=False)
    matched = filter_flights(flights, codes, is_arrival)

    # --- Display ---
    display_flights(matched, target_date, is_arrival, keyword, codes)


if __name__ == "__main__":
    main()
