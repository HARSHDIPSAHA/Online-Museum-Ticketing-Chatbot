import razorpay

RAZORPAY_KEY_ID = "rzp_test_Z0z413oXBXq0ND"
RAZORPAY_KEY_SECRET = "F0ItpJlCvi1F7i56jujGBTrL"

# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Function to create a Razorpay order
def create_razorpay_order(amount):
    """
    Create a Razorpay order using the provided amount.
    Amount should be in paise.
    """
    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "receipt": "receipt#1",
        "partial_payment": False,
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    })
    return order

# Function to create a Razorpay payment link
def create_razorpay_payment_link(amount, description):
    """
    Create a Razorpay payment link for a specific customer and amount.
    Amount should be in paise.
    """

    data = {
        "amount": amount,  # Amount in paise
        "currency": "INR",
        "description": description,
        "notify": {
            "sms": True,
            "email": False
        },
        # this is the link where we have to be redirected, add the website url here, don't use this success url, it is for dialogueflwo 
        # "callback_url": "https://tm6g92fk-8000.inc1.devtunnels.ms/payment-gateway/payment-verification/",
        # "callback_method": "get"
    }
    payment_link = client.payment_link.create(data)
    return payment_link


def get_payment_status(payment_id):
    """
    Retrieve the payment status from Razorpay using the provided payment ID.
    """
    try:
        # Fetch payment details using the payment ID
        payment = client.payment.fetch(payment_id)
        
        # Extract payment status
        payment_status = payment.get('status')

        # You can also return additional details if needed
        return {
            "payment_id": payment.get('id'),
            "status": payment_status,
            "amount": payment.get('amount'),
            "currency": payment.get('currency'),
            "method": payment.get('method'),
            "captured": payment.get('captured'),
        }

    # except razorpay.errors.RazorpayError as e:
    #     # Handle Razorpay-specific errors
    #     print(f"An error occurred while fetching payment status: {e}")
    #     return {"error": str(e)}
    
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}

payment_id = "OvKEt29jQes0LU"  # Example payment ID
status_info = get_payment_status(payment_id)

if "error" not in status_info:
    print(f"Payment ID: {status_info['payment_id']}")
    print(f"Status: {status_info['status']}")
    print(f"Amount: {status_info['amount']}")
    print(f"Currency: {status_info['currency']}")
    print(f"Method: {status_info['method']}")
    print(f"Captured: {status_info['captured']}")
else:
    print(f"Error fetching payment status: {status_info['error']}")
