from Lib.point_counters import *


def test_counts_basic():
    dice = [1, 2, 2, 5, 6]
    result = counts(dice)
    assert result == {
        1: 1,
        2: 2,
        3: 0,
        4: 0,
        5: 1,
        6: 1
    }


def test_counts_empty():
    dice = []
    result = counts(dice)
    assert all(v == 0 for v in result.values())

def test_obere_punkte():
    dice = [1, 1, 3, 5, 6]
    c = counts(dice)
    result = oberePunkte(c)

    assert result[1] == 2
    assert result[3] == 3
    assert result[5] == 5
    assert result[6] == 6

def test_dreier_pasch_true():
    dice = [3, 3, 3, 5, 6]
    assert dreierPasch(counts(dice), dice) == sum(dice)


def test_dreier_pasch_false():
    dice = [3, 3, 5, 6, 1]
    assert dreierPasch(counts(dice), dice) == 0


def test_vierer_pasch_true():
    dice = [2, 2, 2, 2, 5]
    assert viererPasch(counts(dice), dice) == sum(dice)


def test_vierer_pasch_false():
    dice = [2, 2, 2, 5, 6]
    assert viererPasch(counts(dice), dice) == 0


def test_kniffel_true():
    dice = [6, 6, 6, 6, 6]
    assert fuenferPasch(counts(dice)) == 50


def test_kniffel_false():
    dice = [6, 6, 6, 6, 5]
    assert fuenferPasch(counts(dice)) == 0

def test_full_house_true():
    dice = [2, 2, 3, 3, 3]
    assert fullHouse(counts(dice)) == 25


def test_full_house_false():
    dice = [2, 2, 2, 2, 3]
    assert fullHouse(counts(dice)) == 0

def test_kleine_strasse_true():
    dice = [1, 2, 3, 4, 6]
    assert kleineStrasse(dice) == 30


def test_kleine_strasse_false():
    dice = [1, 2, 3, 5, 6]
    assert kleineStrasse(dice) == 0


def test_grosse_strasse_true_1():
    dice = [1, 2, 3, 4, 5]
    assert grosseStrasse(dice) == 40


def test_grosse_strasse_true_2():
    dice = [2, 3, 4, 5, 6]
    assert grosseStrasse(dice) == 40


def test_grosse_strasse_false():
    dice = [1, 2, 3, 4, 6]
    assert grosseStrasse(dice) == 0

def test_chance():
    dice = [1, 2, 3, 4, 6]
    assert chance(dice) == 16

def test_get_point_options_kniffel():
    dice = [5, 5, 5, 5, 5]
    options = dict(getPointOptions(dice))

    assert options["Kniffel"] == 50
    assert options["Chance"] == 25
    assert options["Nur 5er zählen"] == 25


def test_get_point_options_full_house():
    dice = [2, 2, 3, 3, 3]
    options = dict(getPointOptions(dice))

    assert options["Full House"] == 25
    assert options["Chance"] == sum(dice)

