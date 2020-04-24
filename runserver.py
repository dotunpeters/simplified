"""
This script runs the simplified application using a development server.
"""

from simplified import app


if __name__ == '__main__':
    #heroku port
    port = int(os.environ.get("PORT", 5000))
    app.run(host=port)
