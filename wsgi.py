from app import create_app
# import bjoern
from dotenv import load_dotenv

from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
app = create_app()

if __name__ == "__main__":
    app.run()
    # bjoern.run(app, 'unix:' + app.config.get("WSGI_SOCKET"))
