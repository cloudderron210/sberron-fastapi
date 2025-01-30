from envparse import Env

env = Env()

DATABASE_URL = env.str(
    'DATABASE_URL',
    default='postgresql+psycopg2://derron:Cloudderron210!@194.120.116.89/debug2'
)

print(DATABASE_URL)
