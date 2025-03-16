from dify_app import DifyApp
from models import db
from extensions import oracle_dialect ##Oracle

def init_app(app: DifyApp):
    db.init_app(app)
