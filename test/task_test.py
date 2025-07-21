
import pytest
import httpx
import logging

logger = logging.getLogger(__name__)


# NOTE: real http interface used insted of FastAPI built in test client

API_BASE_URL="http://localhost:8000/api"


# simulate fixture
task_id = None

def test_create_task():
    global task_id
    resp = httpx.post(API_BASE_URL+"/task", json={"descr":"Test task descr"})
    assert resp.status_code == 201
    task = resp.json()
    task_id = task["id"]
    assert task_id is not None


def test_get_task():
    global task_id
    resp = httpx.get(API_BASE_URL+f"/task/{task_id}")
    assert resp.status_code == 200
    task = resp.json()
    assert task["id"] == task_id
    logger.info(task)


def test_tasklist():
    resp = httpx.get(API_BASE_URL+f"/tasklist")
    assert resp.status_code == 200
    tasklist = resp.json()
    logger.info("len(tasklist): %s", len(tasklist["tasks"]))
    assert len(tasklist["tasks"]) > 0


def test_assign():
    global task_id
    user_id = "123"
    resp = httpx.put(API_BASE_URL+f"/task/{task_id}/assign", json={"user_id": user_id})
    assert resp.status_code == 200
    task = resp.json()
    assert task["assigned_to"] == user_id


def test_reassign():
    global task_id
    user_id = "456"
    resp = httpx.put(API_BASE_URL+f"/task/{task_id}/assign", json={"user_id": user_id})
    assert resp.status_code == 200
    task = resp.json()
    assert task["assigned_to"] == user_id
    logger.info(task)


def test_update1():
    global task_id
    resp = httpx.put(API_BASE_URL+f"/task/{task_id}", json={"status": 1, "descr": "update1"})
    assert resp.status_code == 200
    task = resp.json()
    assert task["status"] == 1
    assert task["descr"] == "update1"


def test_update2():
    global task_id
    resp = httpx.put(API_BASE_URL+f"/task/{task_id}", json={"status": 2, "descr": "update2"})
    assert resp.status_code == 200
    task = resp.json()
    assert task["status"] == 2
    assert task["descr"] == "update2"


def test_comment():
    global task_id
    resp = httpx.post(API_BASE_URL+f"/task/{task_id}/comment", json={"text": "test comment"})
    assert resp.status_code == 200
    comment = resp.json()
    c_id = comment["id"]
    logger.info(f"{comment=}")
    comments = httpx.get(API_BASE_URL+f"/task/{task_id}/comments").json()
    logger.info(f"{comments=}")
    assert any(cmn["id"] == c_id for cmn in comments["comments"])

