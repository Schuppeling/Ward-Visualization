import configparser

config = configparser.ConfigParser()
config.read("resources/local.properties")

api_key = config["global"]["api_key"]
solo_queue_id = config["global"]["solo_queue_id"]