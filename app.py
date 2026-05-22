from frontend import create_app
from modules.config import DEFAULT_DEBUG, DEFAULT_HOST, DEFAULT_PORT


app = create_app()

if __name__ == "__main__":
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=DEFAULT_DEBUG)
