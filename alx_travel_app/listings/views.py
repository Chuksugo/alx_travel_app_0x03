from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import requests
import uuid

from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation_email

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        # Trigger async email task
        if booking.user and booking.user.email:
            send_booking_confirmation_email.delay(booking.user.email, booking.id)

@api_view(['POST'])
def initiate_payment(request):
    data = request.data
    booking_reference = data.get("booking_reference")
    amount = data.get("amount")
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    # Generate unique transaction reference
    tx_ref = str(uuid.uuid4())

    payload = {
        "amount": str(amount),
        "currency": "ETB",
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "tx_ref": tx_ref,
        "callback_url": "http://localhost:8000/api/payment/verify/"
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.post(
        f"{settings.CHAPA_BASE_URL}/transaction/initialize",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        resp_data = response.json()
        Payment.objects.create(
            booking_reference=booking_reference,
            transaction_id=tx_ref,
            amount=amount,
            status="Pending"
        )
        return Response(resp_data, status=status.HTTP_200_OK)

    return Response(
        {"error": "Payment initiation failed"},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def verify_payment(request):
    tx_ref = request.query_params.get("tx_ref")

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
    }

    response = requests.get(
        f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}",
        headers=headers
    )

    if response.status_code == 200:
        resp_data = response.json()
        payment = Payment.objects.filter(transaction_id=tx_ref).first()

        if payment:
            if resp_data.get("status") == "success":
                payment.status = "Completed"
            else:
                payment.status = "Failed"
            payment.save()

        return Response(resp_data, status=status.HTTP_200_OK)

    return Response(
        {"error": "Verification failed"},
        status=status.HTTP_400_BAD_REQUEST
    )
