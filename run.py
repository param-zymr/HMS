"""Application Entrypoint"""
from src.main import create_app
from src.app.config import app_settings

app = create_app()

app.app_context().push()

if __name__ == '__main__':
    app.run(host=app_settings.APP_HOST, port=app_settings.APP_PORT, debug=True)
