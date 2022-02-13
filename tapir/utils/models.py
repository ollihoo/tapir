from __future__ import annotations

from collections import namedtuple
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

# http://xml.coverpages.org/country3166.html
COUNTRIES = (
    ("AD", _("Andorra")),
    ("AE", _("United Arab Emirates")),
    ("AF", _("Afghanistan")),
    ("AG", _("Antigua & Barbuda")),
    ("AI", _("Anguilla")),
    ("AL", _("Albania")),
    ("AM", _("Armenia")),
    ("AN", _("Netherlands Antilles")),
    ("AO", _("Angola")),
    ("AQ", _("Antarctica")),
    ("AR", _("Argentina")),
    ("AS", _("American Samoa")),
    ("AT", _("Austria")),
    ("AU", _("Australia")),
    ("AW", _("Aruba")),
    ("AZ", _("Azerbaijan")),
    ("BA", _("Bosnia and Herzegovina")),
    ("BB", _("Barbados")),
    ("BD", _("Bangladesh")),
    ("BE", _("Belgium")),
    ("BF", _("Burkina Faso")),
    ("BG", _("Bulgaria")),
    ("BH", _("Bahrain")),
    ("BI", _("Burundi")),
    ("BJ", _("Benin")),
    ("BM", _("Bermuda")),
    ("BN", _("Brunei Darussalam")),
    ("BO", _("Bolivia")),
    ("BR", _("Brazil")),
    ("BS", _("Bahama")),
    ("BT", _("Bhutan")),
    ("BV", _("Bouvet Island")),
    ("BW", _("Botswana")),
    ("BY", _("Belarus")),
    ("BZ", _("Belize")),
    ("CA", _("Canada")),
    ("CC", _("Cocos (Keeling) Islands")),
    ("CF", _("Central African Republic")),
    ("CG", _("Congo")),
    ("CH", _("Switzerland")),
    ("CI", _("Ivory Coast")),
    ("CK", _("Cook Iislands")),
    ("CL", _("Chile")),
    ("CM", _("Cameroon")),
    ("CN", _("China")),
    ("CO", _("Colombia")),
    ("CR", _("Costa Rica")),
    ("CU", _("Cuba")),
    ("CV", _("Cape Verde")),
    ("CX", _("Christmas Island")),
    ("CY", _("Cyprus")),
    ("CZ", _("Czech Republic")),
    ("DE", _("Germany")),
    ("DJ", _("Djibouti")),
    ("DK", _("Denmark")),
    ("DM", _("Dominica")),
    ("DO", _("Dominican Republic")),
    ("DZ", _("Algeria")),
    ("EC", _("Ecuador")),
    ("EE", _("Estonia")),
    ("EG", _("Egypt")),
    ("EH", _("Western Sahara")),
    ("ER", _("Eritrea")),
    ("ES", _("Spain")),
    ("ET", _("Ethiopia")),
    ("FI", _("Finland")),
    ("FJ", _("Fiji")),
    ("FK", _("Falkland Islands (Malvinas)")),
    ("FM", _("Micronesia")),
    ("FO", _("Faroe Islands")),
    ("FR", _("France")),
    ("FX", _("France, Metropolitan")),
    ("GA", _("Gabon")),
    ("GB", _("United Kingdom (Great Britain)")),
    ("GD", _("Grenada")),
    ("GE", _("Georgia")),
    ("GF", _("French Guiana")),
    ("GH", _("Ghana")),
    ("GI", _("Gibraltar")),
    ("GL", _("Greenland")),
    ("GM", _("Gambia")),
    ("GN", _("Guinea")),
    ("GP", _("Guadeloupe")),
    ("GQ", _("Equatorial Guinea")),
    ("GR", _("Greece")),
    ("GS", _("South Georgia and the South Sandwich Islands")),
    ("GT", _("Guatemala")),
    ("GU", _("Guam")),
    ("GW", _("Guinea-Bissau")),
    ("GY", _("Guyana")),
    ("HK", _("Hong Kong")),
    ("HM", _("Heard & McDonald Islands")),
    ("HN", _("Honduras")),
    ("HR", _("Croatia")),
    ("HT", _("Haiti")),
    ("HU", _("Hungary")),
    ("ID", _("Indonesia")),
    ("IE", _("Ireland")),
    ("IL", _("Israel")),
    ("IN", _("India")),
    ("IO", _("British Indian Ocean Territory")),
    ("IQ", _("Iraq")),
    ("IR", _("Islamic Republic of Iran")),
    ("IS", _("Iceland")),
    ("IT", _("Italy")),
    ("JM", _("Jamaica")),
    ("JO", _("Jordan")),
    ("JP", _("Japan")),
    ("KE", _("Kenya")),
    ("KG", _("Kyrgyzstan")),
    ("KH", _("Cambodia")),
    ("KI", _("Kiribati")),
    ("KM", _("Comoros")),
    ("KN", _("St. Kitts and Nevis")),
    ("KP", _("Korea, Democratic People's Republic of")),
    ("KR", _("Korea, Republic of")),
    ("KW", _("Kuwait")),
    ("KY", _("Cayman Islands")),
    ("KZ", _("Kazakhstan")),
    ("LA", _("Lao People's Democratic Republic")),
    ("LB", _("Lebanon")),
    ("LC", _("Saint Lucia")),
    ("LI", _("Liechtenstein")),
    ("LK", _("Sri Lanka")),
    ("LR", _("Liberia")),
    ("LS", _("Lesotho")),
    ("LT", _("Lithuania")),
    ("LU", _("Luxembourg")),
    ("LV", _("Latvia")),
    ("LY", _("Libyan Arab Jamahiriya")),
    ("MA", _("Morocco")),
    ("MC", _("Monaco")),
    ("MD", _("Moldova, Republic of")),
    ("MG", _("Madagascar")),
    ("MH", _("Marshall Islands")),
    ("ML", _("Mali")),
    ("MN", _("Mongolia")),
    ("MM", _("Myanmar")),
    ("MO", _("Macau")),
    ("MP", _("Northern Mariana Islands")),
    ("MQ", _("Martinique")),
    ("MR", _("Mauritania")),
    ("MS", _("Monserrat")),
    ("MT", _("Malta")),
    ("MU", _("Mauritius")),
    ("MV", _("Maldives")),
    ("MW", _("Malawi")),
    ("MX", _("Mexico")),
    ("MY", _("Malaysia")),
    ("MZ", _("Mozambique")),
    ("NA", _("Namibia")),
    ("NC", _("New Caledonia")),
    ("NE", _("Niger")),
    ("NF", _("Norfolk Island")),
    ("NG", _("Nigeria")),
    ("NI", _("Nicaragua")),
    ("NL", _("Netherlands")),
    ("NO", _("Norway")),
    ("NP", _("Nepal")),
    ("NR", _("Nauru")),
    ("NU", _("Niue")),
    ("NZ", _("New Zealand")),
    ("OM", _("Oman")),
    ("PA", _("Panama")),
    ("PE", _("Peru")),
    ("PF", _("French Polynesia")),
    ("PG", _("Papua New Guinea")),
    ("PH", _("Philippines")),
    ("PK", _("Pakistan")),
    ("PL", _("Poland")),
    ("PM", _("St. Pierre & Miquelon")),
    ("PN", _("Pitcairn")),
    ("PR", _("Puerto Rico")),
    ("PT", _("Portugal")),
    ("PW", _("Palau")),
    ("PY", _("Paraguay")),
    ("QA", _("Qatar")),
    ("RE", _("Reunion")),
    ("RO", _("Romania")),
    ("RU", _("Russian Federation")),
    ("RW", _("Rwanda")),
    ("SA", _("Saudi Arabia")),
    ("SB", _("Solomon Islands")),
    ("SC", _("Seychelles")),
    ("SD", _("Sudan")),
    ("SE", _("Sweden")),
    ("SG", _("Singapore")),
    ("SH", _("St. Helena")),
    ("SI", _("Slovenia")),
    ("SJ", _("Svalbard & Jan Mayen Islands")),
    ("SK", _("Slovakia")),
    ("SL", _("Sierra Leone")),
    ("SM", _("San Marino")),
    ("SN", _("Senegal")),
    ("SO", _("Somalia")),
    ("SR", _("Suriname")),
    ("ST", _("Sao Tome & Principe")),
    ("SV", _("El Salvador")),
    ("SY", _("Syrian Arab Republic")),
    ("SZ", _("Swaziland")),
    ("TC", _("Turks & Caicos Islands")),
    ("TD", _("Chad")),
    ("TF", _("French Southern Territories")),
    ("TG", _("Togo")),
    ("TH", _("Thailand")),
    ("TJ", _("Tajikistan")),
    ("TK", _("Tokelau")),
    ("TM", _("Turkmenistan")),
    ("TN", _("Tunisia")),
    ("TO", _("Tonga")),
    ("TP", _("East Timor")),
    ("TR", _("Turkey")),
    ("TT", _("Trinidad & Tobago")),
    ("TV", _("Tuvalu")),
    ("TW", _("Taiwan, Province of China")),
    ("TZ", _("Tanzania, United Republic of")),
    ("UA", _("Ukraine")),
    ("UG", _("Uganda")),
    ("UM", _("United States Minor Outlying Islands")),
    ("US", _("United States of America")),
    ("UY", _("Uruguay")),
    ("UZ", _("Uzbekistan")),
    ("VA", _("Vatican City State (Holy See)")),
    ("VC", _("St. Vincent & the Grenadines")),
    ("VE", _("Venezuela")),
    ("VG", _("British Virgin Islands")),
    ("VI", _("United States Virgin Islands")),
    ("VN", _("Viet Nam")),
    ("VU", _("Vanuatu")),
    ("WF", _("Wallis & Futuna Islands")),
    ("WS", _("Samoa")),
    ("YE", _("Yemen")),
    ("YT", _("Mayotte")),
    ("YU", _("Yugoslavia")),
    ("ZA", _("South Africa")),
    ("ZM", _("Zambia")),
    ("ZR", _("Zaire")),
    ("ZW", _("Zimbabwe")),
    ("ZZ", _("Unknown or unspecified country")),
)

PREFERRED_LANGUAGES = [
    ("de", _("🇩🇪 Deutsch")),
    ("en", _("🇬🇧 English")),
]


class CountryField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 2)
        kwargs.setdefault("choices", COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"


class RangeModelMixin(models.Model):
    """RangeModelMixin represents an open-ended (time) range. It must have a start and may have an end."""

    class Meta:
        abstract = True

    def _get_start(self):
        return getattr(self, self.RangeModelMeta.start_field_name)

    def _get_end(self):
        return getattr(self, self.RangeModelMeta.end_field_name)

    ## Return True if the model is currently active, else False
    def is_active(self, effective_date=None) -> bool:
        if not effective_date:
            # if no effective date was given, use today as the default
            effective_date = date.today()
        # check if the start date is in the future
        if self._get_start() > effective_date:
            # if the start is in the future, the model is not active
            return False

        # now we have established that the start date is today or in the past
        if self._get_end() is None:
            # unlimited duration
            return True
        elif self._get_end() >= effective_date:
            # end date is today or in the future
            return True

        # end date is in the past, the model is not active anymore
        return False

    ## Return True if the model overlaps with the given model, else false
    ## @param `other` the model to check overlap with
    def overlaps_with(self, other: RangeModelMixin) -> bool:
        overlaps = False

        # Use brute force to find overlaps
        if self._get_start():
            overlaps = overlaps or other.is_active(self._get_start())
        if other._get_start():
            overlaps = overlaps or self.is_active(other._get_start())
        if self._get_end():
            overlaps = overlaps or other.is_active(self._get_end())
        if other._get_end():
            overlaps = overlaps or self.is_active(other._get_end())

        return overlaps

    ## Validate the model
    def clean(self, *args, **kwargs):
        super().clean()
        # Ensure that the duration has a start date
        if not self._get_start():
            raise ValidationError(_("start date must be set"))
        # Ensure that the start date precedes the end date
        if self._get_end() and self._get_start() > self._get_end():
            raise ValidationError(_("Start date must be prior to end date"))


class RangeModelMixinQuerySet(models.QuerySet):
    ## Filter all objects that overlap with the given object.
    #
    # @param obj the object that the filtered objects should overlap with
    # @return all objects that overlap with the given object but not the given object itself
    def overlapping_with(self, obj) -> RangeModelMixinQuerySet:
        # Moved to _get_model instead of attribute to avoic cyclic dependency
        start_field_name = self._get_model().RangeModelMeta.start_field_name
        end_field_name = self._get_model().RangeModelMeta.end_field_name

        if isinstance(obj, tuple):
            start, end = obj
        else:
            start = obj._get_start()
            end = obj._get_end()

        return self.filter(
            (
                # All objects that begin after `obj` begins
                Q(**{start_field_name + "__gte": start})
                &
                # and begin during the duration of `obj`
                (Q(**{start_field_name + "__lte": end}) if end is not None else Q())
            )
            | (
                # All object that begin before `obj` begins
                Q(**{start_field_name + "__lte": start})
                &
                # and end after `obj` begins
                (
                    Q(**{end_field_name + "__gte": start})
                    | Q(**{end_field_name + "__isnull": True})
                )
            )
        ).exclude(id=(obj.id if hasattr(obj, "id") else None))

    ## Filter all objects that are active on a given date.
    # @param effective_date The date that the objects returned should all be active on.
    def active_temporal(self, effective_date=None) -> RangeModelMixinQuerySet:
        if not effective_date:
            # if no effective date was given, use today as the default
            effective_date = date.today()
        return self.overlapping_with((effective_date, effective_date))


class DateDurationModelMixinQuerySet(RangeModelMixinQuerySet):
    def _get_model(self):
        return DateDurationModelMixin


## Mixin to represent a model that is active inbetween two dates
class DateDurationModelMixin(RangeModelMixin):
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(null=True, blank=True, db_index=True)

    objects = DateDurationModelMixinQuerySet.as_manager()

    class RangeModelMeta:
        start_field_name = "start_date"
        end_field_name = "end_date"

    class Meta(RangeModelMixin.Meta):
        ordering = ["-start_date"]
        abstract = True


def get_country_code(full_country_name: str) -> str:
    for pair in COUNTRIES:
        if full_country_name in pair[1]:
            return pair[0]

    raise Exception("Country code not found for " + full_country_name)


def copy_user_info(source, target):
    target.first_name = source.first_name
    target.last_name = source.last_name
    target.email = source.email
    target.phone_number = source.phone_number
    target.birthdate = source.birthdate
    target.street = source.street
    target.street_2 = source.street_2
    target.postcode = source.postcode
    target.city = source.city
    target.country = source.country
    target.preferred_language = source.preferred_language
