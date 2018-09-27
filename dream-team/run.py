# run.py

import os

from app import create_app

#config_name = os.getenv('development')
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
