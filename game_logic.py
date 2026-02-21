import random
from constants import SNAKES, LADDERS, BOARD_SIZE

def roll_dice():
    """Returns a random number between 1 and 6."""
    return random.randint(1, 6)

def move_player(position, roll):
    """
    Calculates the new position after a roll.
    Returns (new_position, message, event)
    """
    new_position = position + roll
    message = ""
    event = "normal"

    # 1. Exact win
    if new_position == BOARD_SIZE:
        return new_position, "Landed exactly on 50! 🎉", "win"

    # 2. Overshoot — bounce back
    if new_position > BOARD_SIZE:
        overshoot = new_position - BOARD_SIZE
        new_position = BOARD_SIZE - overshoot
        message = f"Overshot by {overshoot}, bounced back to {new_position}. "
        event = "overshoot"

    # 3. Check for Snakes
    if new_position in SNAKES:
        dest = SNAKES[new_position]
        message += f"Oh no! 🐍 Snake at {new_position}, sliding down to {dest}."
        event = "snake"
        new_position = dest

    # 4. Check for Ladders
    elif new_position in LADDERS:
        dest = LADDERS[new_position]
        message += f"Awesome! 🪜 Ladder at {new_position}, climbing to {dest}."
        event = "ladder"
        new_position = dest

    # 5. Normal Move
    if not message:
        message = f"Moved cleanly to {new_position}."

    return new_position, message, event

def check_extra_turn(roll):
    """Returns True if the player rolled a 6."""
    return roll == 6

def get_initial_stats():
    """Returns a fresh stats dictionary."""
    return {
        "rolls": [],
        "snakes_hit": 0,
        "ladders_climbed": 0,
    }

def update_stats(stats, roll, event):
    """Updates a player's stats based on the turn event."""
    stats["rolls"].append(roll)
    if event == "snake":
        stats["snakes_hit"] += 1
    elif event == "ladder":
        stats["ladders_climbed"] += 1
    return stats

def get_other_player(current_player):
    """Switches turns."""
    return "player_2" if current_player == "player_1" else "player_1"