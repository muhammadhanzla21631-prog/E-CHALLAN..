# Notification System Setup

The E-Challan system now supports sending notifications via **Email (Gmail)** and **WhatsApp (Twilio)**.

## 1. Environment Variables

To enable these features, you must set the following environment variables. You can set these in your terminal or create a `.env` file (if using `python-dotenv`).

### Email (Gmail)
- `MAIL_SENDER`: Your Gmail address (e.g., `yourname@gmail.com`)
- `MAIL_PASSWORD`: Your **App Password** (Not your login password).
    - Go to Google Account > Security > 2-Step Verification > App passwords.
    - Generate a new app password and use it here.

### WhatsApp (Twilio)
- `TWILIO_SID`: Your Twilio Account SID.
- `TWILIO_TOKEN`: Your Twilio Auth Token.
- `TWILIO_FROM`: Your Twilio WhatsApp number (e.g., `whatsapp:+14155238886`).

## 2. Usage

When issuing a challan via the API, provide the `user_id` to trigger notifications for that user.

```http
POST /api/challan
Content-Type: application/json

{
  "vehicle": "LEC-1234",
  "camera_id": 1,
  "amount": 500,
  "user_id": 1
}
```

If the user (ID 1) has an email and phone number saved in the database, they will receive the notifications.

## 3. Dependencies

Ensure you have installed the required packages:
```bash
pip install twilio
```
(This is already added to `requirements.txt`)
