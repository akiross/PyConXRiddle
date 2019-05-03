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


def without_answer(entry):
    """Automatically set answer pass and no score for the entry point."""
    @functools.wraps(entry)
    def entry_(*args, **kwargs):
        r = entry(*args, **kwargs)
        r['score'] = 0
        r['answer'] = 'pass'
        return r
    return entry_


def on_success(redirect=None, score=1, twins=None):
    """Determine what happens on level passed."""
    def _deco(entry):
        entry.on_success = (redirect, score)
        entry.twins = twins
        return entry
    return _deco


def on_failure(redirect=None, score=0, twins=None):
    """Determine what happens on level failed."""
    def _deco(entry):
        entry.on_failure = (redirect, score)
        entry.twins = twins
        return entry
    return _deco


def on_answer(redirect=None, success_score=1, failure_score=0, twins=None):
    """Determine what happens when a pass/fail answer is given."""
    def _deco(entry):
        entry.on_success = (redirect, success_score)
        entry.on_failure = (redirect, failure_score)
        entry.twins = twins
        return entry
    return _deco
