import os
import random
from typing import Optional


addresses = open('mo.csv', 'rb')
# max value for random byte seeking
bound = os.path.getsize('mo.csv') - 2 # skip the final newline+null
# ensure bound does not include the final location in dataset for 1/n edge case
addresses.seek(bound)
while addresses.read(1) != b'\n':
    bound -= 1
    addresses.seek(bound)


class Address:
    def __init__(self, number: str, street: str, unit: Optional[str], city: str, postcode: str):
        self.street_address = number + ' ' + street
        self.unit = unit
        self.city = city
        self.postcode = postcode

    def __repr__(self):
        return f"{self.street_address}, {(self.unit + ', ') if self.unit else ''}{self.city}, MO, {self.postcode}"

    # ram-constant, time-constant random choice alg for a missouri address
    # pick a random byte offset, seek to it, increment until newline, read until next newline
    # avoid picking EOF by bounding randint to the second-to-last newline; see above
    @classmethod
    def generate_address(cls):
        """generates a random address in missouri. dataset from kaggle

        Returns:
            Address: gps trackable
        """
        byte = random.randint(0, bound)
        addresses.seek(byte)
        while addresses.read(1) != b'\n':
            byte += 1
            addresses.seek(byte)

        return cls(
            *next(addresses).rstrip(b"\r\n").decode().split(",")
            )