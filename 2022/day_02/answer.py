#!/usr/bin/env python


def p1(data, is_sample):
    score_pick = {"X": 1, "Y": 2, "Z": 3}
    score_game = {"win": 6, "draw": 3, "loss": 0}
    total_score = 0

    for play in data:
        other = play[0]
        me = play[-1]

        if other == "A":
            if me == "X":
                score = score_game["draw"]
            elif me == "Y":
                score = score_game["win"]
            else:
                score = score_game["loss"]
        elif other == "B":
            if me == "X":
                score = score_game["loss"]
            elif me == "Y":
                score = score_game["draw"]
            else:
                score = score_game["win"]
        else:
            if me == "X":
                score = score_game["win"]
            elif me == "Y":
                score = score_game["loss"]
            else:
                score = score_game["draw"]

        total_score += score + score_pick[me]

    return total_score


def p2(data, is_sample):
    score_pick = {"A": 1, "B": 2, "C": 3}
    score_game = {"X": 0, "Y": 3, "Z": 6}
    total_score = 0

    for play in data:
        other = play[0]
        game = play[-1]

        if other == "A":
            if game == "X":
                score = score_pick["C"]
            elif game == "Y":
                score = score_pick["A"]
            else:
                score = score_pick["B"]
        elif other == "B":
            if game == "X":
                score = score_pick["A"]
            elif game == "Y":
                score = score_pick["B"]
            else:
                score = score_pick["C"]
        else:
            if game == "X":
                score = score_pick["B"]
            elif game == "Y":
                score = score_pick["C"]
            else:
                score = score_pick["A"]

        total_score += score + score_game[game]

    return total_score
