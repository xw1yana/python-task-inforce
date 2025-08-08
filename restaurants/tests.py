from datetime import date, timedelta

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from employees.models import Employee
from restaurants.models import Menu, Restaurant, Vote


@pytest.mark.django_db
def test_register_and_jwt_token(client):
    url = "/api/auth/register/"
    resp = client.post(
        url,
        {"username": "user1", "password": "strongpass123", "email": "u@example.com"},
    )
    assert resp.status_code == 201
    token_resp = client.post(
        "/api/auth/token/", {"username": "user1", "password": "strongpass123"}
    )
    assert token_resp.status_code == 200
    assert "access" in token_resp.json()


@pytest.mark.django_db
def test_menu_create_and_get_today(client):
    user = Employee.objects.create_user(username="u2", password="pass12345")
    token = client.post(
        "/api/auth/token/", {"username": "u2", "password": "pass12345"}
    ).json()["access"]
    auth = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    r = Restaurant.objects.create(name="R1")
    resp = client.post(
        "/api/menus/",
        {"restaurant": r.id, "date": date.today().isoformat(), "items": "a,b,c"},
        **auth,
    )
    assert resp.status_code == 201
    resp2 = client.get("/api/menus/today/", **auth)
    assert resp2.status_code == 200
    assert len(resp2.json()) >= 1


@pytest.mark.django_db
def test_vote_and_prevent_duplicate(client):
    user = Employee.objects.create_user(username="voter", password="pass12345")
    token = client.post(
        "/api/auth/token/", {"username": "voter", "password": "pass12345"}
    ).json()["access"]
    auth = {"HTTP_AUTHORIZATION": f"Bearer {token}"}
    r = Restaurant.objects.create(name="R2")
    m = Menu.objects.create(restaurant=r, date=date.today(), items="x,y")
    r1 = client.post("/api/votes/", {"menu": m.id}, **auth)
    assert r1.status_code == 201
    r2 = client.post("/api/votes/", {"menu": m.id}, **auth)
    assert r2.status_code == 400
