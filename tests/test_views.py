def test_example(test_client):
    rv = test_client.get('/url/does/not/exist')
    assert rv.status_code == 404
