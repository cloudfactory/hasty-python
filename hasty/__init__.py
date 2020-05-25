import uuid

# Global variables
api_key = None
api_base = 'https://api.staging.dev.hasty.ai'
api_session = str(uuid.uuid4())

# API Resources
from .api_resources import *
