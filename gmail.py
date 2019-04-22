import pickle
import os.path
from googleapiclient.discovery import build


def get_creds(cache):
    SCOPE_PREFIX = 'https://www.googleapis.com/auth/gmail.'
    SCOPES = [f'{SCOPE_PREFIX}{scope}' for scope in ['readonly', 'send']]

    creds = None
    if not os.path.exists(cache):
        raise RuntimeError(f'Cache {cache} not found')
    with open(cache, 'rb') as token:
        creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        if not creds or not creds.valid:
            raise RuntimeError('Invalid credentials')
    return creds
