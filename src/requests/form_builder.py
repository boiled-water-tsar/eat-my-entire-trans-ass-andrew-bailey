from faker import Faker
from requests_toolbelt.multipart.encoder import MultipartEncoder

from src.generators import address, phone

fake = Faker()
addy = address.Address.generate_address()
phone_number = phone.Phone.generate_phone(addy).randomize_format()


def form_builder():
    return {"TextFieldController_4": fake.first_name(),
            "TextFieldController_5": fake.last_name(),
            "TextFieldController_1": addy.street_address,
            "TextFieldController_2": addy.city,
            "DropdownListFieldController": "MO",
            "TextFieldController_6": addy.postcode,
            "TextFieldController_0": fake.free_email(),
            "TextFieldController_3": phone_number,
            "ParagraphTextFieldController": fake.paragraph(10)}
