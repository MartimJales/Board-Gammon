# format.py

def format_move_to_text(move):
    if move.cannot_move:
        return f"{move.dice_roll.die1}{move.dice_roll.die2}: Cannot Move"

    actions_text = []
    for action in move.actions:
        from_point = 'bar' if action.from_point == 25 else action.from_point
        to_point = 'off' if action.to_point == 0 else action.to_point
        hit_marker = '*' if action.is_hit else ''
        actions_text.append(f"{from_point}/{to_point}{hit_marker}")

    return f"{move.dice_roll.die1}{move.dice_roll.die2}: {' '.join(actions_text)}"

def format_cube_action(cube_action):
    if cube_action.action_type == 'double':
        return f" Doubles => {cube_action.new_value}"
    elif cube_action.action_type == 'take':
        return " Takes"
    elif cube_action.action_type == 'pass':
        return " Drops"
    return ""

def format_game_to_text(game, game_number, player1, player2):
    game_text = []
    game_text.append(f"Game {game_number}")
    game_text.append(f"{player1} : {game.score_before['player1']}                             {player2} : {game.score_before['player2']}")

    for move_number, move in enumerate(game.moves, start=1):
        move_text = f"{move_number:2d}) "
        if move.player == player1:
            move_text += format_move_to_text(move).ljust(35)
        else:
            move_text += " " * 35 + format_move_to_text(move)

        if move.cube_action:
            move_text += format_cube_action(move.cube_action)

        game_text.append(move_text)

    if game.resignation_type:
        game_text.append(f"{game.winner} Wins {game.points_won} point{'s' if game.points_won > 1 else ''} ({game.resignation_type} resignation)")
    else:
        game_text.append(f"{game.winner} Wins {game.points_won} point{'s' if game.points_won > 1 else ''}")

    return "\n".join(game_text)

def format_match_to_text(match):
    match_text = []
    match_text.append(f"; [Site \"{match.metadata['site']}\"]")
    match_text.append(f"; [Match ID \"{match.metadata['match_id']}\"]")
    match_text.append(f"; [Player 1 \"{match.metadata['player1']}\"]")
    match_text.append(f"; [Player 2 \"{match.metadata['player2']}\"]")
    match_text.append(f"; [EventDate \"{match.metadata['date']}\"]")
    match_text.append(f"; [EventTime \"{match.metadata['time']}\"]")
    match_text.append(f"; [Variation \"{match.metadata['variation']}\"]")
    match_text.append(f"; [Crawford \"{match.metadata['crawford']}\"]")
    match_text.append("")
    match_text.append(f"{match.metadata['match_length']} point match")
    match_text.append("")

    # Agora a função format_game_to_text recebe os valores de player1 e player2 e o número do jogo diretamente
    for game_number, game in enumerate(match.games, start=1):
        match_text.append(format_game_to_text(game, game_number, match.metadata['player1'], match.metadata['player2']))
        match_text.append("")

    return "\n".join(match_text)

# Uso:
# formatted_text = format_match_to_text(match)
# with open('match_log.txt', 'w') as f:
#     f.write(formatted_text)
