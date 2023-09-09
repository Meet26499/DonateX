# DonateX: A Charitable Donation System with Phone-based Authentication and Payment Gateway Integration

## Introduction
DonateX is an open-source charitable donation system that combines phone-based authentication and seamless payment gateway integration. This system enables users to make donations securely and easily, track their donation history, and visualize their contributions over time.

## Getting Started
Follow these steps to set up the DonateX project on your local system:

1. #### Clone the Repository:
    ```git clone https://github.com/Meet26499/DonateX```

2. #### Create an Environment File:
    Create an environment file (.env) and add the necessary variables to configure the project. You will need to set up environment variables for Twilio and Stripe integration.

3. #### Create a Virtual Environment (Optional):

4. #### Docker Setup (Optional):
    If you prefer, you can use Docker to set up the project and its dependencies. Simply add the `docker-compose.yml` and `Dockerfile` provided and run the following command to build the Docker container:

    ```sudo docker-compose up --build```

## API Endpoints
DonateX provides the following API endpoints:

- `Send OTP`
    - `Endpoint`: http://127.0.0.1:8000/send-otp
    - `Description`: This API is used to send a one-time password (OTP) for phone-based authentication to the user. Twilio is used as the third-party library to send OTP.

- `Verify OTP And Login`
    - `Endpoint` - http://127.0.0.1:8000/login
    - `Description` - This API is used to verify the OTP which user provides and ogin the user in our system.

- `Donation`
    - `Endpoint` - http://127.0.0.1:8000/donation
    - `Description` - This API is used to create payment for donation amount user has provided using third party library. For this I have used the Stripe payment gateway to pay user's donation amount.

- `Donation Listing`
    - `Endpoint` - http://127.0.0.1:8000/donation-list
    - `Description` - This API is used to list the successful donations which user has made till now.

- `Donation Visualization`
    - `Endpoint` - http://127.0.0.1:8000/donation-visualization
    - `Query Params`
        - start_date -- start date of the donation
        - end_date -- end date of the donation
        - days -- days in number for which donation data is required to visualize
    - `Description` - This API is used to visualize the donation data for date range for that particular user. For this I have used Plotly library to generate the graph to show the Average donation of user over a period of time.

## Configuration

### Twilio
To use Twilio for OTP authentication, follow these steps:

- Set up a Twilio account.
- Get your Twilio information (e.g., account SID, authentication token).
- Set these Twilio variables in your .env file.
- Generate a Twilio testing number to send SMS from and set it as TWILIO_PHONE_NUMBER.

### Stripe
To integrate with Stripe for payment processing, do the following:

- Create a Stripe account.
- Obtain your publishable and secret API keys from Stripe.
- Set these Stripe variables in your .env file.
- You can use CARD_TEST_TOKEN for testing in India.