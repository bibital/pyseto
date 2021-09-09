from secrets import token_bytes

import pytest

import pyseto
from pyseto import DecryptError, Key, VerifyError

from .utils import load_key


class TestV4Local:
    """
    Tests for v4.local.
    """

    @pytest.mark.parametrize(
        "key, msg",
        [
            (b"", "key must be specified."),
            (token_bytes(65), "key length must be up to 64 bytes."),
        ],
    )
    def test_v4_local_new_with_invalid_arg(self, key, msg):
        with pytest.raises(ValueError) as err:
            Key.new("v4", "local", key)
            pytest.fail("Key.new() should fail.")
        assert msg in str(err.value)

    def test_v4_local_decrypt_via_decode_with_wrong_key(self):
        k1 = Key.new("v4", "local", b"our-secret")
        k2 = Key.new("v4", "local", b"others-secret")
        token = pyseto.encode(k1, b"Hello world!")
        with pytest.raises(DecryptError) as err:
            pyseto.decode(k2, token)
            pytest.fail("pyseto.decode() should fail.")
        assert "Failed to decrypt." in str(err.value)

    @pytest.mark.parametrize(
        "nonce",
        [
            token_bytes(1),
            token_bytes(8),
            token_bytes(31),
            token_bytes(33),
            token_bytes(64),
        ],
    )
    def test_v4_local_encrypt_via_encode_with_wrong_nonce(self, nonce):
        k = Key.new("v4", "local", b"our-secret")
        with pytest.raises(ValueError) as err:
            pyseto.encode(k, b"Hello world!", nonce=nonce)
            pytest.fail("pyseto.encode() should fail.")
        assert "nonce must be 32 bytes long." in str(err.value)


class TestV4Public:
    """
    Tests for v4.public.
    """

    def test_v4_public_verify_via_encode_with_wrong_key(self):
        sk = Key.new("v4", "public", load_key("keys/private_key_ed25519.pem"))
        pk = Key.new("v4", "public", load_key("keys/public_key_ed25519_2.pem"))
        token = pyseto.encode(sk, b"Hello world!")
        with pytest.raises(VerifyError) as err:
            pyseto.decode(pk, token)
            pytest.fail("pyseto.decode() should fail.")
        assert "Failed to verify." in str(err.value)