class Match:
	def __init__(self, player1, player2, match_length):
		self.metadata = {
			'player1': player1,
			'player2': player2,
			'match_length': match_length,
			'date': None,
			'time': None,
			'variation': 'Backgammon',
			'crawford': True,
			'cube_limit': 1024
		}
		self.games = []

class Game:
	def __init__(self):
		self.moves = []
		self.score_before = {'player1': 0, 'player2': 0}
		self.winner = None
		self.points_won = 0
		self.resignation_type = None  # None, 'single', 'gammon', 'backgammon'

class Move:
	def __init__(self, player):
		self.player = player
		self.dice_roll = None
		self.actions = []
		self.resulting_board_state = None
		self.cube_action = None
		self.cannot_move = False

class DiceRoll:
	def __init__(self, die1, die2):
		self.die1 = die1
		self.die2 = die2

class Action:
	def __init__(self, from_point, to_point, is_hit=False):
		self.from_point = from_point  # 'bar' for entering from bar, 0 for bearing off
		self.to_point = to_point  # 0 for bearing off
		self.is_hit = is_hit

class BoardState:
	def __init__(self):
		self.points = {i: {'player1': 0, 'player2': 0} for i in range(1, 25)}
		self.bar = {'player1': 0, 'player2': 0}
		self.off = {'player1': 0, 'player2': 0}

class CubeAction:
	def __init__(self, action_type, new_value=None):
		self.action_type = action_type  # 'double', 'redouble'
		self.new_value = new_value      # O novo valor do cubo após a ação
		self.response = None  # 'take', 'pass' (pode ser adicionado mais tarde)

class Resignation:
	def __init__(self, player, resignation_type):
		self.player = player
		self.resignation_type = resignation_type  # 'single', 'gammon', 'backgammon'
