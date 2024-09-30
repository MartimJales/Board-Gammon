# main.py
import sys
from Match import Match, Game, Move, DiceRoll, Action, CubeAction
from format import format_match_to_text
from parser import parse_match_from_text

def create_sample_match():
	# Criar uma instância de uma partida de Backgammon
	match = Match(player1="Jogador 1", player2="Jogador 2", match_length=5)

	# Adicionar metadados
	match.metadata['date'] = '2024-09-26'
	match.metadata['time'] = '10:00'
	match.metadata['site'] = 'Local Online'
	match.metadata['match_id'] = '001'

	# Criar um jogo (Game)
	game = Game()
	game.score_before['player1'] = 0
	game.score_before['player2'] = 0

	# Adicionar movimentos ao jogo
	move1 = Move(player="Jogador 1")
	move1.dice_roll = DiceRoll(3, 5)
	move1.actions.append(Action(from_point=12, to_point=8))
	move1.actions.append(Action(from_point=8, to_point=3, is_hit=True))

	move2 = Move(player="Jogador 2")
	move2.dice_roll = DiceRoll(6, 1)
	move2.actions.append(Action(from_point=13, to_point=7))

	# Adicionar uma ação de cubo com valor
	cube_action = CubeAction(action_type='double', new_value=2)  # O cubo vai para 2
	move2.cube_action = cube_action

	# Adicionar movimentos ao jogo
	game.moves.append(move1)
	game.moves.append(move2)

	# Definir o vencedor e os pontos ganhos
	game.winner = "Jogador 1"
	game.points_won = 1

	# Adicionar o jogo à partida
	match.games.append(game)

	return match


def main(sys_argv):
	# Receber os argumentos do sistema referente ao nome do ficheiro a ser lido
	if len(sys_argv) != 2:
		print("Usage: python main.py <input_file>")
		return

	# Criar um exemplo de partida
	match = parse_match_from_text(sys_argv[1])

	# Formatá-la como texto
	formatted_text = format_match_to_text(match)

	# Guardar a partida formatada num ficheiro txt
	with open('match_log.txt', 'w') as f:
		f.write(formatted_text)

	print("Partida de Backgammon guardada no ficheiro 'match_log.txt'.")

if __name__ == "__main__":
	main(sys_argv=sys.argv)
