import pickle

from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

PF_VALS_LOCAL_PATH = "/Users/vanessacai/big_data/pf_vals.pickle"
PF_KEYS_LOCAL_PATH = "/Users/vanessacai/big_data/pf_keys.pickle"

PF_VALS_HDFS_PATH = "hdfs:///tmp/vycai/pf_vals.pickle"
PF_KEYS_HDFS_PATH = "hdfs:///tmp/vycai/pf_keys.pickle"

with open(PF_VALS_LOCAL_PATH, 'rb') as pickle_file:
    pf_vals = pickle.load(pickle_file)

with open(PF_KEYS_LOCAL_PATH, 'rb') as pickle_file:
    pf_keys = pickle.load(pickle_file)

from app import routes