import pickle
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

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
