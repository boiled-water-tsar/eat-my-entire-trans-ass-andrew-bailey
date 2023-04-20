# threw this together because faker generates easily-filterable #s:
# w/ leading 0s on country codes, w/ extensions, etc
# TODO: address -> area code/prefix db has to exist somewhere

import random
from typing import Optional

import address


MO_AREA_CODES = ['314', '557', '417', '573', '636', '660', '816']


class Phone:
    def __init__(self, country_code: Optional[str], area: Optional[str], prefix: str, line_no: str):
        self.country_code = country_code if country_code else ''
        self.area = area if area else ''
        self.prefix = prefix
        self.line_no = line_no

    @classmethod
    def generate_phone(cls, addy: address.Address):
        return cls(
            '1',
            Phone.city_to_area(addy.city),
            Phone.address_to_prefix(),
            Phone.random_line_no()
        )

    def __repr__(self):
        return f"{self.country_code}{self.area}{self.prefix}{self.line_no}"

    def randomize_format(self) -> str:
        """1 234 567 8901 -> 234-567-8901, 12345678901, etc

        Returns:
            str: humanized phone #
        """
        res = ''
        if self.country_code and random.random() < 0.3:
            res += self.country_code + ' '
        if self.area:
            res += self.area + ' '
        res += self.prefix + ' ' + self.line_no
        if random.random() < 0.5:
            res = res.replace(' ', '-')
        elif random.random() < 0.5:
            res = res.replace(' ','')
        return res

    @staticmethod
    def city_to_area(city: str) -> str:
        match city.lower():
            case 'saint louis' | 'st. louis' | 'st louis':
                return random.choice(['314','557'])
            case 'springfield' | 'joplin' | 'branson':
                return '417'
            case 'columbia' | 'jefferson city' | 'rolla' | 'cape girardeau' | 'perryville' | 'hannibal':
                return '573'
            case 'saint charles' | 'st charles' | 'st. charles' | 'jefferson':
                return '636'
            case 'sedalia' | 'kirksville' | 'warrensburg' | 'maryville':
                return '660'
            case 'kansas city' | 'saint joseph' | 'st joseph' | 'st. joseph':
                return '816'
            case _:
                return random.choice(MO_AREA_CODES)

    @staticmethod
    def address_to_prefix() -> str:
        return str(random.randint(100, 999))

    @staticmethod
    def random_line_no() -> str:
        return str(random.randint(1000, 9999))
