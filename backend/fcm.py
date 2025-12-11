# import firebase_admin
# from firebase_admin import credentials, messaging

# Initialize Firebase Admin SDK
# You need to replace 'path/to/serviceAccountKey.json' with your actual key file path
# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

def send_push(token, title, body, data=None):
    print(f"Sending push to {token}: {title} - {body}")
    # message = messaging.Message(
    #     notification=messaging.Notification(
    #         title=title,
    #         body=body,
    #     ),
    #     data=data,
    #     token=token,
    # )
    # response = messaging.send(message)
    # print('Successfully sent message:', response)