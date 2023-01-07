from random import Random
from random import choice
from game.game_state import GameState
import game.character_class

from game.item import Item

from game.position import Position
from strategy.strategy import Strategy

class StarterStrategy(Strategy):
    def strategy_initialize(self, my_player_index: int):
        return game.character_class.CharacterClass.WIZARD

    def move_action_decision(self, game_state: GameState, my_player_index: int) -> Position:
        x = game_state.player_state_list[my_player_index].position.x
        y = game_state.player_state_list[my_player_index].position.y
        if (x < 5 and y < 5): #center at (4, 4) spawn (0, 0)
            if (x + 2 <= 4):
                x = x + 2
                y = y + 1
                return Position(x, y)
            if (y + 2 <= 4):
                x = x + 1
                y = y + 2
                return Position(x, y)
        if (x < 5 and y > 5): #center at (4, 5) spawn (0, 9)
            if (x + 2 <= 4):
                x = x + 2
                y = y - 1
                return Position(x, y)
            if (y - 2 >= 5):
                x = x + 1
                y = y - 2
                return Position(x, y)
        if (x > 5 and y < 5): #center at (5, 4) spawn (9, 0)
            if (x - 2 >= 5):
                x = x - 2
                y = y + 1
                return Position(x, y)
            if (y + 2 <= 4):
                x = x - 1
                y = y + 2
                return Position(x, y)
        if (x >= 5 and y >= 5): #center at (5, 5) spawn (9, 9)
            if (x - 2 >= 5):
                x = x - 2
                y = y - 1
                return Position(x, y)
            if (y - 2 >= 5):
                x = x - 1
                y = y - 2
                return Position(x, y)
        return Position(x, y)

    def attack_action_decision(self, game_state: GameState, my_player_index: int) -> int:
        valid_players = {}
        us = None
        for i, player in enumerate(game_state.player_state_list) :
            if (i != my_player_index) :
                valid_players[i] = player
            else :
                us = player
        victims = []
        our_x = us.position.x
        our_y = us.position.y
        for idx in valid_players.keys():
            current_player = valid_players[idx]
            their_x = current_player.position.x
            their_y = current_player.position.y
            if (abs(our_x - their_x) <= 2 and abs(our_y - their_y) <= 2):
                victims.append(idx)
        if len(victims) == 0:
            return (my_player_index + 1) % 4
        if len(victims) <= 1:
            return victims[0]
        else:
            damage = 5
            if us.item == Item.RALLY_BANNER:
                damage = 7
            for victim in victims:
                if valid_players[victim].health <= damage:
                    return victim
            return choice(victims)

    def buy_action_decision(self, game_state: GameState, my_player_index: int) -> Item:
        if (game_state.player_state_list[my_player_index].gold >= 8 and game_state.player_state_list[my_player_index].item != Item.HUNTER_SCOPE):
            return Item.RALLY_BANNER
        return Item.NONE

    def use_action_decision(self, game_state: GameState, my_player_index: int) -> bool:
        return False