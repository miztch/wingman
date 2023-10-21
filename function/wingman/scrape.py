import re
import requests
import log
from selectolax.parser import HTMLParser

logger = log.get_logger()


def events() -> dict:
    """
    scrape /events page for upcoming events.
    """

    url = "https://www.vlr.gg/events"
    logger.info("fetch upcoming events list from: %s", url)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }
    resp = requests.get(url, headers=headers)
    html = HTMLParser(resp.text)

    vlr_events: dict = {"upcoming": [], "ongoing": [], "completed": []}

    for item in html.css("a.event-item"):
        event_name = item.css_first(".event-item-inner .event-item-title").text()
        event_name = event_name.replace("\t", "").replace("\n", "")

        event_status = item.css_first(
            ".event-item-desc-item .event-item-desc-item-status"
        ).text()

        dates = item.css_first(".event-item-inner .mod-dates").text()
        dates = dates.replace("\t", "").replace("\n", "").replace("Dates", "")

        country_flag = item.css_first(".event-item-desc-item .flag").attributes["class"]
        country_flag = country_flag.replace(" mod-", "_").replace("flag_", "")

        event_url_path = item.attributes["href"]
        event_url = f"https://vlr.gg{event_url_path}"

        event_id = int(event_url_path.split("/")[2])

        event_logo_path = item.css_first(".event-item-thumb img").attributes["src"]
        if event_logo_path == "/img/vlr/tmp/vlr.png":
            event_logo_path = "vlr.gg" + event_logo_path
        event_logo_path = re.sub(r"^/+", "", event_logo_path)
        event_logo_url = f"https://{event_logo_path}"

        item = {
            "id": event_id,
            "eventName": event_name,
            "dates": dates,
            "eventCountryFlag": country_flag,
            "eventUrl": event_url,
            "eventLogoUrl": event_logo_url,
            "eventStatus": event_status,
        }
        vlr_events[item["eventStatus"]].append(item)

    return vlr_events
