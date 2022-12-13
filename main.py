import argparse
from pyapp.app import create_app
from pyapp.ext.dash import dash_app

if __name__ == '__main__':    
    parse = argparse.ArgumentParser()
    parse.add_argument('--command', required=False)
    args = parse.parse_args()
    
    app = create_app(args)
    
    with app.app_context() as ctx:
        dash_app.run(debug=True, host='0.0.0.0')