from django.urls import path
from .views import ChatWebhookView, RazorpayPaymentView, RazorpayPaymentAndTicketGenerationView

urlpatterns = [
    path('sangrah-bot/',ChatWebhookView.as_view(), name = "sangrah-bot"),
    path('payment-gateway/', RazorpayPaymentView.as_view(), name = "payment"),
    path('verify-and-generate/', RazorpayPaymentAndTicketGenerationView.as_view(), name = "payment-verification-and-pdf-generation")
]