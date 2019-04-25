import base64
import pickle
import os.path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

import scraper.flags

flags = scraper.flags.get_flags()

def get_creds(token_file):
    SCOPE_PREFIX = "https://www.googleapis.com/auth/gmail."
    SCOPES = [f"{SCOPE_PREFIX}{scope}" for scope in ["readonly", "send"]]

    creds = None
    if not os.path.exists(token_file):
        raise RuntimeError(f"Cache {token_file} not found")
    with open(token_file, "rb") as token:
        creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        if not creds or not creds.valid:
            raise RuntimeError("Invalid credentials")
    return creds

def send_html(creds, name, content):
    message = MIMEMultipart()
    message["to"] = flags.dst_address
    message["from"] = flags.src_address
    message["subject"] = name

    fname = f"{name}.html"
    base = MIMEText(f"{name} is attached")
    message.attach(base)

    attachment = MIMEText(content, "html")
    attachment.add_header("Content-Disposition", "attachment", filename=fname)

    message.attach(attachment)

    mail = {
        "raw": base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode(
            "ascii"
        )
    }

    service = build("gmail", "v1", credentials=creds)
    service.users().messages().send(userId="me", body=mail).execute()
