import argparse
from pyapp.app import create_app, run_dash

if __name__ == '__main__':    
    parse = argparse.ArgumentParser()
    parse.add_argument('--command', required=False)
    args = parse.parse_args()
    
    run_dash(args)