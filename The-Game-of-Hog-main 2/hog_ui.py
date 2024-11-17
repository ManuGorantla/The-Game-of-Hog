from hog import *



def play_and_print(strategy0, strategy1):
    """Simulate a game and print out what happened during the simulation."""
    final0, final1 = play(printing_strategy(0, strategy0),
                          printing_strategy(1, strategy1),
                          sus_update_and_print, 0, 0,
                          printing_dice(six_sided))
    print('The final score is Player 0:', final0, 'vs Player 1:', final1)


def printing_strategy(who, strategy):
    """Return a strategy that also prints the player's score and choice.

    
    """
    assert who == 0 or who == 1, 'the player must be 0 or 1'

    def choose_and_print(score, opponent_score):
        "A strategy function that also prints."
        if who == 0:
            score0, score1 = score, opponent_score
        else:
            score0, score1 = opponent_score, score
        num_rolls = strategy(score, opponent_score)
        print('The score is', score0, 'to', score1, 'and Player', who,
              'rolls', num_rolls, 'dice...')
        return num_rolls
    return choose_and_print


def printing_dice(dice):
    """Return a dice function that also prints the outcome and a space."""
    def dice_and_print():
        "A dice function that also prints."
        outcome = dice()
        print(outcome, end=' ')
        return outcome
    return dice_and_print


def sus_update_and_print(num_rolls, player_score, opponent_score, dice):
    """Return the updated score, print out the score update, and print when
    Sus Fuss is triggered.

  
    """
    print('  [', end=" ")
    turn_score = take_turn(num_rolls, player_score, opponent_score, dice)  
    print('] =>', turn_score, end='; ')
    print(player_score, '+', turn_score, '=', player_score + turn_score, end='')
    score = turn_score + player_score
    sus_score = sus_points(score)
    if sus_score != score:
        score = sus_score
        print(' triggering **Sus Fuss**, increasing to', score)
    else:
        print() 
    return score





def get_int(prompt, lower, upper):
    """Returns an integer i such that i >= lower and i <= upper."""
    choice = input(prompt)
    while not choice.isnumeric() or int(choice) < lower or int(choice) > upper:
        print('Please enter an integer from', lower, 'to', upper)
        choice = input(prompt)
    return int(choice)


def interactive_strategy(who):
    """Returns a strategy for which the user provides the number of rolls."""
    def strategy(score, opponent_score):
        print('Player', who, ', you have', score, 'and your opponent has', opponent_score)
        choice = get_int('How many dice will you roll? ', 0, 10)
        return choice
    return strategy




def play_with(num_players):
    """Plays a game with NUM_PLAYERS interactive (human) players."""
    if num_players == 0:
        play_and_print(always_roll_5, always_roll_5)
    elif num_players == 1:
        play_and_print(interactive_strategy(0), always_roll_5)
    elif num_players == 2:
        play_and_print(interactive_strategy(0), interactive_strategy(1))
    else:
        print('num_players must be 0, 1, or 2.')


@main
def run(*args):
    """Select number of players and play a game."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--num_players', '-n', type=int, default=0,
                        help='How many interactive players (0, 1, or 2)')
    args = parser.parse_args()
    play_with(args.num_players)
