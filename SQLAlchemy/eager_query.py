from sqlalchemy import select
from sqlalchemy.orm import defaultload, joinedload, selectinload, subqueryload, immediateload

from models import Detail, Post, User, session

query = session.query(User)
print(query.all())

query = session.query(User).options(selectinload(User.posts))
print(query.all())