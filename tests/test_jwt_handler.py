import pytest
from unittest.mock import patch
from jose import JWTError
from app.auth.jwt_handler import (
    create_access_token,
    decode_token,
    get_username_from_token,
    get_role_from_token,
    is_token_expired,
)

# token creation

def test_create_token_returns_string():
    token = create_access_token({"sub": "alice", "role": "customer"})
    assert isinstance(token, str) and len(token) > 0

def test_token_contains_correct_username():
    token = create_access_token({"sub": "alice", "role": "customer"})
    assert decode_token(token)["sub"] == "alice"

def test_token_contains_expiry():
    token = create_access_token({"sub": "alice", "role": "customer"})
    assert "exp" in decode_token(token)

def test_longer_expiry_produces_later_exp():
    short = create_access_token({"sub": "a", "role": "customer"}, expires_minutes=5)
    long = create_access_token({"sub": "a", "role": "customer"}, expires_minutes=60)
    assert decode_token(long)["exp"] > decode_token(short)["exp"]


# decoding 

def test_decode_valid_token_returns_payload():
    token = create_access_token({"sub": "alice", "role": "customer"})
    assert decode_token(token)["sub"] == "alice"

def test_decode_expired_token_raises_error():
    token = create_access_token({"sub": "alice", "role": "customer"}, expires_minutes=-1)
    with pytest.raises(JWTError):
        decode_token(token)

def test_decode_garbage_string_raises_error():
    with pytest.raises(JWTError):
        decode_token("not.a.real.token")


# purposely broken inputs to verify the system rejects them

def test_tampered_signature_is_rejected():
    token = create_access_token({"sub": "alice", "role": "customer"})
    tampered = token[:-5] + "XXXXX"
    with pytest.raises(JWTError):
        decode_token(tampered)

def test_tampered_payload_is_rejected():
    token = create_access_token({"sub": "alice", "role": "customer"})
    parts = token.split(".")
    parts[1] = "dGhpc2lzZmFrZXBheWxvYWQ"
    with pytest.raises(JWTError):
        decode_token(".".join(parts))

def test_token_signed_with_wrong_key_is_rejected():
    # sign with a fake key, decode with the real one, should fail
    with patch("app.auth.jwt_handler.SECRET_KEY", "wrong-key"):
        bad_token = create_access_token({"sub": "alice", "role": "customer"})
    with pytest.raises(JWTError):
        decode_token(bad_token)


def test_get_username_returns_none_when_decode_fails():
    with patch("app.auth.jwt_handler.decode_token", side_effect=JWTError("mocked")):
        assert get_username_from_token("any_token") is None

def test_get_role_returns_none_when_decode_fails():
    with patch("app.auth.jwt_handler.decode_token", side_effect=JWTError("mocked")):
        assert get_role_from_token("any_token") is None


# helper functions

def test_get_username_returns_correct_value():
    token = create_access_token({"sub": "bob", "role": "driver"})
    assert get_username_from_token(token) == "bob"

def test_get_username_returns_none_for_bad_token():
    assert get_username_from_token("bad.token") is None

def test_get_role_returns_correct_value():
    token = create_access_token({"sub": "alice", "role": "admin"})
    assert get_role_from_token(token) == "admin"

def test_valid_token_is_not_expired():
    token = create_access_token({"sub": "alice", "role": "customer"})
    assert is_token_expired(token) is False

def test_expired_token_is_expired():
    token = create_access_token({"sub": "alice", "role": "customer"}, expires_minutes=-1)
    assert is_token_expired(token) is True
