from channels.generic.websocket import AsyncJsonWebsocketConsumer


class LiveUpdatesConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = 'live_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def broadcast_update(self, event):
        await self.send_json(event['payload'])
