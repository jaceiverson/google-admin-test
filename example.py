import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import pandas as pd
from rich import print as rprint


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/admin.reports.audit.readonly"]


def authenticate():
    """
    https://developers.google.com/admin-sdk/reports/v1/quickstart/python
    Shows basic usage of the Admin SDK Reports API.
    Prints the time, email, and name of the last 10 login events in the domain.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("admin", "reports_v1", credentials=creds)


def get_drive_events(service):
    """_summary_: gets the drive events
    https://developers.google.com/admin-sdk/reports/v1/appendix/activity/drive

    """
    return (
        service.activities()
        .list(
            applicationName="drive",
            eventName="create",
            userKey="all",
            maxResults=10,
        )
        .execute()
    )


def parse_params(data):
    return pd.Series({x["name"]: x.get("value", x.get("boolValue")) for x in data})


def parse_json_response(response):
    """_summary_: parses the response"""
    df = pd.json_normalize(response.get("items"), max_level=10)
    events = pd.json_normalize(pd.json_normalize(df["events"])[0])
    params = events.parameters.apply(parse_params)
    events.columns = [f"event.{x}" for x in events.columns]
    params.columns = [f"parameter.{x}" for x in params.columns]

    return df.join(events).join(params).drop(["events", "event.parameters"], axis=1)


def main():
    service = authenticate()
    resp = get_drive_events(service)
    df = parse_json_response(resp)


if __name__ == "__main__":
    main()
