import json
import os


SAVE_FILE = "save.json"


# ==================================================
# SAVE GAME
# ==================================================

def save_game(level):

    data = {

        "score": level.score,

        "health": level.player.health,

        "level_complete": level.level_complete,

        "checkpoint": None

    }

    # ----------------------------------------------
    # CURRENT CHECKPOINT
    # ----------------------------------------------

    if level.current_checkpoint is not None:

        data["checkpoint"] = {
            "x": level.current_checkpoint.x,
            "y": level.current_checkpoint.y
        }

    # ----------------------------------------------
    # CHECKPOINTS
    # ----------------------------------------------

    data["checkpoints"] = []

    for checkpoint in level.checkpoints:

        data["checkpoints"].append(
            checkpoint.activated
        )

    # ----------------------------------------------
    # WRITE JSON
    # ----------------------------------------------

    with open(
        SAVE_FILE,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ==================================================
# LOAD GAME
# ==================================================

def load_game(level):

    if not os.path.exists(
        SAVE_FILE
    ):
        return False

    try:

        with open(
            SAVE_FILE,
            "r"
        ) as file:

            data = json.load(file)

        # ------------------------------------------
        # SCORE
        # ------------------------------------------

        level.score = data.get(
            "score",
            0
        )

        # ------------------------------------------
        # HEALTH
        # ------------------------------------------

        level.player.health = data.get(
            "health",
            3
        )

        # ------------------------------------------
        # LEVEL COMPLETE
        # ------------------------------------------

        level.level_complete = data.get(
            "level_complete",
            False
        )

        # ------------------------------------------
        # CHECKPOINTS
        # ------------------------------------------

        saved_checkpoints = data.get(
            "checkpoints",
            []
        )

        for index, activated in enumerate(
            saved_checkpoints
        ):

            if index < len(
                level.checkpoints
            ):

                level.checkpoints[
                    index
                ].activated = activated

        # ------------------------------------------
        # CURRENT CHECKPOINT
        # ------------------------------------------

        checkpoint_data = data.get(
            "checkpoint"
        )

        if checkpoint_data is not None:

            for checkpoint in level.checkpoints:

                if (
                    checkpoint.x
                    == checkpoint_data["x"]
                    and
                    checkpoint.y
                    == checkpoint_data["y"]
                ):

                    level.current_checkpoint = (
                        checkpoint
                    )

                    break

        return True

    except (
        json.JSONDecodeError,
        KeyError,
        TypeError
    ):

        return False


# ==================================================
# DELETE SAVE
# ==================================================

def delete_save():

    if os.path.exists(
        SAVE_FILE
    ):

        os.remove(
            SAVE_FILE
        )