from environs import Env
env = Env()
env.read_env()
origin_db=env.str("origin_db")
origin_host=env.str("origin_host")
origin_user=env.str("origin_user")
origin_pass=env.str("origin_pass")
origin_ssl=env.bool("origin_ssl")
origin_session=env.str("origin_session")
destination_db=env.str("destination_db")
destination_host=env.str("destination_host")
destination_user=env.str("destination_user")
destination_pass=env.str("destination_pass")
destination_ssl=env.bool("destination_ssl")
destination_session=env.str("destination_session")