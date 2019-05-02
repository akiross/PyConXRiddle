from collections import Counter
from riddle.tools import eval_expr
from . import make_entry_point, validate


questions = []


@questions.append
@validate(float)
def q_math_1(ans) -> "Real e.g. 123.45":
    """A bottle of pregiated Italian wine is worth 52 euros, the bottle of wine
       alone is worth 50 euros more than the cork.
       How many euros is the cork worth?
    """
    # b(ottle) + c(cork) = 52
    # b = 50 + c
    # 50 + c + c = 52
    # c = 1
    return ans == 1


@questions.append
@validate(int)
def q_math_2(ans) -> "Integer e.g. 12345":
    """<p>A very large cake is divided among one hundred people. The first
       person gets 1% of the whole cake, the second person gets 2% of the
       remaining cake, the third has 3% of the remaining cake, and so on. The
       last person takes, of course, 100% of the remaining cake.</p>
       <p>Write the number of the person who has the largest slice</p>
    """
    cake = 1
    portions = []
    for i in range(1, 101):
        portion = cake * i / 100
        portions.append(portion)
        cake -= portion
    return ans == portions.index(max(portions)) + 1


@questions.append
@validate(lambda s: set(str(s)).issubset(set('+8')), check_only=True)
def q_math_3(ans) -> "Sum of integers e.g. 8+8+8888+8+8":
    """How can eight 8s sum up to 1000, using only addition?"""
    return eval_expr(ans) == 1000


@questions.append
@validate(int)
def q_math_4(ans) -> "Integer e.g. 12345":
    """<p>There is a 10 figures number where the first (most significant) digit
       tells how many zeros are present, the second digits tells how many ones
       are present, the third how many twos are present, and so on, until the
       tenth digit, which tells how many nines are in the number.</p>
       <p>In other words, the number $$a_0a_1a_2a_3...a_9$$ where \\(a_i\\) counts
       the number of times digit \\(i\\) appears in the number.</p>
       <p>What is this number?</p>
    """
    # TODO compute this solution
    return ans == 6210001000


entry = make_entry_point(2, questions, '/wasp10/stage3')
