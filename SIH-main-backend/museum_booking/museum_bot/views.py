from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Trip
from .serializers import TripSerializer
from .utils import create_razorpay_payment_link, get_payment_status
from .models import Museum
from .utils2 import generate_and_upload_ticket
from datetime import datetime

class ChatWebhookView(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('sessionInfo', {}).get('parameters', {}).get('phone_number')
        museum_name = request.data.get('sessionInfo', {}).get('parameters', {}).get('museum_name')
        adult_visitors = request.data.get('sessionInfo', {}).get('parameters', {}).get('adult_visitors')
        child_visitors = request.data.get('sessionInfo', {}).get('parameters', {}).get('child_visitors')
        visit_date = request.data.get('sessionInfo', {}).get('parameters', {}).get('visiting_date')

        if phone_number:
            user, created = CustomUser.objects.get_or_create(phone_number=phone_number)

            if created:
                response = {"fulfillmentText": f"Your phone number {phone_number} has been registered."}
            else:
                response = {"fulfillmentText": f"Your phone number {phone_number} is already registered. Continue with your booking!"}

            if not museum_name or not visit_date:
                return Response(response, status=status.HTTP_200_OK)
            
            try:
                trip_data = {
                    'user': user.id,
                    'museum_name': museum_name,
                    'visitors_info': {
                        'adults': adult_visitors,
                        'kids': child_visitors,
                        'visit_date': visit_date
                    },
                    'phone_number': phone_number
                }

                trip_serializer = TripSerializer(data=trip_data)
                
                if trip_serializer.is_valid():
                    trip_serializer.save()
                    return Response({
                        "fulfillmentText": "Your trip has been booked successfully!",
                    }, status=status.HTTP_201_CREATED)
                else:
                    print(f"Serializer errors: {trip_serializer.errors}")
                    return Response(trip_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
            except Exception as e:
                print(f"An error occurred: {e}")
                return Response({"fulfillmentText": "An error occurred while booking the trip."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"fulfillmentText": "Sorry, I didn't understand that."}, status=status.HTTP_400_BAD_REQUEST)


def calc_price(adults, child, museum_name):
    try:
        museum = Museum.objects.get(MUSEUM_NAME=museum_name)
        total_price = adults * museum.ADULTPRICE + child * museum.CHILDPRICE
        return total_price
    except Museum.DoesNotExist:
        return None
    
class RazorpayPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            adult_visitors = request.data.get('sessionInfo', {}).get('parameters', {}).get('adult_visitors', 0)
            child_visitors = request.data.get('sessionInfo', {}).get('parameters', {}).get('child_visitors', 0)
            museum_name = request.data.get('sessionInfo', {}).get('parameters', {}).get('museum_name', '')

            print(museum_name)
            total_price = calc_price(adult_visitors, child_visitors, museum_name)
            if total_price is None:
                return Response({
                    "fulfillmentMessages": [
                        {
                            "text": {
                                "text": ["Sorry, the museum you selected was not found. Please choose another one."]
                            }
                        }
                    ]
                }, status=status.HTTP_404_NOT_FOUND)
            
            amount = total_price * 100

            payment_link = create_razorpay_payment_link(amount, f"Ticket payment for {museum_name}")

            payment_url = payment_link['short_url']

            return Response({
                    "fulfillment_response": {
                        "messages": [
                            {
                                "text": {
                                    "text": [f"Your payment link has been generated! Please proceed to payment: $session.params.payment_url. Please confirm the payment "]
                                }
                            }
                        ]
                    },
                    "session_info": {
                        "parameters": {
                            "payment_url": payment_url,
                            "plink": payment_link['id']
                        }
                    }
                }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({
                "fulfillment_response": {
                    "messages": [
                        {
                            "text": {
                                "text": ["An error occurred while creating the payment link. Please try again later."]
                            }
                        }
                    ]
                },
                "session_info": {
                    "parameters": {
                        "error": str(e)
                    }
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RazorpayPaymentAndTicketGenerationView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            session_parameters = request.data.get('sessionInfo', {}).get('parameters', {})
            razorpay_plink = session_parameters.get('plink')

            museum_name = session_parameters.get('museum_name', 'Unknown Museum')
            num_adults = session_parameters.get('adult_visitors', 1)
            num_children = session_parameters.get('child_visitors', 0)
            date_time = session_parameters.get('visiting_date', 'Not Specified')

            image_path = r"C:\Users\Anshuman Raj\OneDrive\Desktop\SIH main back\SIH-main-backend\museum_booking\museum_bot\museum_static\logo.png"

            pdf_file_name = f"ticket_{razorpay_plink}.pdf"
            booking_credentials = generate_and_upload_ticket(museum_name, num_adults, num_children, date_time, image_path,pdf_file_name)
            print(booking_credentials)
            return Response({
                "fulfillment_response": {
                    "messages": [
                        {
                            "text": {
                                "text": [f"Here is your ticket: $session.params.booking_credentials"]
                            }
                        }
                    ]
                },
                "session_info": {
                    "parameters": {
                        "booking_credentials": booking_credentials
                    }
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"An error occurred during ticket generation: {e}")
            return Response({
                "fulfillmentMessages": [
                    {
                        "text": {
                            "text": ["An error occurred during ticket generation. Please try again later."]
                        }
                    }
                ],
                "session_info": {
                    "parameters": {
                        "error": str(e)
                    }
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
