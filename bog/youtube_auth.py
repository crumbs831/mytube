# AIzaSyBfCbZW4ci4azQVQOqN_h1T5YAJTcKdAtE
# # Create a new file: youtube_auth.py

# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.oauth2.credentials import Credentials
# import os

# SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# def get_youtube_credentials():
#     # Path to your client secrets file
#     client_secrets_file = "client_secret.json"
    
#     # Check if we have stored credentials
#     if os.path.exists('token.json'):
#         credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
#     else:
#         # If no stored credentials, run the OAuth flow
#         flow = InstalledAppFlow.from_client_secrets_file(
#             client_secrets_file, SCOPES)
#         credentials = flow.run_local_server(port=0)
        
#         # Save credentials for future use
#         with open('token.json', 'w') as token:
#             token.write(credentials.to_json())
    
#     return credentials