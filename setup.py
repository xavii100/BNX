from app.listener import Listener
from app import create_app

if __name__ == "__main__":
    create_app()
    listener = Listener()
    listener.check_file_inbox()