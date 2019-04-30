import math

from riddle.tools import eval_expr
from . import make_entry_point, validate


questions = []


@questions.append
@validate(int)
def q_basic_1(ans) -> "Integer e.g. 12345":
    """Compute 2<sup>38</sup>."""
    return ans == 2**38


@questions.append
@validate(float)
def q_basic_2(ans) -> "Real e.g. 123.45":
    """Given the equation $$y = (log(4 * x + 1) * x) / log(9 * x**2 * e**x)$$
       please compute $y$ when $x=42$.
       <p>Round to 2<sup>nd</sup> decimal digit.</p>
    """
    def _f(x):
        return (math.log(4 * x + 1) * x) / math.log(9 * x ** 2 * math.exp(x))
    return round(ans, 2) == round(_f(42), 2)


@questions.append
@validate(float)
def q_basic_3(ans) -> "Real e.g. 123.45":
    """Given the function
    $$f(n) = \\sum_{i=0}^{n}{i}$$
    compute
    $$\\prod_{n=0}^{50000}{f(n)}$$.
    """
    return ans == 0


@questions.append
@validate(float)
def q_basic_4(ans) -> "Real e.g. 123.45":
    """Compute the modulo of $4+3j$."""
    return ans == abs(4 + 3j)


@questions.append
@validate(lambda x: eval_expr(x, 'np+-'))
def q_basic_5(ans) -> "Complex e.g. 12.3 + 4.5j":
    """Compute $(7+4j)\\cdot(17-5j)$."""
    return ans == ((7 + 4j) * (17 - 5j))


# We move to next page regardless the correctness of the answer
entry = make_entry_point(1, questions, '/wasp10/stage2')
