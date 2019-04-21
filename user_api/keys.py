import json
from jwcrypto import jwk


def load_keys(key_list_path: str):
    global keys
    # Load the RSA keys from the keys folder
    keys = jwk.JWKSet()
    with open(key_list_path, mode="r") as key_list_file:

        # Read the locations of the keys
        key_list = json.load(key_list_file)
        print(f"Keylist contains {len(key_list)} elements.")
        for key_list_item in key_list:

            # Read the PEM key file
            with open(key_list_item["path"], mode="rb") as key_file:
                # Create JWK from file
                k = jwk.JWK.from_pem(key_file.read())
                k._params["kid"] = key_list_item["name"]
                keys.add(k)

        print("JWKSet has been loaded.", keys)
    load_key()


def load_key():
    global key
    # We will sign with the first key
    key = next(keys.__iter__(), None)
    if key is not None:
        print("Signing key has been loaded.", key._params["kid"], key)
    else:
        print("WARNING: Signing key could not be loaded.")


def get_keys():
    return keys


def get_signing_key():
    return key
