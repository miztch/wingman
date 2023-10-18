import json

import log
from constants import countries

logger = log.getLogger()


def format_slack(event) -> str:
    region_emoji = f":flag-{event['eventCountryFlag']}:"

    data = json.dumps(
        {
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
    )

    return data


def format_discord(event) -> str:
    # region emoji
    if event["eventCountryFlag"] == "un":
        region_emoji = ":united_nations:"
    else:
        region_emoji = f":flag_{event['eventCountryFlag']}:"

    # assemble webhook data
    data = json.dumps(
        {
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
    )

    return data
