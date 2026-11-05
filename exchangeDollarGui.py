import requests
from easygui import multenterbox, msgbox

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

fields = ["Base currency (e.g. USD)", "Amount"]
values = multenterbox("Enter conversion details:", "Currency Converter", fields)

if values is None: 
    msgbox("Cancelled. Goodbye!", "Currency Converter")        
    exit()

base_code = values[0].strip().upper()
amount = float(values[1].strip())

lines = []
try:
    for code in TARGETS.values():
        rate = get_rates(base_code, code)
        exchange_amount = amount * rate
        lines.append(f"{code}: {exchange_amount:,.4f}")
    lines += ["", "Rates By Exchange Rate API"]
    msgbox("\n".join(lines), "Conversion Results")
except KeyError:
    msgbox(f"Unsupported currency code: {base_code} or {target_code}", "Error")
except Exception as e:
    msgbox(f"Error: {e}", "Error")

