from .plugin import Plugin
from .registry import ExtractorRegistry


def get_extractor_registry():
    registry = ExtractorRegistry()
    registry.discover()
    return registry
