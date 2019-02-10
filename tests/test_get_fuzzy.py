import pytest

from dictextendfuzzy import get_fuzzy, get_fuzzy_stats


DATA = {"aaaa" : 1, "bbbb" : 2, 'cccc' : 3, 1234: 'x1234x', 9876: 'x9876x'}

@pytest.mark.parametrize('key, expected', [
    ('aaaa', 1),
    ('aAaA', 1),
    ('aaa', 1),
    ('abbb', 2),
    ('aaax', 1),
    ('xxxx', None),
    (1, None),
    (None, None),
    ('1234', 'x1234x'),
    ('1235', 'x1234x'),
    (1235, 'x1234x'),
])
def test_get_fuzzy(key, expected):
    assert DATA.get_fuzzy(key) == expected
    assert DATA.get_fuzzy_stats(key).value == expected
    

@pytest.mark.parametrize('key, level, expected', [
    ('aaaa', 1, 1),
    ('aAaA', 1, 1),
    ('aAbb', 0.50001, None),
    ('aabb', 0.5, 2),
    ('aabb', 0.499999, 2),
    ('bbbb', 0, 2),
    ('xxxx', 0, 3),
    ('', 0, 3),
    (None, 0, 3),
])
def test_get_fuzzy_with_level(key, level, expected):
    assert DATA.get_fuzzy(key, level=level) == expected
    assert DATA.get_fuzzy_stats(key, level=level).value == expected

@pytest.mark.parametrize('key, level, default, expected', [
    ('aaaa', 1, 999, 1),
    ('aaaB', 1, {}, {}),
])
def test_get_fuzzy_with_default(key, level, default, expected):
    assert DATA.get_fuzzy(key, default, level=level) == expected
    assert DATA.get_fuzzy_stats(key, default, level=level).value == expected


def test_empty_dict():
    assert {}.get_fuzzy('aaaa') == None
    assert {}.get_fuzzy('aaaa', {}) == {}
    assert {}.get_fuzzy('aaaa', 999, level=0) == 999

    actual = {}.get_fuzzy_stats('aaaa') 
    assert actual.key == None
    assert actual.value == None
    assert actual.ratio == 0

    actual = {}.get_fuzzy_stats('aaaa', {})
    assert actual.key == None
    assert actual.value == {}
    assert actual.ratio == 0

    actual = {}.get_fuzzy_stats('aaaa', 999, level=0)
    assert actual.key == None
    assert actual.value == 999
    assert actual.ratio == 0


def test_non_primitive_key():
    data = {
        ('aaa', 'bbb') : 12,
        ('ccc', 'ddd') : 34,
        "('ccc', 'ddd')" : 99
    }

    assert data.get_fuzzy(('aaa','bbb')) == 12
    assert data.get_fuzzy_stats(('aaa','bbb')).ratio == 1
    
    assert data.get_fuzzy(('aaa','bbc')) == 12
    assert data.get_fuzzy(('aaa','bcc')) == 12
    assert data.get_fuzzy(('aaa','ccc')) == 12
    assert data.get_fuzzy(('abb','bbc')) == 12

    assert data.get_fuzzy(('ccc','ddd')) == 34
    assert data.get_fuzzy_stats(('ccc','ddd')).ratio == 1

    # key has been duplicated because keys must be transform to string
    # str('ccc', 'ddd') ==  "('ccc', 'ddd')" 
    assert data.get_fuzzy(('ccc','ddc')) in (34, 99)
    
