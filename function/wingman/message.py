import json
import os

import log
from constants import countries

logger = log.getLogger()


def format_slack(event) -> str:
    region_emoji = ":flag-{}:".format(event["eventCountryFlag"])

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
                        "text": "*<{}|{}>*".format(
                            event["eventUrl"], event["eventName"]
                        ),
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": ":world_map: *REGION*\n {} {}".format(
                                region_emoji, countries[event["eventCountryFlag"]]
                            ),
                        },
                        {
                            "type": "mrkdwn",
                            "text": ":calendar: *DATES*\n {}".format(event["dates"]),
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
        region_emoji = ":flag_{}:".format(event["eventCountryFlag"])

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
                            "name": ":earth_americas: REGION",
                            "value": "{} {}".format(
                                region_emoji, countries[event["eventCountryFlag"]]
                            ),
                            "inline": True,
                        },
                        {
                            "name": ":calendar: DATES",
                            "value": event["dates"],
                            "inline": True,
                        },
                    ],
                }
            ],
        }
    )

    return data
