"""
This script runs the simplified application using a development server.
"""

import os
from simplified import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,port=port)
