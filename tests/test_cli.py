import os
from reorg import cli


def test_whats_dir_target(monkeypatch):
    monkeypatch.setenv("PWD", "/foo")
    assert "/foo/reorged" == cli.whats_dir_target(None)
    assert "/bar/reorged" == cli.whats_dir_target("/bar")

def test_prepare_dir_target(tmpdir):
    target_dir = cli.whats_dir_target(str(tmpdir))
    print(target_dir)
    cli.prepare_dir_target(target_dir)
    assert os.path.exists(target_dir)

    # Test when target directory already exists with stuff in it
    with open(os.path.join(target_dir, "some-file.md"), "w+") as f:
        f.write("Hello world!")

    cli.prepare_dir_target(target_dir)
    assert os.path.exists(target_dir) and len(os.listdir(target_dir)) == 0
