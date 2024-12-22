import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import DenyConnection

logger = logging.getLogger(__name__)

class TeamConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.team_id = self.scope['url_route']['kwargs']['team_id']
            self.team_group_name = f'team_{self.team_id}'
            
            logger.info(f"Attempting WebSocket connection for team {self.team_id}")
            
            # Join team group
            await self.channel_layer.group_add(
                self.team_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Send initial connection confirmation
            await self.send_json({
                'type': 'connection_established',
                'message': f'Connected to team {self.team_id}'
            })
            
            logger.info(f"WebSocket connection established for team {self.team_id}")
            
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}")
            raise DenyConnection()

    async def disconnect(self, close_code):
        try:
            logger.info(f"WebSocket disconnecting for team {self.team_id} with code {close_code}")
            # Leave team group
            await self.channel_layer.group_discard(
                self.team_group_name,
                self.channel_name
            )
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def receive_json(self, content):
        try:
            logger.info(f"Received message: {content}")
            message_type = content.get('type')
            
            if message_type == 'ping':
                await self.send_json({'type': 'pong'})
            elif message_type == 'tip_update':
                await self.channel_layer.group_send(
                    self.team_group_name,
                    {
                        'type': 'tip_update',
                        'tip': content['tip']
                    }
                )
        except Exception as e:
            logger.error(f"Error in receive_json: {str(e)}")

    async def tip_update(self, event):
        try:
            await self.send_json({
                'type': 'tip_update',
                'tip': event['tip']
            })
        except Exception as e:
            logger.error(f"Error in tip_update: {str(e)}")
