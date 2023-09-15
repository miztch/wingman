# wingman

> "Go get 'em, buddy!"

Lambda Function notifies the specific discord/slack channel of new Valorant events added on vlr.gg.

## Provisioning

- In advance, you have to create an incoming webhook in the channel you want to notify, and get its URL.
  - [Discord](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
  - [Slack](https://api.slack.com/messaging/webhooks)
- You can use [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) to provision this application.

```bash
sam build
sam deploy --guided --capabilities CAPABILITY_IAM
```

## Disclaimer

This project is not affiliated with vlr.gg nor Riot Games. All product names, logos, and brands are property of their respective owners.