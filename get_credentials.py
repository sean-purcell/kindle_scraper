# obtained from https://developers.google.com/gmail/api/quickstart/python
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

def main():
    flow = InstalledAppFlow.from_client_secrets_file("project_credentials.json", SCOPES)
    creds = flow.run_local_server()
    # Save the credentials for the next run
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

if __name__ == "__main__":
    main()
