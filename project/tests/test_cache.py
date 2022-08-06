import pytest

from ampyr import protocols as pt


def test_cache_manager_can_init(cache_manager_object: pt.CacheManager):
    """
    Dummy test that forces the target fixture to
    construct an `CacheManager` object.
    Naturally fails if object cannot construct
    properly.
    """

    assert True


def test_cache_manager_can_broker_data(
    cache_manager_object: pt.CacheManager,
    cacheable_object):
    """
    Validates that the given `CacheManager`
    object is able to safely `save` and `find`
    data as is expected.
    """

    obj_key, nil_key = "object_key", "null_key"

    import tempfile

    cache_manager_object.save(obj_key, cacheable_object)
    assert cache_manager_object.find(nil_key) is None
    assert cache_manager_object.find(obj_key) == cacheable_object
