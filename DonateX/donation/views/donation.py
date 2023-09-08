from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from django.db.models import Avg
import plotly.express as px
from datetime import datetime, timedelta

from ..models import STATUS_CHOICES
from ..models import Donation
from ..serializers import DonationSerializer, DonationListSerializer
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateDonationView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        try:
            # Creating Payment Method to attach this to related Payment Intent to pay through stripe
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={
                    "token": settings.CARD_TEST_TOKEN,
                },
            )

            # Creating Payment Intent to pay in stripe
            intent = stripe.PaymentIntent.create(
                amount=int(amount) * 100,
                currency="inr",
                description="Payment for order XYZ",
                payment_method=payment_method.id,
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never',
                }
            )

            # Confirm our payment intent to pay through stripe
            confirm_intent = stripe.PaymentIntent.confirm(
                intent.id,
                payment_method=payment_method.id,
                return_url=f"{settings.HOST_URL}donation-list/"
            )

            return HttpResponseRedirect(confirm_intent.get("next_action").get("redirect_to_url").get("url"))

        except stripe.error.StripeError as e:
            raise serializers.ValidationError(str(e))
        
class DonationListView(generics.ListAPIView):
    serializer_class = DonationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user, status="success")

    def get(self, request, *args, **kwargs):
        payment_intent = self.request.GET.get("payment_intent", "")
        user = self.request.user

        try:
            if payment_intent:
                intent = stripe.PaymentIntent.retrieve(
                        payment_intent
                    )
                
                if intent.status == "succeeded":
                    donation = Donation(user=user, amount=(intent.amount)/100, status='success')
                    donation.save()
                else:
                    raise Exception("Stripe charge failed")
            
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            raise serializers.ValidationError(str(e))
        

class DonationVisualizationView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        days = request.GET.get('days')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
            end_date = datetime.strptime(end_date_str, '%d-%m-%Y')
        elif days:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=int(days))
        else:
            return Response({'error': 'Please provide valid date parameters or days.'}, status=status.HTTP_400_BAD_REQUEST)

        donations = Donation.objects.filter(
            user=self.request.user,
            date__gte=start_date,
            date__lte=end_date
        ).values('date').annotate(
            avg_amount=Avg('amount'),
        )

        if not donations:
            fig = px.line(title='No Donation Data')
            fig.update_layout(annotations=[dict(text="No donation data available.", showarrow=False)])
        else:
            fig = px.line(donations, x='date', 
                        y='avg_amount', 
                        title='Average Donation Amount Over Time',
                        markers=True)

        # Convert the Plotly chart to HTML
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

        # HTML to show Plotly Chart
        html_response = f'''
        <html>
            <head>
                <!-- Include Plotly.js -->
                <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            </head>
            <body style="background-color:aliceblue">
                <h2 style="color:#2ba191;text-decoration:underline">Donation Visualization</h2>
                <div>
                    <!-- Embed the Plotly chart -->
                    {chart_html}
                </div>
            </body>
        </html>
        '''

        return HttpResponse(html_response)
