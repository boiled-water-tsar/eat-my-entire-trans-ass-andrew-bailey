from base64 import b64decode
from hashlib import sha256
from io import BytesIO
from faker import Faker
import wave
import requests

faker = Faker()

CAPTCHA_SETTINGS_FIELD = '/RestApi/comments-api'
CAPTCHA_ENDPOINT = 'https://ago.mo.gov/RestApi/comments-api/captcha'
NULL_LIMIT = 512

HASHES = {
    '03f8e2b4b3a96190b3bd087fc6ce77371f3475daddea75928ecfe06317ac9c13': '0',
    '5cac9424d9d1a2f023101592bc726783406f2df797fae754cd8b2b1ad69808fa': '1',
    '99b4df94af4fffc23b2f35ecdbb4fc9aa47c74eb9ed7c8e82be69f74e3279e38': '2',
    'e856a3700be2b29c1e850d0390e25a027d5aef93169385e836a89abb07f23c8d': '3',
    'a6830e81f4a4c4bddd7afaccc27af37fcbac2f9cc981f85e943e66277026466c': '4',
    'ab3f07a2a35a20db58b709af4de589e5f2173d1933993a02ed4895bad9a79289': '5',
    'cf06c1b3e0c323de28e80bf7e7d1ea4b07e000b8b9b037cd6d4f126044d6d06c': '6',
    'a51efb95c9d279e6b93582ecda06964237852c9b1cd97336f4e9497d30c6cede': '7',
    'fcc6e97d40813d240bdd7b82f25d8f37f2a8aa5b971fb921657813773d1aae27': '8',
    '5c64f50f104ce7fb4af7ab047a05a369acb79ca881ff34e0a03ff21b3352a1cd': '9',
    '6f604da6a3082607e78240b37041461f439c63efcd9892e46e4641c33e5caadd': 'A',
    '5e266f13683a4e4671bc92bdb2ed3b35fff657b366bbe8ad14ce45cdd476109a': 'B',
    '57f71c73b964f422adb56be6ce40bf25a458a1ef04995d2db92e4923954e1684': 'C',
    '6074707217022d86a49c65f4f87274bcf08fd6a82fffdbb43ab20a2f3157d33d': 'D',
    '50298d96d00537f4e18b04dbd0620737bb3bd7b587e4e8e6dfca754dd24a9818': 'E',
    'c7ac8d50a7795f350769e2e6b74a5f471a924ac9600b3dbf148f9c99aa6ec2ce': 'F',
    '8f14aa376500ba99394387a99b6d08dbc0482472f821f9420735c9008c937fde': 'G',
    '78c581c45a31e3979144a3461d3a16a3479a18181c129932748785fd5a362239': 'H',
    'c72598d85ba3f6f48498e61171863911ae090f28a27de5579fa6679aec76da8b': 'I',
    'b3e8b72b7c36513e8b6a25c5a7ff2b13f4d6dfa23a1789854a0166b37648a6d5': 'J',
    'fa9e5c7010642e309f25391823d1bd2e5e3313ccfda307cd3569f0445403d8c5': 'K',
    '92640ee50edbe37a10300892c85330c583f5b926f903247fb5c65c81d3fb36cb': 'L',
    '4ac8d726fe428a1bb867e8ad12d2044458f7ff50fb4d3d89124d2d33edd9046d': 'M',
    '536dbe2612e078cf015df79e1211de1c99f0dc3d2b8f5d258f325c0d59ceec7f': 'N',
    'da444b974759601830ae0e67c016d57d5679c5d2a8b0fb62a0c0908c25f8fe3d': 'O',
    '6b44c59b37ee43a7124b696a5f4433d07f8af024fa65a4a41a5f4e0a780707ee': 'P',
    '7da59ed320c429bec81e717dc0c53c4beb20373d3b7780dd27ce6e239037b049': 'Q',
    'e24073fe8613e13e59e2fc6b59bf67d97eeabb231a19283cc65584df875c82b8': 'R',
    'c4c9af32c1a5710fbb501e55c5803eb47886dd3ea37764d588a37bd039a53af0': 'S',
    'f2a2235dcac3b0a34ca85ad54adb17c3ace8da3d259ec03237501254e3a15a0f': 'T',
    'ed9bdcea8a29596c5b67cdf5964299b3ab7d56ddd9cc12c84658af2e3426f2dd': 'U',
    'd0e1aacd630f16f23e6b5de219bb5a0d403cbb6db68309faebd301fe01598ec9': 'V',
    '12b1a5d8b31932e3ef182231da60a9c8f04e006ccb3e37da5c3d657cab115c81': 'W',
    '748130b99f450b8ff8785977306cf2c52e4680e4a3f05e27e938926c67230ffb': 'X',
    '0f76b4b016622a6d99a701784df01e97936a6c5644415b6203621989136b8292': 'Y',
    'b9c6b95d5224341f823bfbb70da97cb67a97c16dcf1caea96e4a293126634954': 'Z'
}


def solve(in_wave):
    letter_frames = []

    is_waiting = False
    consecutive_zero_frames = 0
    letter_buf = b''

    while True:
        # Read one frame from input wave file
        frames = in_wave.readframes(1)
        consecutive_zero_frames += 1

        if frames == b'':
            break

        # If we read a non-zero byte set the waiting flag to false
        if any(frames):
            consecutive_zero_frames = 0
            is_waiting = False

        # If we're still waiting, don't store
        if is_waiting:
            continue

        # Otherwise, add to buffer
        letter_buf += frames

        # If we read more than a specified limit of zero frames, set the waiting flag
        if consecutive_zero_frames > NULL_LIMIT:
            # Remove leading and trailing null bytes
            letter_frames.append(letter_buf.strip(b'\x00'))

            is_waiting = True
            letter_buf = b''

    if len(letter_frames) != 5:
        raise ValueError(f'expected 5 letters from captcha audio, got {len(letter_frames)}')

    # Hash check each letter
    letters = []

    for i, letter in enumerate(letter_frames):
        h = sha256(letter).hexdigest()

        if h not in HASHES:
            raise ValueError(f'Missing hash at idx {i} - got {h}')

        letters.append(HASHES[h])

    return ''.join(letters)


def generate_captcha_token():
    # Request the CAPTCHA data from their endpoint
    captcha_res = requests.get(CAPTCHA_ENDPOINT, headers={
        'Accept': 'application/json',
        'X-Forwarded-For': faker.ipv4()
    })

    captcha_res.raise_for_status()
    captcha_body = captcha_res.json()

    # Decode audio blob to WAV
    in_wave_b64 = captcha_body['Audio']
    in_wave_blob = b64decode(in_wave_b64)
    in_wave_bio = BytesIO(in_wave_blob)

    with wave.open(in_wave_bio, mode='rb') as in_wave:
        assert in_wave.getcomptype() == 'NONE', 'got unexpected compressed wave'
        solution = solve(in_wave)

    # Generate required form parameters
    params = {
        'captcha-a': solution,
        'captcha-ca': captcha_body['CorrectAnswer'],
        'captcha-iv': captcha_body['InitializationVector'],
        'captcha-k': captcha_body['Key'],
        'captcha-settings': CAPTCHA_SETTINGS_FIELD
    }

    return params


if __name__ == '__main__':
    params = generate_captcha_token()
