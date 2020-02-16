from reorg import crawling as cr


def test_is_leaf_node():
    assert cr.is_leaf_node(("/root", ["_notes"], ["_index.md"])) == True
    assert cr.is_leaf_node(("/root", ["_notes", "AnotherContext"],
        ["_index.md"])) == False

def test_whats_dir_target_for_section():
    target_dir = cr.whats_target_dir_for_section("/foo/bar/baz", "/foo", "/target")
    assert target_dir == "/target/bar/baz"
    target_dir = cr.whats_target_dir_for_section("/foo/bar", "/foo/bar", "/target")
    assert target_dir == "/target"

