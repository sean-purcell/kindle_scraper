import asyncio
from aiogoogle import Aiogoogle, GoogleAPI
from aiogoogle.auth.creds import ClientCreds, UserCreds
import base64
import bs4
import json

import scraper.util
import scraper.flags

AUTHOR = "Erratic Errata"

def _get_user_creds(creds):
    return UserCreds(
        access_token=creds.token,
        refresh_token=creds.refresh_token,
        expires_at=creds.expiry.isoformat(),
        scopes=creds.scopes,
    )

def _get_client_creds(creds):
    return ClientCreds(
        client_id=creds.client_id,
        client_secret=creds.client_secret,
        scopes=creds.scopes,
    )

async def _get_email_ids(session, gmail):
    def _get_query():
        queries = [
            "from:bing@patreon.com",
            'subject:"ErraticErrata just shared"',
            "newer_than:14d",
        ]

        return " ".join(queries)
    messages = []
    pageToken = None
    while True:
        response = await session.as_user(
            gmail.users.messages.list(userId="me", q=_get_query(), pageToken=pageToken)
        )
        if "messages" not in response:
            break
        messages.extend(response["messages"])
        if "nextPageToken" not in response:
            break
        pageToken = response["nextPageToken"]

    return [message["id"] for message in messages]

async def _get_email(session, gmail, key):
    response = await session.as_user(gmail.users.messages.get(userId="me", id=key))

    ts = int(response["internalDate"])

    subject = [
        hdr["value"]
        for hdr in response["payload"]["headers"]
        if hdr["name"] == "Subject"
    ][0]

    # part 1 is the html one
    b64 = response["payload"]["parts"][1]["body"]["data"]

    html = base64.urlsafe_b64decode(b64).decode("utf-8")

    soup = bs4.BeautifulSoup(html, features="lxml")
    a1 = soup.find("td", "contents")
    a2 = soup.find("td", "body-copy")
    article = a2 if a2 else a1
    article = str(article.decode_contents())

    return (subject, article, ts)

async def _get_after(creds, gmail, timestamp):
    async with Aiogoogle(
        user_creds=_get_user_creds(creds), client_creds=_get_client_creds
    ) as session:
        print(f"Getting emails")

        ids = await _get_email_ids(session, gmail)
        print(f"Found {len(ids)} ids")

        emails = await asyncio.gather(*(_get_email(session, gmail, key) for key in ids))
        print(f"Scraped {len(emails)} emails")

        filtered = [email for email in emails if email[2] > timestamp]
        print(f"Found {len(filtered)} new emails")

        return filtered

def scrape(state, creds):
    timestamp = state.get("timestamp", 0)

    discovery = json.loads(open(scraper.flags.get_flags().gmail_discovery, 'rb').read())
    gmail = GoogleAPI(discovery)

    emails = asyncio.run(_get_after(creds, gmail, timestamp))

    return (
        [
            (subject, scraper.util.format_chapter(subject, html, AUTHOR))
            for (subject, html, _) in emails
        ],
        {"timestamp": max(0, timestamp, *[ts for (_, _, ts) in emails])},
    )
