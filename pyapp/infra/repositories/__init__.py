from pyapp.ext.database import db
from flask_sqlalchemy.pagination import Pagination


def paginator(model, current_page, per_page=10, error_out=False) -> Pagination:
    return db.paginate(model, page=current_page, per_page=per_page, error_out=error_out)