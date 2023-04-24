import os
import time

import requests
from faker import Faker

from src.requests.form_builder import Form

requestTimeoutLength = float(os.getenv("SLEEP_TIME", 1)) # Seconds to wait between successful requests
retryTimeoutLength = 10  # Seconds to wait after an error before retrying

URL = "https://ago.mo.gov/file-a-complaint/transgender-center-concerns?sf_cntrl_id=ctl00$MainContent$C001"
count = 0

fake = Faker()
form = Form()

while True:
    count += 1

    try:
        response = form.send_request()
    except ConnectionError as connection_error:
        print("A connection error occurred. ")
        print("This could be a normal network error or the connection could have been blocked by the host.")
        print(f"Error text: {connection_error}")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except requests.HTTPError as http_error:
        print("An HTTP error occurred.")
        print("This means the program received an invalid HTTP response from the server.")
        print(f"Error text: {http_error}")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except TimeoutError as timeout_error:
        print("A timeout error occurred.")
        print("This means the server waited too long to send a response.")
        print(f"Error text: {timeout_error}")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except requests.exceptions.RequestException as request_exception:
        print("A request error occurred.")
        print("This means there was an ambiguous exception that occurred while handling the request.")
        print(f"Error text: {request_exception}")
        print("Trying again in 10 seconds...")
        time.sleep(retryTimeoutLength)
    except Exception as exception:
        print("An unknown error occurred.")
        print("Trying again in 10 seconds...")
        print(f"Error text: {exception}")
        time.sleep(retryTimeoutLength)
    else:  # if there were no errors
        if not response.ok:
            print(f"Endpoint failed {response.status_code}.")
            print("Trying again in 10 seconds...")
            time.sleep(retryTimeoutLength)
        elif "already submitted" in response.text:
            print("Got 'Form already submitted' message. New workaround required?")
            print("Trying again in 10 seconds...")
            time.sleep(retryTimeoutLength)
        else:
            print(f"Response {count} submitted successfully")
            time.sleep(requestTimeoutLength)
