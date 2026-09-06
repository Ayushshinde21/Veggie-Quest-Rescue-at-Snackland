import json
import os


SAVE_FILE = "savegame.json"


# ==============================================
# SAVE GAME
# ==============================================

def save_game(level):

    # ------------------------------------------
    # LOAD EXISTING SAVE DATA
    # ------------------------------------------

    existing_data = {}

    if os.path.exists(SAVE_FILE):

        try:

            with open(
                SAVE_FILE,
                "r"
            ) as file:

                existing_data = json.load(file)

        except (
            json.JSONDecodeError,
            OSError
        ):

            existing_data = {}

    # ------------------------------------------
    # GET UNLOCKED LEVELS
    # ------------------------------------------

    unlocked_levels = existing_data.get(
        "unlocked_levels",
        [1]
    )

    # Make sure Level 1 is always unlocked
    if 1 not in unlocked_levels:
        unlocked_levels.insert(0, 1)

    # Unlock the next level after completing the current level
    completed_level = level.level_number

    if completed_level < 3:
        next_level = completed_level + 1

        if next_level not in unlocked_levels:
            unlocked_levels.append(next_level)

    # ------------------------------------------
    # CREATE SAVE DATA
    # ------------------------------------------

    data = {
        "score": level.score,
        "checkpoint": None,
        "unlocked_levels": unlocked_levels
    }

    # ------------------------------------------
    # SAVE CHECKPOINT
    # ------------------------------------------

    if level.current_checkpoint is not None:

        checkpoint = level.current_checkpoint

        data["checkpoint"] = {
            "id": checkpoint.checkpoint_id
        }

    # ------------------------------------------
    # WRITE JSON
    # ------------------------------------------

    with open(
        SAVE_FILE,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==============================================
# LOAD GAME
# ==============================================

def load_game(level, level_select=None):

    if not os.path.exists(SAVE_FILE):

        return False

    try:

        with open(
            SAVE_FILE,
            "r"
        ) as file:

            data = json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return False

    # ------------------------------------------
    # LOAD SCORE
    # ------------------------------------------

    level.score = data.get(
        "score",
        0
    )

    # ------------------------------------------
    # LOAD CHECKPOINT
    # ------------------------------------------

    checkpoint_data = data.get(
        "checkpoint"
    )

    if checkpoint_data is not None:

        saved_id = checkpoint_data.get(
            "id"
        )

        for checkpoint in level.checkpoints:

            if checkpoint.checkpoint_id == saved_id:
                checkpoint.activated = True

                level.current_checkpoint = (
                    checkpoint
                )

                break

    # ------------------------------------------
    # LOAD UNLOCKED LEVELS
    # ------------------------------------------

    if level_select is not None:

        unlocked_levels = data.get(
            "unlocked_levels",
            [1]
        )

        for level_number in unlocked_levels:

            level_select.unlock_level(
                level_number
            )

    return True


# ==============================================
# DELETE SAVE
# ==============================================

def delete_save():

    if os.path.exists(SAVE_FILE):

        os.remove(SAVE_FILE)