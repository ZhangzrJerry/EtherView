def test_package():
    import etherview  # noqa: F401

    assert etherview.__version__ == "0.0.0"
    assert etherview.__name__ == "etherview"
