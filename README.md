# Slackbot Template

This is a template for a Slack Bot
running with Amazon Web Services Comprehend


## 1. Setup

1. Install Python 3.x and Git.
   On CentOS / Amazon Linux / etc, the command would be:

```bash
sudo yum install python36 python36-pip git
```

2. Clone this Github repository

```bash
git clone https://github.com/nathanielng/slackbot-template.git
```

3. Create a virtual environment (optional)

```bash
python3 -m pip install --user virtualenv
virtualenv -p python3 slackbot-env
source slackbon-env/bin/activate
```

4. Install Python Libraries

```bash
python3 -m pip install -r requirements.txt
```

5. Create a Slack App

Go to the [Slack dashboard](https://api.slack.com/apps)
for your app(s) and

- Install the App to a Slack channel
- Under Event Subscriptions, look for the
  "Subscribe to Workspace Events" section.
  Add the Workspace Event: "message.channels"
- Under the Bot Users section,
  Create a bot user 
- Get the bot token for your Slack App.
  You will need it in the next section.

6. Add tokens:

For geocoding using Bing Maps, a
[Bing API Key](https://docs.microsoft.com/en-us/bingmaps/getting-started/bing-maps-dev-center-help/getting-a-bing-maps-key)
may be obtained.

Add the Slack bot token and
Bing API key to `~/.bash_profile` as follows:

```bash
export SLACK_BOT_TOKEN="your Slack bot token here"
export BING_API_KEY="your Bing API key here"
```

7. In the Amazon AWS Console, create an IAM admin user.
 
   Add the credentials for the IAM user to `~/.aws/config`:

```
[profile adminuser]
aws_access_key_id = _my_access_key_here_
aws_secret_access_key = _put_iam_user_secret_access_key_here_
region = _put_the_aws_region_here_
```

## 2. Running the Bot

```bash
screen -S slackbot
cd src/
python3 bot.py --run
```

Type Ctrl-A, Ctrl-D to exit the screen session.
If this was done on a remote server (e.g. Amazon EC2),
it is now safe to log out from the server.

To get back to the screen session, type

```bash
screen -r slackbot
```

## 3. Using the Bot

To use the bot, @mention the bot with a message in
any Slack channel where the bot has been added.

For example, type:

```
@bot_user_name message_to_bot
```

where `@bot_user_name` should be replaced by the user name of the bot.

