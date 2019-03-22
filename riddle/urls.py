import functools


def add_route(route, **options):
    """Use flask's routing mechanism."""
    def _deco(entry):
        # Append to the list if existing, else create the list
        if hasattr(entry, 'route'):
            entry.route.append((route, options))
        else:
            entry.route = [(route, options)]
        return entry
    return _deco


def add_encoded_route(route, encoder, **options):
    """Encoder is a function that given a string encodes it."""
    def _deco(entry):
        def _builder(name):
            """Encode name and replace it in route."""
            return route.format(name=encoder(str(name)))
        if hasattr(entry, 'route'):
            entry.route.append((_builder, options))
        else:
            entry.route = [(_builder, options)]
        return entry
    return _deco


def on_success(redirect=None, score=1):
    """Determine what happens on level passed."""
    def _deco(entry):
        entry.on_success = (redirect, score)
        return entry
    return _deco


def on_failure(redirect=None, score=0):
    """Determine what happens on level failed."""
    def _deco(entry):
        entry.on_failure = (redirect, score)
        return entry
    return _deco


def on_answer(redirect=None, success_score=1, failure_score=0):
    """Determine what happens when a pass/fail answer is given."""
    def _deco(entry):
        entry.on_success = (redirect, success_score)
        entry.on_failure = (redirect, failure_score)
        return entry
    return _deco
