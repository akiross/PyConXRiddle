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
            return route.format(name=encoder(name))
        if hasattr(entry, 'route'):
            entry.route.append((_builder, options))
        else:
            entry.route = [(_builder, options)]
        return entry
    return _deco
