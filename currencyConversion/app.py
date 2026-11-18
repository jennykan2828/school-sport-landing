from flask import Flask, render_template, request
import requests

app = Flask(__name__)

TARGETS = {
    "HK dollars":     "HKD",
    "US dollars":     "USD",
    "Renminbi":       "CNY",
    "Yen":            "JPY",
    "British Pound":  "GBP",
    "EURO":           "EUR",
    "Thai Baht":      "THB",
    "Korean wons":    "KRW",
}

def get_all_rates(base_code):
    url = f"https://open.er-api.com/v6/latest/{base_code.upper()}"
    response = requests.get(url, timeout=15)
    data = response.json()
    if data.get("result") != "success":
        raise RuntimeError(data.get("error-type", "API error"))
    return data["rates"]

@app.route('/')
def index():
    return render_template(
        'index.html',
        targets=TARGETS,
        base_code="USD",
        target_code="HKD",
        amount="100"
    )

@app.route('/submit', methods=['POST'])
def currencyConvert():
    base_code = request.form.get('base_code', 'USD').strip().upper()
    target_code = request.form.get('target_code', 'HKD').strip().upper()
    amount_str = request.form.get('amount', '0')

    results = {}
    converted_target = None
    rate_info = None
    error_msg = None

    try:
        amount = float(amount_str)
        rates = get_all_rates(base_code)

        # Calculate the main "To" box value
        target_rate = rates[target_code]
        converted_target = f"{amount * target_rate:,.2f}"
        rate_info = f"1.00 {base_code} = {target_rate:.4f} {target_code}"

        # Calculate all currencies for the grid below
        for name, code in TARGETS.items():
            rate = rates[code]
            results[f"{name} ({code})"] = f"{amount * rate:,.2f}"

    except ValueError:
        error_msg = "Please enter a valid number."
    except KeyError:
        error_msg = "Unsupported currency selected."
    except Exception as e:
        error_msg = f"Error: {e}"

    return render_template(
        'index.html',
        targets=TARGETS,
        results=results,
        converted_target=converted_target,
        rate_info=rate_info,
        error=error_msg,
        base_code=base_code,
        target_code=target_code,
        amount=amount_str
    )

if __name__ == '__main__':
    app.run(debug=True, port=5500)


# from flask import Flask, render_template, request
# import requests

# app = Flask(__name__)

# # Format: "Currency Code": ("Display Name", "2-letter flag code")
# TARGETS = {
#     "HKD": ("HK dollars",    "hk"),
#     "USD": ("US dollars",    "us"),
#     "CNY": ("Renminbi",      "cn"),
#     "JPY": ("Yen",           "jp"),
#     "GBP": ("British Pound", "gb"),
#     "EUR": ("EURO",          "eu"),
#     "THB": ("Thai Baht",     "th"),
#     "KRW": ("Korean wons",   "kr"),
# }

# def get_all_rates(base_code):
#     url = f"https://er-api.com{base_code.upper()}"
#     response = requests.get(url, timeout=15)
#     data = response.json()
#     if data.get("result") != "success":
#         raise RuntimeError(data.get("error-type", "API error"))
#     return data["rates"]

# @app.route('/')
# def index():
#     return render_template(
#         'index.html',
#         targets=TARGETS,
#         base_code="USD",
#         target_code="HKD",
#         amount="100"
#     )

# @app.route('/submit', methods=['POST'])
# def currencyConvert():
#     base_code = request.form.get('base_code', 'USD').strip().upper()
#     target_code = request.form.get('target_code', 'HKD').strip().upper()
#     amount_str = request.form.get('amount', '100').strip()

#     results = []
#     converted_target = None
#     rate_info = None
#     error_msg = None

#     try:
#         amount = float(amount_str)
#         rates = get_all_rates(base_code)

#         target_rate = rates[target_code]
#         converted_target = f"{amount * target_rate:,.2f}"
#         rate_info = f"1.00 {base_code} = {target_rate:.4f} {target_code}"

#         for code, (name, flag) in TARGETS.items():
#             rate = rates[code]
#             results.append({
#                 "code": code,
#                 "name": name,
#                 "flag": flag,
#                 "value": f"{amount * rate:,.2f}"
#             })

#     except ValueError:
#         error_msg = "Please enter a valid number."
#     except KeyError:
#         error_msg = "Unsupported currency selected."
#     except Exception as e:
#         error_msg = f"Error: {e}"

#     return render_template(
#         'index.html',
#         targets=TARGETS,
#         results=results,
#         converted_target=converted_target,
#         rate_info=rate_info,
#         error=error_msg,
#         base_code=base_code,
#         target_code=target_code,
#         amount=amount_str
#     )

# if __name__ == '__main__':
#     app.run(debug=True, port=5500)

