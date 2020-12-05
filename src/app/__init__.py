import os
import pickle
import requests
import subprocess

from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

if os.getenv('WHEREAMI') == 'local':
    with open("/Users/vanessacai/big_data/pf_vals.pickle", 'rb') as f:
        pf_vals = pickle.load(f)

    with open("/Users/vanessacai/big_data/pf_keys.pickle", 'rb') as f:
        pf_keys = pickle.load(f)
else:
    r = requests.get("https://vycai-proj-2.s3.us-east-2.amazonaws.com/pf_keys.pickle")
    pf_keys = pickle.loads(r.content)

    r = requests.get("https://vycai-proj-2.s3.us-east-2.amazonaws.com/pf_vals.pickle")
    pf_vals = pickle.loads(r.content)


from app import routes