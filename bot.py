import argparse
import aws_comprehend as ac
import json
import os
import slackclient
import time


class MySlackClass:
    """A class for handling Slack Calls"""


    def __init__(self, token=None):
        if token is None:
            if 'SLACK_BOT_TOKEN' not in os.environ:
                print('SLACK_BOT_TOKEN has not been defined as an environment variable')
                quit()
            self._token = os.environ.get('SLACK_BOT_TOKEN')
        else:
            self._token = token
        self._slack_client = slackclient.SlackClient(self._token)


    def api_call(self, *args, **kwargs):
        return self._slack_client.api_call(*args, **kwargs)


    def bot_userid(self):
        return self.api_call('auth.test')['user_id']


    def get_channels(self):
        result = self.api_call("channels.list")
        if result.get('ok'):
            return result['channels']


    def list_channels(self):
        channels = self.get_channels()
        for channel in channels:
            # print(channel)
            print('{id} "{name}": Purpose - {purpose}'.format(**channel))


    def send_message(self, channel_id, message):
        result = self._slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            username='pythonbot',
            icon_emoji=':robot_face:'
        )
        return result


    def parse_commands(self, events, LEM=None):
        for event in events:
            if event['type'] == 'message' and not 'subtype' in event:
                user_id = event['user']
                msg = event['text']
                channel = event['channel']
                print(f'User: {user_id}@{channel}, msg="{msg}"')
                if LEM is not None:
                    txt = LEM.get_entities(msg)
                    print(f'Text: {txt}')
                    self.send_message(channel, txt)


    def run(self, LEM=None, delay=1):
        if self._slack_client.rtm_connect(with_team_state=False) is False:
            print('Connection failed')
            quit()

        bot_id = self.bot_userid()
        print(f'Bot (ID={bot_id}) is now running ', end='')
        print(f'on `slackclient` version {slackclient.version.__version__}')
        while True:
            events = self._slack_client.rtm_read()
            print(events)
            if len(events) > 0:
                self.parse_commands(events, LEM)
            time.sleep(delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_test', action='store_true')
    parser.add_argument('--channels', action='store_true')
    parser.add_argument('--message', default='')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--userid', action='store_true')
    args = parser.parse_args()

    SC = MySlackClass()

    if args.api_test is True:
        # python3 bot.py --api_test
        result = SC.api_call('api.test')
        txt = json.dumps(result, indent=4)
        print(txt)
    elif args.channels is True:
        # python3 bot.py --channels
        txt = SC.list_channels()
        print(txt)
    elif len(args.message) > 0:
        # python3 bot.py --message "Hello"
        my_channel = 'CGRBJFKPH'
        result = SC.send_message(my_channel, args.message)
    elif args.userid is True:
        # python3 bot.py --userid
        print(f'Bot userid = {SC.bot_userid()}')
    elif args.run is True:
        # python3 bot.py --run
        LEM = ac.LanguageEngineMedical('us-west-2')
        SC.run(LEM)

