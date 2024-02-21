extractor_registry = None


def add_executor_parsers(subparser):
    """
    Dynamically add discovered plugin parsers.
    """
    global extractor_registry
    from . import get_extractor_registry

    extractor_registry = get_extractor_registry()
    for _, plugin in extractor_registry.plugins.items():
        plugin.add_arguments(subparser)
