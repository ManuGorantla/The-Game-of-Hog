"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100 




def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'

    count = 0
    total = 0

    while(count < num_rolls):
        currentValue = dice()

        if (currentValue != 1):
            total += currentValue
        else:
            total = 1
            
            while(count + 1 < num_rolls):
                currentValue = dice()
                count += 1
    
        count += 1

    return total



        

        




def boar_brawl(player_score, opponent_score):
    """Return the points scored by rolling 0 dice according to Boar Brawl.
    """
    "*** YOUR CODE HERE ***"

    score = 3 * abs(((opponent_score // 10)%10) - (player_score % 10))
    if score > 1:
        return score
    else:
        return 1



def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
 

    if num_rolls == 0:
        return boar_brawl(player_score, opponent_score)
    else:
        return roll_dice(num_rolls, dice)




def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

def is_prime(n):
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """Return the number of factors of N, including 1 and N itself."""

    x = 1
    count = 0
    while x <= n:
        if(n % x == 0):
            count = count + 1
        x+=1
    return count


def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule."""
    

    if num_factors(score) == 3 or num_factors(score) == 4:
        while num_factors(score) != 2:
            score += 1
    return score


def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    """

    score = sus_points(simple_update(num_rolls, player_score, opponent_score, dice))
    return score
    


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

   
    """
    who = 0  

    while (score0 < goal and score1 < goal):
        if (who == 0):
            turns0 = strategy0(score0, score1)
            count0 = 0
            score0 = update(turns0, score0, score1, dice)
            who = 1
        else:
            turns1 = strategy1(score1, score0)
            count1 = 0
            score1 = update(turns1, score1, score0, dice)
            who = 0

    return score0, score1





def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    
    """
    assert n >= 0 and n <= 10
    "*** YOUR CODE HERE ***"

    def strategy(score0, score1):
        return n

    return strategy



def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

  
    """

    roll = strategy(0, 0)
    player_score, opponent_score = 0, 0
    while player_score <= goal:
        while opponent_score <= goal:
            if(strategy(player_score, opponent_score)) != roll:
                return False
            opponent_score += 1
        opponent_score = 0
        player_score += 1
        
    return True

    
    
    
    
   

        


    
    


def make_averaged(original_function, times_called=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TIMES_CALLED times.


  
    """

    
    
    def func(*args):
        n = times_called
        total = 0
        while n > 0:
            total += original_function(*args)
            n -= 1
        return total / times_called
    return func


def max_scoring_num_rolls(dice=six_sided, times_called=1000):
    """Return the number of dice (1 to 10) that gives the maximum average score for a turn.
    Assume that the dice always return positive outcomes.
    """
    n = 10
    great = 0
    element = 0
    while n >= 1:
        greatest = make_averaged(roll_dice)(n, dice)
        if greatest >= great:
            great = greatest
            element = n 
        n -= 1
    return element


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) 
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.
    """
    if boar_brawl(score, opponent_score) >= threshold:
        return 0
    return num_rolls 


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    if sus_points(score + boar_brawl(score, opponent_score)) - score >= threshold:
        return 0
    return num_rolls  


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    """
    return 6  




@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
