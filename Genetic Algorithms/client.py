import json
import requests
import numpy as np

API_ENDPOINT = 'http://10.4.21.156'
MAX_DEG = 11
SECRET_KEY = "LTSCro3XJ8t8dYv4auyWiNRX38W04vA157S780x57ponUc5sC1"

best_vector = [0.00000000e+00, -1.04844750e-13, -1.99474870e-13,  4.01885848e-11,
                0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,
                -1.42273480e-07, -1.79418130e-10,  0.00000000e+00]

def urljoin(root, path=''):
    if path:
        root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root


def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id': id, 'vector': vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response


def get_errors(id, vector):
    for i in vector:
        assert 0 <= abs(i) <= 10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(id, vector, 'geterrors'))


def get_overfit_vector(id):
    return json.loads(send_request(id, [0], 'getoverfit'))


def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    """
    for i in vector:
        assert 0 <= abs(i) <= 10
    assert len(vector) == MAX_DEG
    return send_request(id, vector, 'submit')

# Replace 'SECRET_KEY' with your team's secret key (Will be sent over email)
if __name__ == "__main__":
    print(submit(SECRET_KEY, best_vector))
