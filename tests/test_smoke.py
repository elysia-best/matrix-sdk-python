import pytest

from matrix_sdk_python import (
    __all__ as public_api,
    ClientError,
    MediaSource,
    is_room_alias_format_valid,
    matrix_to_room_alias_permalink,
    matrix_to_user_permalink,
    room_alias_name_from_room_display_name,
    sdk_git_sha,
)
from matrix_sdk_python._generated import matrix_sdk_ffi


@pytest.mark.parametrize(
    ("alias", "expected"),
    [
        ("alias:domain.org", False),
        ("#alias:something:domain.org", False),
        ("#alias.domain.org", False),
        ("#alias:", False),
        ("#alias with whitespace:domain.org", False),
        ("#alias\t:domain.org", False),
        ("#a#lias,{t\\est}:domain.org", False),
        ("#Alias:domain.org", False),
        ("#alias:Domain.org", False),
        ("#alias.test:domain.org", True),
    ],
)
def test_room_alias_format_validation_matches_rust_cases(alias: str, expected: bool) -> None:
    assert is_room_alias_format_valid(alias) is expected
    assert matrix_sdk_ffi.is_room_alias_format_valid(alias) is expected


def test_public_api_exports_expected_symbols() -> None:
    expected_names = {
        "ClientError",
        "MediaSource",
        "is_room_alias_format_valid",
        "matrix_to_room_alias_permalink",
        "matrix_to_user_permalink",
        "room_alias_name_from_room_display_name",
        "sdk_git_sha",
    }

    assert expected_names.issubset(set(public_api))
    assert "dataclass" not in public_api
    assert "annotations" not in public_api
    assert "matrix_sdk" not in public_api


def test_sdk_git_sha_returns_non_empty_string() -> None:
    value = sdk_git_sha()
    assert isinstance(value, str)
    assert value


def test_public_and_generated_sdk_git_sha_match() -> None:
    assert sdk_git_sha() == matrix_sdk_ffi.sdk_git_sha()


def test_permalink_helpers_work_without_network() -> None:
    user_permalink = matrix_to_user_permalink("@alice:example.org")
    room_alias_permalink = matrix_to_room_alias_permalink("#room:example.org")

    assert user_permalink == "https://matrix.to/#/@alice:example.org"
    assert room_alias_permalink == "https://matrix.to/#/%23room:example.org"


def test_permalink_helpers_raise_on_invalid_identifiers() -> None:
    with pytest.raises(ClientError):
        matrix_to_user_permalink("alice:example.org")

    with pytest.raises(ClientError):
        matrix_to_room_alias_permalink("room:example.org")


def test_room_alias_helpers_work_without_network() -> None:
    assert room_alias_name_from_room_display_name("Hello Matrix Room") == "hello-matrix-room"


def test_media_source_round_trip_without_network() -> None:
    media_source = MediaSource.from_url("mxc://example.org/media-id")

    assert media_source.url() == "mxc://example.org/media-id"

    json_value = media_source.to_json()
    restored = MediaSource.from_json(json_value)

    assert restored.url() == "mxc://example.org/media-id"
    assert restored.to_json() == json_value
