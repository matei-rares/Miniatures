from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define the Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

#todo vezi aici daca merge

# Authenticate and build the Gmail service
def authenticate_gmail():
    creds = None
    # Token file stores user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


# Get a list of emails from the "Updates" or "Promotions" categories
def list_emails(service, category_label):
    results = service.users().messages().list(
        userId='me',
        labelIds=[category_label],
        q='category:{}'.format(category_label.lower())
    ).execute()
    messages = results.get('messages', [])
    return messages


# Delete emails based on message IDs
def delete_emails(service, messages):
    for message in messages:
        try:
            service.users().messages().delete(userId='me', id=message['id']).execute()
            print(f"Deleted email with ID: {message['id']}")
        except Exception as e:
            print(f"An error occurred while deleting email {message['id']}: {e}")


# Main function
def main():
    service = authenticate_gmail()

    # Specify categories to clean
    categories = ['CATEGORY_UPDATES', 'CATEGORY_PROMOTIONS']

    for category in categories:
        print(f"Fetching emails from {category}...")
        messages = list_emails(service, category)

        if not messages:
            print(f"No emails found in {category}.")
            continue

        print(f"Found {len(messages)} emails in {category}. Deleting them...")
        delete_emails(service, messages)

    print("Email cleanup complete!")


if __name__ == '__main__':
    main()
