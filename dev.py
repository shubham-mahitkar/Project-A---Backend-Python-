"""
Development Server
==================

This server is for development purposes only. It turns on the necessary
flags to allow quick reloads (no need to restart the server after making
changes), and debug flags. It also provides a development server which
launches the application (not suitable for production).
"""
import os
from users.app import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='localhost', debug=True, port=port)
