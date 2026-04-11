def test_get_all_workflows(authorized_client, test_workflows):
    res = authorized_client.get("/workflows")

    assert res.status_code == 200
    assert len(res.json()) == len(test_workflows)


def test_get_single_workflow(authorized_client, test_workflows):
    workflow_id = test_workflows[0].id
    res = authorized_client.get(f"/workflows/{workflow_id}")

    assert res.status_code == 200
    assert res.json()["id"] == workflow_id


def test_get_single_workflow_not_found(authorized_client):
    res = authorized_client.get("/workflows/9999")

    assert res.status_code == 404


def test_get_single_workflow_not_owner(authorized_client, test_user2, session):
    from app import models

    new_workflow = models.Workflow(
        title="Other user workflow",
        raw_input="test",
        input_type="text",
        owner_id=test_user2["id"]
    )
    session.add(new_workflow)
    session.commit()

    res = authorized_client.get(f"/workflows/{new_workflow.id}")
    assert res.status_code == 404


def test_create_workflow(authorized_client):
    res = authorized_client.post("/workflows", json={
        "title": "New Workflow",
        "raw_input": "Automate something",
        "input_type": "text"
    })

    assert res.status_code == 201
    assert res.json()["title"] == "New Workflow"


def test_delete_workflow(authorized_client, test_workflows):
    workflow_id = test_workflows[0].id

    res = authorized_client.delete(f"/workflows/{workflow_id}")
    assert res.status_code == 204


def test_delete_workflow_no_token(client, test_workflows):
    workflow_id = test_workflows[0].id

    res = client.delete(f"/workflows/{workflow_id}")
    assert res.status_code == 401


def test_delete_workflow_not_owner(authorized_client, test_user2, session):
    # create workflow owned by another user
    from app import models

    new_workflow = models.Workflow(
        title="Other user workflow",
        raw_input="test",
        input_type="text",
        owner_id=test_user2["id"]
    )
    session.add(new_workflow)
    session.commit()

    res = authorized_client.delete(f"/workflows/{new_workflow.id}")
    assert res.status_code == 404
