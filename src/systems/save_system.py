import json
import os


SAVE_FILE = "savegame.json"


# ==============================================
# SAVE GAME
# ==============================================

def save_game(level):

    data = {
        "score": level.score,
        "checkpoint": None
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

def load_game(level):

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

    return True


# ==============================================
# DELETE SAVE
# ==============================================

def delete_save():

    if os.path.exists(SAVE_FILE):

        os.remove(SAVE_FILE)