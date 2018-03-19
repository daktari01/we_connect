import os

from v1 import create_app_v1
from v2 import create_app_v2

config_name = os.getenv('FLASK_CONFIG')
# app_v1 = create_app_v1(config_name)
app_v2 = create_app_v2(config_name)

if __name__ == '__main__':
    # app_v1.run()
    # app_v2.run()
    # # c9
    # app_v1.run(host='0.0.0.0', port=8080, debug=True) 
    app_v2.run(host='0.0.0.0', port=8080, debug=True)