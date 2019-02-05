import sys
import os

apps_dir = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'apps')))
sys.path.append(apps_dir)