import os

input_path = 'files/input.json'
output_path = 'files/output.json'
nesting_keys = ["currency", "country", "city"]
local_user = "candidate"
local_password = os.getenv("local_password", "change_me")
