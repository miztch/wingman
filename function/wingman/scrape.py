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

    vlr_events: dict = {"upcoming": [], "ongoing": [], "paused": [], "completed": []}

    for item in html.css("a.event-item"):
        name_node = item.css_first(".event-item-inner .event-item-title")
        if name_node is None:
            logger.warning("skipping event item: missing title element")
            continue
        event_name = name_node.text().replace("\t", "").replace("\n", "")
        if not event_name:
            logger.warning("skipping event item: empty event name")
            continue

        status_node = item.css_first(
            ".event-item-desc-item .event-item-desc-item-status"
        )
        if status_node is None:
            logger.warning("skipping event '%s': missing status element", event_name)
            continue
        event_status = status_node.text()

        dates_node = item.css_first(".event-item-inner .mod-dates")
        dates = dates_node.text().replace("\t", "").replace("\n", "").replace("Dates", "") if dates_node else ""

        flag_node = item.css_first(".event-item-desc-item .flag")
        if flag_node is None:
            logger.warning("skipping event '%s': missing flag element", event_name)
            continue
        country_flag = flag_node.attributes.get("class", "")
        country_flag = country_flag.replace(" mod-", "_").replace("flag_", "")

        event_url_path = item.attributes.get("href", "")
        event_url = f"https://vlr.gg{event_url_path}"

        event_id = int(event_url_path.split("/")[2])

        logo_node = item.css_first(".event-item-thumb img")
        event_logo_path = logo_node.attributes.get("src", "") if logo_node else ""
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
        if item["eventStatus"] not in vlr_events:
            logger.warning("skipping event '%s': unknown status '%s'", item["eventName"], item["eventStatus"])
            continue
        vlr_events[item["eventStatus"]].append(item)


    return vlr_events
