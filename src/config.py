from environs import Env

env = Env()
# Read .env into os.environ
env.read_env()


class Settings:
    CMC_API_KEY = env.str("CMC_API_KEY")
