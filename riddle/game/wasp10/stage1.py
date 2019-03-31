import math

from . import make_entry_point, validate


questions = []


@questions.append
@validate(int)
def q_math_1(ans):
    """Compute 2<sup>38</sup>."""
    return ans == 2**38


@questions.append
@validate(float)
def q_math_2(ans):
    """Given the equation $$y = (log(4 * x + 1) * x) / log(9 * x**2 * e**x)$$
       please compute $y$ when $x=42$.
       <p>Round to 2<sup>nd</sup> decimal digit.</p>
    """
    def _f(x):
        return (math.log(4 * x + 1) * x) / math.log(9 * x ** 2 * math.exp(x))
    return round(ans, 2) == round(_f(42), 2)


@questions.append
@validate(float)
def q_math_3(ans):
    """Given the function $$f(n) = \sum_{i=0}^{n}{i}$$ compute
    $$\prod_{n=0}^{50000}{f(n)}$$.
    """
    return ans == 0


# We move to next page regardless the correctness of the answer
entry = make_entry_point(1, questions, '/wasp10/stage2')
