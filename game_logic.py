import random
from constants import SNAKES, LADDERS, BOARD_SIZE


def roll_dice():
    """Returns a random number between 1 and 6."""
    return random.randint(1, 6)


def move_player(position, roll):
    """
    Calculates the new position after a roll.
    Returns (new_position, message, event)
    event can be: 'win', 'snake', 'ladder', 'overshoot', or 'normal'
    """
    new_position = position + roll
    message = ""
    event = "normal"

    # Exact win
    if new_position == BOARD_SIZE:
        return new_position, "Reached 50! 🎉", "win"

    # Overshoot — bounce back
    if new_position > BOARD_SIZE:
        overshoot = new_position - BOARD_SIZE
        new_position = BOARD_SIZE - overshoot
        message = f"Overshot! Bounced back to {new_position}. "
        event = "overshoot"

    # Check snakes
    if new_position in SNAKES:
        dest = SNAKES[new_position]
        message += f"🐍 Snake at {new_position}! Slides down to {dest}."
        event = "snake"
        new_position = dest

    # Check ladders
    elif new_position in LADDERS:
        dest = LADDERS[new_position]
        message += f"🪜 Ladder at {new_position}! Climbs up to {dest}."
        event = "ladder"
        new_position = dest

    else:
        message += f"Moved to {new_position}."

    return new_position, message, event


def check_extra_turn(roll):
    """Returns True if the player rolled a 6 and gets an extra turn."""
    return roll == 6


def get_initial_stats():
    """Returns a fresh stats dictionary for one player."""
    return {
        "rolls": [],
        "snakes_hit": 0,
        "ladders_climbed": 0,
    }


def update_stats(stats, roll, event):
    """Updates a player's stats based on what happened this turn."""
    stats["rolls"].append(roll)

    if event == "snake":
        stats["snakes_hit"] += 1
    elif event == "ladder":
        stats["ladders_climbed"] += 1

    return stats


def get_other_player(current_player):
    """Switches between player_1 and player_2."""
    return "player_2" if current_player == "player_1" else "player_1"
