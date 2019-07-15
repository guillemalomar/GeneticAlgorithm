from settings import ENVIRONMENT_PARAMS
from src.model import Environment


my_env = Environment()
ENVIRONMENT = my_env.create(**ENVIRONMENT_PARAMS)
