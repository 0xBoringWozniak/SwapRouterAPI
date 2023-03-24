import os

# HTTP Node URL (e.g. http://localhost:5000) or infura URL (e.g. https://mainnet.infura.io/v3/...)
HTTP_NODE = os.getenv('HTTP_NODE')

# Mongo URI to connect in format mongodb://<user>:<password>@<host>:<port>
MONGO_URI = os.getenv('MONGO_URI')
