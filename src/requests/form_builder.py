import requests
from faker import Faker
from requests_toolbelt.multipart.encoder import MultipartEncoder

from src.captcha import fuck_missouri
from src.generators import address, phone


class Form:
    def __init__(self):
        self.multipart_data = None
        self.parsed_form_data = None
        self.headers = None
        self.form_data = None
        self.faker = Faker()

    def send_request(self):
        self._build_form()
        self._solve_captcha()
        self._build_headers()
        return requests.post('https://ago.mo.gov/file-a-complaint/transgender-center-concerns',
                             params={'sf_cntrl_id': 'ctl00$MainContent$C001'},
                             headers=self.headers,
                             data=self.parsed_form_data
                             )

    def _build_form(self):
        addy = address.Address.generate_address()
        phone_number = phone.Phone.generate_phone(addy).randomize_format()
        self.form_data = {"TextFieldController_4": self.faker.first_name(),
                          "TextFieldController_5": self.faker.last_name(),
                          "TextFieldController_1": addy.street_address,
                          "TextFieldController_2": addy.city,
                          "DropdownListFieldController": "MO",
                          "TextFieldController_6": addy.postcode,
                          "TextFieldController_0": self.faker.free_email(),
                          "TextFieldController_3": phone_number,
                          "ParagraphTextFieldController": self.faker.paragraph(10)}
        return self

    def _solve_captcha(self):
        captcha_resp = fuck_missouri.generate_captcha_token()
        self.form_data.update(captcha_resp)
        self.multipart_data = MultipartEncoder(fields=self.form_data)
        self.parsed_form_data = self.multipart_data.to_string().decode()
        return self

    def _build_headers(self):
        self.headers = {
            'Content-Type': self.multipart_data.content_type,
            'User-Agent': self.faker.user_agent(),
            'X-Forwarded-For': self.faker.ipv4()
        }
