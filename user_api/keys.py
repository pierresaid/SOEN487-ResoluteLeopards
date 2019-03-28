import json
from jwcrypto import jwk


def load_keys(key_list_path: str):
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
                key_file.close()

        key_list_file.close()
        print("JWKSet has been loaded.", keys)

    return keys


def load_key(keys: jwk.JWKSet):
    # We will sign with the first key
    key = next(keys.__iter__())
    if key is not None:
        print("Signing key has been loaded.", key)
    else:
        print("WARNING: Signing key could not be loaded.")
    return key
