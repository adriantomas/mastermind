from datetime import datetime
from random import choices
from typing import Tuple
from uuid import uuid4

from pynamodb.attributes import (
    BooleanAttribute,
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)

from .base_model import BaseModel

MAX_TRIES = 9
COLORS = ["R", "G", "Y", "B", "W", "O"]
TOTAL_LETTERS = 4


class Guess(MapAttribute):
    combination = UnicodeAttribute()
    guessed_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow())
    black_pegs = NumberAttribute(default_for_new=0)
    white_pegs = NumberAttribute(default_for_new=0)

    def is_valid_guess(self) -> bool:
        if not isinstance(self.combination, str):
            return False

        if len(self.combination) != TOTAL_LETTERS:
            return False

        for letter in self.combination:
            if letter not in COLORS:
                return False

        return True


class Game(BaseModel):
    class Meta(BaseModel.Meta):
        pass

    game_id = UnicodeAttribute(
        hash_key=True, attr_name="pk", default_for_new=str(uuid4())
    )
    secret = UnicodeAttribute(default_for_new="".join(choices(COLORS, k=TOTAL_LETTERS)))
    tries_left = NumberAttribute(default_for_new=MAX_TRIES)
    created_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow())
    is_solved = BooleanAttribute(default_for_new=False)
    guesses = ListAttribute(of=Guess, null=True, default=[])

    def check_win_condition(self, guess: Guess) -> None:
        if guess.combination == self.secret:
            self.is_solved = True

    def get_info(self) -> dict:
        return {k: v for k, v in self.to_dict().items() if k != "secret"}

    def save_guess(self, guess: Guess):
        self.update(
            actions=[
                Game.guesses.set((Game.guesses | []).append([guess])),
                Game.tries_left.set(Game.tries_left - 1),
                Game.is_solved.set(self.is_solved),
            ]
        )

    def is_playable(self) -> bool:
        if not self.is_solved and self.tries_left:
            return True
        return False

    def get_black_and_white_pegs(self, guess: Guess) -> Tuple[int, int]:
        combination_cp = guess.combination
        secret_cp = self.secret

        black_pegs_counter = 0
        black_pegs_indexes = []
        white_pegs_counter = 0

        for i, letter in enumerate(self.secret):
            if guess.combination[i] == letter:
                black_pegs_counter += 1

                black_pegs_indexes.append(i)

        black_pegs_indexes.reverse()

        for index in black_pegs_indexes:
            combination_cp = combination_cp[:index] + combination_cp[index + 1 :]
            secret_cp = secret_cp[:index] + secret_cp[index + 1 :]

        for letter in combination_cp:
            if letter in secret_cp:
                white_pegs_counter += 1

        return black_pegs_counter, white_pegs_counter
