import os

from v1 import create_app_v1

config_name = os.getenv('FLASK_CONFIG')
app_v1 = create_app_v1(config_name)

if __name__ == '__main__':
    app_v1.run()
    # app.run(host='0.0.0.0', port=8080, debug=True) # c9