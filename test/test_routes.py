# tests/test_routes.py

import pytest
import time


def test_index_redirects_to_collection(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/collection" in response.headers["Location"]


@pytest.mark.parametrize("route", ["/collection", "/carousel"])
def test_basic_route_loads(client, route):
    response = client.get(route)
    assert response.status_code == 200
    assert b"<html" in response.data.lower()


@pytest.mark.parametrize(
    "route,sort",
    [
        ("/collection", "artist"),
        ("/collection", "year"),
        ("/collection", "album"),
        ("/carousel", "artist"),
        ("/carousel", "year"),
        ("/carousel", "album"),
    ],
)
def test_sorting_options(client, route, sort):
    response = client.get(f"{route}?sort={sort}")
    assert response.status_code == 200
    assert b"<html" in response.data.lower()


@pytest.mark.parametrize("route", ["/collection", "/carousel"])
def test_filter_accepts_parameter(client, route):
    response = client.get(f"{route}?filter=Kings+of+Leon")
    assert response.status_code == 200
    assert b"<html" in response.data.lower()


@pytest.mark.parametrize("route", ["/collection", "/carousel"])
def test_filter_results_contain_artist(client, route):
    response = client.get(f"{route}?filter=Kings+of+Leon")
    html = response.data.decode()
    assert "kings of leon" in html.lower(), (
        f"Expected 'Kings of Leon' to be in the response HTML for {route}"
    )


def test_collection_response_time(client):
    start = time.time()
    response = client.get("/collection")
    duration = time.time() - start
    assert duration < 2.5, f"Page took too long to respond: {duration:.2f}s"


def test_settings_route(client):
    response = client.get("/settings")
    assert response.status_code == 200
    assert b"<html" in response.data.lower()


@pytest.mark.parametrize(
    "release_id, expected_title, expected_artist",
    [
        (1471516, "Only By The Night", "Kings Of Leon"),
        (8328229, "The Heat", "NEEDTOBREATHE"),
        (22551998, "Going To Hell", "The Pretty Reckless"),
    ],
)
def test_release_page_by_id(client, release_id, expected_title, expected_artist):
    response = client.get(f"/release?id={release_id}")
    assert response.status_code == 200

    html = response.data.decode().lower()

    assert "<html" in html, f"Expected HTML content for release {release_id}"
    assert expected_title.lower() in html, (
        f"Expected album title '{expected_title}' in release {release_id} page"
    )
    assert expected_artist.lower() in html, (
        f"Expected artist name '{expected_artist}' in release {release_id} page"
    )


def test_settings_refresh_post(client):
    response = client.post(
        "/settings", data={"collectionRefresh": "Refresh Collection Data"}
    )
    assert response.status_code == 200
    html = response.data.decode()
    assert "Settings" in html
    assert "Refresh Collection Data" in html
