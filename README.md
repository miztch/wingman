# wingman

> "Go get 'em, buddy!"

Lambda Function notifies the specific discord channel of new Valorant events added on vlr.gg.

## Provisioning

- In advance, you have to [make a Webhook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) in the channel you want to notify, and get Webhook URL.
- You can use [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) to provision this application.

```bash
sam build
sam deploy --guided --capabilities CAPABILITY_IAM
```

## Disclaimer

This project is not affiliated with vlr.gg nor Riot Games. All product names, logos, and brands are property of their respective owners.