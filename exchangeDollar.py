import requests

TARGETS = {
    "HK dollars":     "HKD",
    "US dollars":     "USD",
    "Renmenbi":       "CNY",
    "Yen":            "JPY",
    "British Pound":  "GBP",
    "EURO":           "EUR",
    "Thai Baht":      "THB",
    "Korean wons":    "KRW",
}

def get_rates(base_code, target_code):
    url = f"https://open.er-api.com/v6/latest/{base_code.upper()}"
    response = requests.get(url, timeout=15)
    data = response.json()
    if data.get("result") != "success":
        raise RuntimeError(data.get("error-type", "API error"))
    return data["rates"][target_code.upper()]

print("=== Currency Converter ===")

base_code = input("Enter the currency you have (ISO code, e.g. USD, HKD, EUR): ").strip().upper()
amount = float(input("Enter the amount: ").strip())
# target_code = input("Enter the currency you want convert to (ISO code, e.g. USD, HKD, EUR): ").strip().upper()

try:
    for code in TARGETS.values():
        rate = get_rates(base_code, code)
        exchange_amount = amount * rate
        print(f"The exchange amount for {code} is {exchange_amount}")
except KeyError:
    print(f"Unsupported currency code: {base_code} or {code}")
except Exception as e:
    print(f"Error: {e}")