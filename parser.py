# parser.py

from Match import Match, Game, Move, DiceRoll, Action, CubeAction

def parse_match_from_text(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    match = None
    current_game = None

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        # Adiciona print para debugging
        print(f"Parsing line {line_number}: {line}")

        # Parse metadata do match
        if line.startswith("; [Site "):
            site = line.split('"')[1]
        elif line.startswith("; [Match ID "):
            match_id = line.split('"')[1]
        elif line.startswith("; [Player 1 "):
            player1 = line.split('"')[1]
        elif line.startswith("; [Player 2 "):
            player2 = line.split('"')[1]
        elif line.startswith("; [EventDate "):
            event_date = line.split('"')[1]
        elif line.startswith("; [EventTime "):
            event_time = line.split('"')[1]
        elif line.startswith("; [Variation "):
            variation = line.split('"')[1]
        elif line.startswith("; [Crawford "):
            crawford = line.split('"')[1] == 'On'
        elif line.startswith("; [CubeLimit "):
            cube_limit = int(line.split('"')[1])

        # Inicializar o match quando os metadados estiverem completos
        if not match and line == "7 point match":
            match = Match(player1, player2, 7)
            match.metadata.update({
                'site': site,
                'match_id': match_id,
                'date': event_date,
                'time': event_time,
                'variation': variation,
                'crawford': crawford,
                'cube_limit': cube_limit,
            })

        # Parsear novos jogos
        elif line.startswith("Game "):
            if current_game:
                match.games.append(current_game)
            current_game = Game()

        # Parsear movimentos
        elif line and ')' in line:
            move_number, move_text = line.split(')', 1)
            move_text = move_text.strip()

            # Dividir jogadas dos dois jogadores
            player_moves = move_text.split("                        ")  # separador entre as jogadas dos jogadores

            for player_move_text in player_moves:
                if ':' in player_move_text:
                    dice_roll, actions = player_move_text.split(':', 1)
                    dice_roll = dice_roll.strip()

                    # Certifique-se de que o dado contém dois números válidos
                    if dice_roll.replace(' ', '').isdigit():
                        die1, die2 = map(int, dice_roll)
                    else:
                        print(f"Skipping invalid dice roll on line {line_number}: {dice_roll}")
                        continue  # Se não for um lançamento de dados válido, ignora esta linha

                    # Identificar o jogador
                    player = player1 if "mjales" in player_move_text else player2
                    move = Move(player=player)
                    move.dice_roll = DiceRoll(die1, die2)

                    # Processar ações
                    if "Cannot Move" in actions:
                        move.cannot_move = True
                    else:
                        actions = actions.strip().split()
                        for action_text in actions:
                            if '/' in action_text:
                                # Verificar se há múltiplas ações no mesmo ponto, ex.: '20(3)'
                                if '(' in action_text:
                                    base_action, count = action_text.split('(')
                                    count = int(count.rstrip(')'))  # Remover o parêntese
                                else:
                                    base_action = action_text
                                    count = 1  # Movimento único

                                from_point, to_point = base_action.split('/')
                                from_point = 25 if from_point == 'bar' else int(from_point)
                                to_point = 0 if to_point == 'off' else int(to_point.strip('*'))
                                is_hit = '*' in action_text

                                # Adicionar a ação múltiplas vezes, se necessário
                                for _ in range(count):
                                    move.actions.append(Action(from_point, to_point, is_hit))

                    current_game.moves.append(move)

        # Parsear ações do cubo
        elif "Doubles" in line:
            cube_action = CubeAction(action_type='double', new_value=2)
            current_game.moves[-1].cube_action = cube_action
        elif "Takes" in line:
            current_game.moves[-1].cube_action.response = 'take'
        elif "Drops" in line:
            current_game.moves[-1].cube_action.response = 'pass'

        # Verificar o vencedor e os pontos ganhos
        elif "Wins" in line:
            winner, points_won = line.split(' Wins ')
            points_won = int(points_won.split()[0])
            current_game.winner = winner.strip()
            current_game.points_won = points_won

    if current_game:
        match.games.append(current_game)

    return match
