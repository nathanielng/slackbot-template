import boto3
import json
import os
import pandas as pd
import re
import time
from slackclient import SlackClient


if __name__ == "__main__":
    if 'SLACK_BOT_TOKEN' not in os.environ:
        print('SLACK_BOT_TOKEN has not been defined as an environment variable')
        quit()

    token = os.environ.get('SLACK_BOT_TOKEN')
    slack_client = SlackClient(token)

