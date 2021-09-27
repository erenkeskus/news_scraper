import os
from .logging_setup import construct_logger

app_root = os.environ['ROOT'] 
db_uri = os.environ['DB_URI'] 
construct_logger()