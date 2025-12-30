def test_create_and_list_tags(client):
    """Test creating and listing tags."""
    # Create a tag
    payload = {"name": "urgent", "color": "#FF5733"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "urgent"
    assert data["color"] == "#FF5733"
    assert "id" in data

    # List tags
    r = client.get("/tags/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_create_duplicate_tag(client):
    """Test that creating a duplicate tag returns 400."""
    payload = {"name": "duplicate", "color": "#000000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201

    # Try to create the same tag again
    r = client.post("/tags/", json=payload)
    assert r.status_code == 400
    assert "already exists" in r.text


def test_get_tag(client):
    """Test getting a specific tag."""
    # Create a tag first
    payload = {"name": "important", "color": "#00FF00"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201
    tag_id = r.json()["id"]

    # Get the tag
    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "important"
    assert data["id"] == tag_id


def test_get_nonexistent_tag(client):
    """Test getting a tag that doesn't exist returns 404."""
    r = client.get("/tags/999999")
    assert r.status_code == 404


def test_update_tag(client):
    """Test updating a tag."""
    # Create a tag
    payload = {"name": "old-name", "color": "#111111"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201
    tag_id = r.json()["id"]

    # Update the tag
    update_payload = {"name": "new-name", "color": "#222222"}
    r = client.put(f"/tags/{tag_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "new-name"
    assert data["color"] == "#222222"

    # Verify the update persisted
    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "new-name"


def test_update_tag_partial(client):
    """Test updating only some fields of a tag."""
    # Create a tag
    payload = {"name": "partial", "color": "#AAAAAA"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201
    tag_id = r.json()["id"]

    # Update only the color
    update_payload = {"color": "#BBBBBB"}
    r = client.put(f"/tags/{tag_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "partial"  # Name unchanged
    assert data["color"] == "#BBBBBB"  # Color updated


def test_update_tag_duplicate_name(client):
    """Test that updating a tag to a duplicate name returns 400."""
    # Create two tags
    r = client.post("/tags/", json={"name": "tag1"})
    assert r.status_code == 201

    r = client.post("/tags/", json={"name": "tag2"})
    assert r.status_code == 201
    tag2_id = r.json()["id"]

    # Try to rename tag2 to tag1
    r = client.put(f"/tags/{tag2_id}", json={"name": "tag1"})
    assert r.status_code == 400
    assert "already exists" in r.text


def test_delete_tag(client):
    """Test deleting a tag."""
    # Create a tag
    payload = {"name": "to-delete", "color": "#FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201
    tag_id = r.json()["id"]

    # Delete the tag
    r = client.delete(f"/tags/{tag_id}")
    assert r.status_code == 204

    # Verify it's deleted
    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 404


def test_delete_nonexistent_tag(client):
    """Test deleting a tag that doesn't exist returns 404."""
    r = client.delete("/tags/999999")
    assert r.status_code == 404
