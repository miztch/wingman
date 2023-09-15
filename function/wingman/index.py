import requests

import database
import log
import notify
import scrape


def lambda_handler(event, context) -> None:
    logger = log.getLogger()

    # get events from vlr.gg
    vlr_events = scrape.events()

    # get events from DynamoDB table
    saved_events = database.get_saved_events()

    # update DynamoDB table with "upcoming" events
    database.put_events(vlr_events["upcoming"])

    # delete events "started" or "completed" if in DynamoDB table
    events_delete: list = []
    for vlr_event in vlr_events["ongoing"] + vlr_events["completed"]:
        if vlr_event["id"] in [saved_event["id"] for saved_event in saved_events]:
            events_delete.append(vlr_event)
    database.delete_events(events_delete)

    # notify to channel if new event
    for vlr_event in vlr_events["upcoming"]:
        if vlr_event["id"] not in [saved_event["id"] for saved_event in saved_events]:
            try:
                notify.send(vlr_event)
            except:
                # rollback if notifying fails
                database.delete_events([vlr_event])
