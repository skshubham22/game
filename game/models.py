from django.db import models
import random
import string

class Room(models.Model):
    GAME_TYPES = (
        ('TIC_TAC_TOE', 'Tic Tac Toe'),
        ('LUDO', 'Ludo'),
    )
    
    code = models.CharField(max_length=8, unique=True, blank=True)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES, default='TIC_TAC_TOE')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Store game state as JSON (simplifies handling different game types)
    # For Tic-Tac-Toe: {'board': [null]*9, 'turn': 'X', 'winner': null}
    game_state = models.JSONField(default=dict, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        if not self.game_state:
            if self.game_type == 'TIC_TAC_TOE':
                self.game_state = {
                    'board': [None] * 9,
                    'turn': 'X',
                    'winner': None,
                    'players': {} # session_key: 'X' or 'O'
                }
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.game_type} - {self.code}"
