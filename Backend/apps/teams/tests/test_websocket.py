from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from ..routing import websocket_urlpatterns
from ..models import Team, TeamTip
import json

class TeamWebSocketTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up the application here so it's available for all tests
        cls.application = URLRouter(websocket_urlpatterns)

    async def asyncSetUp(self):
        # Create test user
        self.user = await self.create_user()
        self.team = await self.create_team()

    @staticmethod
    async def create_user():
        User = get_user_model()
        # Use sync_to_async or create in a sync context
        return await User.objects.acreate(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    async def create_team(self):
        return await Team.objects.acreate(
            name='Test Team',
            description='Test Description',
            created_by=self.user
        )

    async def test_websocket_connection(self):
        await self.asyncSetUp()
        communicator = WebsocketCommunicator(
            self.application,
            f'/ws/teams/{self.team.id}/'
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_tip_broadcast(self):
        await self.asyncSetUp()
        # Connect two clients to the same team
        communicator1 = WebsocketCommunicator(
            self.application,
            f'/ws/teams/{self.team.id}/'
        )
        communicator2 = WebsocketCommunicator(
            self.application,
            f'/ws/teams/{self.team.id}/'
        )
        
        await communicator1.connect()
        await communicator2.connect()

        # Send a tip update from client 1
        await communicator1.send_json_to({
            'type': 'tip_update',
            'tip': {
                'content': 'Test tip',
                'author': self.user.id
            }
        })

        # Verify both clients receive the update
        response1 = await communicator1.receive_json_from()
        response2 = await communicator2.receive_json_from()

        self.assertEqual(response1['type'], 'tip_update')
        self.assertEqual(response2['type'], 'tip_update')
        self.assertEqual(response1['tip']['content'], 'Test tip')
        self.assertEqual(response2['tip']['content'], 'Test tip')

        await communicator1.disconnect()
        await communicator2.disconnect() 