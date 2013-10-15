import base64
import pickle

from json import JSONDecoder, JSONEncoder


def _encode_pickle(data):
    """
    :returns: bytes -- encoded data
    """
    return base64.b64encode(
        # to be compatible with Python2
        pickle.dumps(data, protocol=2)
    )


def _decode_pickle(data):
    """
    :type data: bytes.
    """
    return pickle.loads(
        base64.b64decode(data)
    )


json_encoder = JSONEncoder()
json_decoder = JSONDecoder()


def _encode_json(data):
    return json_encoder.encode(data).encode()


def _decode_json(data):
    return json_decoder.decode(data.decode())

encode = _encode_json
decode = _decode_json
