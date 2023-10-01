from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from .models import Booking, Configuration
from datetime import datetime as dt
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count
from .forms import BookingForm


# Create your views here.
def home(request):
    opening_hour = Configuration.objects.get(key="opening_hour").value
    closing_hour = Configuration.objects.get(key="closing_hour").value
    context = {"opening_hour": opening_hour, "closing_hour": closing_hour}
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def book(request):
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "book.html", context)


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, "menu.html", {"menu": main_data})


def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, "menu_item.html", {"menu_item": menu_item})


@csrf_exempt
def bookings(request):
    if request.method == "POST":
        try:
            data = json.load(request)
        except:
            return JsonResponse("ERROR IN loading the request", status=400)

        form = BookingForm(data)

        exists = (
            Booking.objects.filter(reservation_date=data["reservation_date"])
            .filter(reservation_hour=data["reservation_hour"])
            .filter(phone_number=data["phone_number"])
            .filter(first_name=data["first_name"])
            .filter(numberOfPeople=data["number_of_guests"])
            .exists()
        )
        if not exists and form.is_valid():
            cleaned_data = form.cleaned_data

            booking = Booking(
                first_name=cleaned_data["first_name"],
                reservation_date=cleaned_data["reservation_date"],
                reservation_hour=cleaned_data["reservation_hour"],
                phone_number=cleaned_data["phone_number"],
                numberOfPeople=cleaned_data["number_of_guests"],
            )
            booking.save()

            return JsonResponse({"success": True}, status=200)
        elif exists:
            return JsonResponse({"error": "Reservation already exists"}, status=409)
        else:
            error_messages = []
            print(form.errors)
            for field, errors in form.errors.items():
                pretty_field = field.replace("_", " ").title()
                for error in errors:
                    error_messages.append(f"{pretty_field}: {error}")

            return JsonResponse({"error": error_messages}, status=400)

    date = request.GET.get("date", dt.today().date())
    try:
        opening_hour = Configuration.objects.get(key="opening_hour").value
        closing_hour = Configuration.objects.get(key="closing_hour").value
        max_guests = Configuration.objects.get(key="max_number_of_guests").value
        max_reservations = Configuration.objects.get(key="max_reservations").value
    except:
        return JsonResponse(
            "Server errors. Please try again later or contact us", status=500
        )

    reservations_per_hour = (
        Booking.objects.all()
        .filter(reservation_date=date)
        .values("reservation_hour")
        .annotate(Count("id"))
        .order_by("reservation_hour")
    )
    reservations_per_hour = list(reservations_per_hour)

    context = {
        "reservations_per_hour": reservations_per_hour,
        "max_reservations": int(max_reservations),
        "opening_hour": int(opening_hour),
        "closing_hour": int(closing_hour),
        "max_number_of_guests": int(max_guests),
    }

    return JsonResponse(context)
