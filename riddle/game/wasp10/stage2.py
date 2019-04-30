from . import make_entry_point, validate


questions = []


@questions.append
@validate(float)
def q_math_1(ans):
    """Compute the modulo of $4+3j$."""
    return ans == abs(4+3j)


@questions.append
@validate(complex)
def q_math_2(ans):
    """Compute $(7+4j)\\cdot(17-5j)$."""
    return ans == (139+33j)


entry = make_entry_point(2, questions, '/wasp10/stage4')
