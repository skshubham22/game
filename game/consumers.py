import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'game_%s' % self.room_code

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'join_game':
            await self.join_game(text_data_json)
        elif message_type == 'make_move':
            await self.make_move(text_data_json)
        
    async def join_game(self, data):
        # Logic to assign player to a side (X or O)
        # This is simplified; ideally we check session or user ID
        side = await self.assign_player_side()
        
        # Send initial state to the joining player
        await self.send(text_data=json.dumps({
            'type': 'game_start',
            'side': side,
            'game_state': await self.get_game_state()
        }))
        
        # Broadcast the new player list/state to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',
                'game_state': await self.get_game_state()
            }
        )
        
    async def make_move(self, data):
        index = data['index']
        player = data['player']
        
        # Validate move and update state
        valid_move = await self.update_game_state(index, player)
        
        if valid_move:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'game_update',
                    'game_state': await self.get_game_state()
                }
            )

    # Receive message from room group
    async def game_update(self, event):
        game_state = event['game_state']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'game_state': game_state
        }))

    @database_sync_to_async
    def get_game_state(self):
        room = Room.objects.get(code=self.room_code)
        return room.game_state

    @database_sync_to_async
    def assign_player_side(self):
        room = Room.objects.get(code=self.room_code)
        state = room.game_state
        players = state.get('players', {})
        
        player_id = self.scope['session'].session_key
        # Fallback for dev/testing without session cookies
        if not player_id:
             player_id = self.channel_name

        player_name = self.scope['session'].get('player_name', 'Unknown Player')
        
        if player_id in players:
            # Update name if changed
            players[player_id]['name'] = player_name
            room.game_state = state
            room.save()
            return players[player_id]['side']
        
        # Determine side
        if 'X' not in [p['side'] for p in players.values()]:
            side = 'X'
        elif 'O' not in [p['side'] for p in players.values()]:
            side = 'O'
        else:
            side = 'SPECTATOR'
            
        players[player_id] = {
            'side': side,
            'name': player_name
        }
            
        room.game_state = state
        room.save()
        return side

    @database_sync_to_async
    def update_game_state(self, index, player):
        room = Room.objects.get(code=self.room_code)
        state = room.game_state
        board = state['board']
        turn = state['turn']
        winner = state['winner']
        
        if winner or board[index] is not None or turn != player:
            return False
            
        board[index] = player
        
        # Check for winner
        if self.check_winner(board, player):
            # Find player name
            winner_name = player
            for p_id, p_data in state['players'].items():
                if p_data['side'] == player:
                    winner_name = p_data['name']
                    break
            state['winner'] = winner_name
        elif all(cell is not None for cell in board):
            state['winner'] = 'DRAW'
        else:
            state['turn'] = 'O' if player == 'X' else 'X'
            
        room.game_state = state
        room.save()
        return True

    def check_winner(self, board, player):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Cols
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]
        return any(all(board[i] == player for i in condition) for condition in win_conditions)
