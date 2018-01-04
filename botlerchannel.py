from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from flask import Blueprint, request, jsonify

from rasa_core.channels.channel import UserMessage
from rasa_core.channels.direct import CollectingOutputChannel
from rasa_core.channels.custom import HttpInputComponent
from rasa_core.tracker_store import TrackerStore
from util.search import SearchUtil

logger = logging.getLogger(__name__)


class SimpleWebBot(HttpInputComponent):
    """A simple web bot that listens on a url and responds."""

    def blueprint(self, on_new_message):
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/webhook", methods=['POST'])
        def receive():
            payload = request.json
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)
            out = CollectingOutputChannel()
            # processor.MessageProcessor.handleMessage
            on_new_message(UserMessage(text, out, sender_id))
            #tracker_store = TrackerStore()
            #tracker = tracker_store.get_or_create_tracker(sender_id)

            responses = [m for _, m in out.messages]
            recipes = []
            for response in responses:
                search_recipes = SearchUtil.search({'q': response, 'portions': 2, 'fields': 'title,ingress,url,ingredients', 'size': 5})
                if len(search_recipes)>0:
                    recipes.append(search_recipes)

            if len(recipes)>0:
                return jsonify(recipes)
            else:
                return jsonify(responses)

        return custom_webhook