from django import forms
import datetime
from .models import Configuration
import re


# Code added for loading form data on the Booking page
class BookingForm(forms.Form):
    reservation_date = forms.DateField()
    reservation_hour = forms.IntegerField()
    phone_number = forms.CharField(max_length=16)
    first_name = forms.CharField(max_length=50)
    number_of_guests = forms.IntegerField()

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data["reservation_date"]
        selected_date = reservation_date
        try:
            today = datetime.date.today()

            one_month_from_now = today + datetime.timedelta(days=30)

            if (selected_date < today) or (selected_date > one_month_from_now):
                raise forms.ValidationError("Not a valid date")

            return reservation_date
        except ValueError:
            raise forms.ValidationError("Not a valid date")

    def clean_reservation_hour(self):
        reservation_hour = self.cleaned_data["reservation_hour"]
        opening_hour = Configuration.objects.get(key="opening_hour").value
        closing_hour = Configuration.objects.get(key="closing_hour").value
        reservation_date = self.cleaned_data["reservation_date"]
        today = datetime.date.today()
        min_hour = datetime.datetime.now().hour + 1
        try:
            if reservation_date == today and reservation_hour < min_hour:
                raise forms.ValidationError(
                    f"Please choose an hour between {min_hour}:00 - {closing_hour}:00"
                )
            if reservation_hour < int(opening_hour) or reservation_hour > int(
                closing_hour
            ):
                raise forms.ValidationError(
                    f"Please choose an hour between {opening_hour}:00 - {closing_hour}:00"
                )
            return reservation_hour
        except ValueError:
            raise forms.ValidationError("Not a valid date")

    def clean_number_of_guests(self):
        number_of_guests = self.cleaned_data["number_of_guests"]
        max_guests = Configuration.objects.get(key="max_number_of_guests").value

        if number_of_guests > int(max_guests) or number_of_guests <= 0:
            raise forms.ValidationError(f"Choose between 1 - {max_guests} Guests")

        return number_of_guests

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]

        pattern = r"^\(\d{3}\) \d{3} - \d{4}$"

        if not re.match(pattern, phone_number):
            raise forms.ValidationError(
                "Invalid phone number format. Please use (123)456-789 format."
            )

        return phone_number
