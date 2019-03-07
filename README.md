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

5. Add the bot token to `~/.bash_profile`

export SLACK_BOT_TOKEN="your Slack bot token here"


## 2. Running the Bot

```bash
screen -S slackbot
python3 bot.py --run
```

Type Ctrl-A, Ctrl-D to exit the screen session.
If this was done on a remote server (e.g. Amazon EC2),
it is now safe to log out from the server.

To get back to the screen session, type

```bash
screen -r slackbot
```
