import math

from . import make_entry_point, validate


questions = []


@questions.append
@validate(str)
def q_logic_1(ans) -> "Index(es) of the correct answer(s) e.g. 1(,2,3)":
    """Which of the following statements is/are true?
    <ol>
        <li>Exactly one of the statements in this list is false.</li>
        <li>Exactly two of the statements in this list are false.</li>
        <li>Exactly three of the statements in this list are false.</li>
        <li>Exactly four of the statements in this list are false.</li>
        <li>Exactly five of the statements in this list are false.</li>
        <li>Exactly six of the statements in this list are false.</li>
        <li>Exactly seven of the statements in this list are false.</li>
        <li>Exactly eight of the statements in this list are false.</li>
        <li>Exactly nine of the statements in this list are false.</li>
        <li>Exactly ten of the statements in this list are false.</li>
    </ol>
    """
    return ans.split(',') == ["9"]


@questions.append
@validate(int)
def q_logic_2(ans) -> "Index of the correct answer e.g. 123":
    """Which answer in the list is the correct answer to this question?
    <ol>
        <li>All of the below.</li>
        <li>None of the below.</li>
        <li>All of the above.</li>
        <li>One of the above.</li>
        <li>None of the above.</li>
        <li>None of the above.</li>
    </ol>
    """
    return ans == 5


@questions.append
@validate(float)
def q_logic_3(ans) -> "Real e.g. 123.45":
    """One hen and half takes a day and half to make an egg and half.
       How many eggs will a hen make in six days?
    """
    return ans == 4


# We move to next page regardless the correctness of the answer
entry = make_entry_point(3, questions, '/wasp10/stage4')
