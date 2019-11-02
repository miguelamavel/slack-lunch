from typing import Sequence

import slack

from dish import Dish


class SlackClient:
    def __init__(self, slack_access_token, slack_channel):
        self.slack_channel = slack_channel
        self.client = slack.WebClient(token=slack_access_token)

        self.menu_attachments = []

    def add_menu(self, restaurant, dish_array: Sequence[Dish], restaurant_icon=None, color=None):
        message = restaurant_icon + ' ' if restaurant_icon else None
        message = message + '*%s*\n\n' % restaurant

        for dish in dish_array:
            message = message + '%s\n%s\n\n' % (dish.title, dish.price)

        if not dish_array:
            message = message + '\nNo menu available'

        self.menu_attachments.append(
            {
                "text": message,
                "fallback": "Fallback",
                "color": color if color else "#233625",
                "attachment_type": "default"
            }
        )

    def write_menu(self):
        self.client.chat_postMessage(
            **{
                "channel": self.slack_channel,
                "text": "Menus",
                "attachments": self.menu_attachments
            })

