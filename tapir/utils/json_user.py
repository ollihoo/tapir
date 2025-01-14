import datetime

import phonenumbers
from unidecode import unidecode

from tapir.accounts.models import TapirUser
from tapir.utils.models import get_country_code
from tapir.utils.user_utils import UserUtils


# Helper class to deal with users generated from https://randomuser.me/


class JsonUser:
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthdate: datetime.date
    street: str
    street_2: str
    postcode: str
    city: str
    country: str
    date_joined: datetime.date
    preferred_language: str
    num_shares: int

    def __init__(self, parsed_json):
        self.first_name = parsed_json["name"]["first"]
        self.last_name = parsed_json["name"]["last"]
        self.email = parsed_json["email"]

        phone_number = phonenumbers.parse(parsed_json["phone"].replace("-", ""), "DE")
        if not phonenumbers.is_valid_number(phone_number):
            phone_number = "+4930182722720"  # Olaf
        self.phone_number = phone_number

        date_of_birth = parsed_json["dob"]["date"].replace("Z", "")
        self.birthdate = datetime.datetime.fromisoformat(date_of_birth).date()

        self.street = (
            parsed_json["location"]["street"]["name"]
            + " "
            + str(parsed_json["location"]["street"]["number"])
        )

        self.street_2 = ""
        self.postcode = str(parsed_json["location"]["postcode"])
        self.city = parsed_json["location"]["city"]
        self.country = get_country_code(parsed_json["location"]["country"])

        date_joined = parsed_json["registered"]["date"].replace("Z", "+00:00")
        self.date_joined = datetime.datetime.fromisoformat(date_joined)

        if parsed_json["nat"] == "DE":
            self.preferred_language = "de"
        else:
            self.preferred_language = "en"

        self.num_shares = max(parsed_json["location"]["street"]["number"] % 10, 1)

    def get_username(self) -> str:
        return unidecode(self.first_name.lower() + "." + self.last_name.lower())

    def get_display_name(self) -> str:
        return UserUtils.build_display_name(self.first_name, self.last_name)

    def get_date_of_birth_str_for_input_field(self) -> str:
        return self.birthdate.strftime("%Y-%m-%d")

    def get_birthdate_display(self) -> str:
        return self.birthdate.strftime("%d.%m.%Y")

    def get_display_address(self) -> str:
        return UserUtils.build_display_address(
            self.street, self.street_2, self.postcode, self.city
        )

    def get_tapir_user(self) -> TapirUser:
        return TapirUser.objects.get(username=self.get_username())
