import log
from constants import countries

logger = log.get_logger()


def format_slack(event) -> dict:
    region_emoji = f":flag-{event['eventCountryFlag']}:"

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":bell: New event on vlr.gg",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*<{event['eventUrl']}|{event['eventName']}>*",
                },
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f":alarm_clock: *STATUS*\n{event['eventStatus'].capitalize()}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f":calendar: *DATES*\n{event['dates']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f":world_map: *REGION*\n{region_emoji} {countries[event['eventCountryFlag']]}",
                    },
                ],
                "accessory": {
                    "type": "image",
                    "image_url": event["eventLogoUrl"],
                    "alt_text": "event logo",
                },
            },
        ]
    }

    return payload


def format_discord(event) -> dict:
    # region emoji
    if event["eventCountryFlag"] == "un":
        region_emoji = ":united_nations:"
    else:
        region_emoji = f":flag_{event['eventCountryFlag']}:"

    payload = {
        "embeds": [
            {
                "title": event["eventName"],
                "url": event["eventUrl"],
                "color": 394046,
                "footer": {"text": "new event on vlr.gg"},
                "thumbnail": {"url": event["eventLogoUrl"]},
                "fields": [
                    {
                        "name": ":alarm_clock: STATUS",
                        "value": event["eventStatus"].capitalize(),
                        "inline": True,
                    },
                    {
                        "name": ":calendar: DATES",
                        "value": event["dates"],
                        "inline": True,
                    },
                    {
                        "name": ":earth_americas: REGION",
                        "value": f"{region_emoji} {countries[event['eventCountryFlag']]}",
                        "inline": True,
                    },
                ],
            }
        ],
    }

    return payload
