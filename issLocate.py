import requests
from time import sleep

link = "http://api.open-notify.org/iss-now.json"

# response = requests.get(link)
# print(response)
# data = response.json()
# print(data)
# print(data['message'])
# print(data['iss_position']['longitude'])
for i in range(3):
    response = requests.get(link)
    data = response.json()
    print(data['iss_position']['longitude'])
    sleep(10)
    
# import requests
# from time import sleep

# link = "http://api.open-notify.org/iss-now.json"

# for i in range(3):
#     try:
#         # Added a 5-second timeout so it doesn't hang indefinitely
#         response = requests.get(link, timeout=5) 
#         response.raise_for_status() # Check for HTTP errors
        
#         data = response.json()
#         print(f"Success! Longitude: {data['iss_position']['longitude']}")
        
#     except requests.exceptions.ConnectTimeout:
#         print("Error: The connection timed out. The API server might be down.")
#     except requests.exceptions.RequestException as e:
#         print(f"A network error occurred: {e}")
        
#     sleep(10)
