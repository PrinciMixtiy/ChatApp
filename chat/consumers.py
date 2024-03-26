from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from django.template.loader import get_template
from django.contrib.auth import get_user_model

import json

from .models import Message

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.recv_id = self.scope['url_route']['kwargs']['recv_id']
        self.receiver = User.objects.get(pk=self.recv_id)
        self.user = self.scope['user']
        name_list = sorted([self.receiver.username, self.user.username])
        self.group_name = "_".join(name_list)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        message = Message.objects.create(author=self.user, to=self.receiver, content=message)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {'type': 'send_message', 'message': message}
        )

    def send_message(self, event):
        message = event['message']
        template_name = ''

        if message.author == self.user:
            template_name = 'chat/partials/message-sent.html'
        elif message.author == self.receiver:
            template_name = 'chat/partials/message-received.html'

        html = get_template(template_name).render(
            context={
                'message': message
            }
        )

        self.send(text_data=html)
