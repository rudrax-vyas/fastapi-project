from sqlalchemy.orm import contains_eager, joinedload
from models import Detail, Post, User, session

print("=" *40)
print("\n Loading with the: 'joinedload' function")
query = (
    session.query(User)
    .options(joinedload(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
    
)
print(query)
print(query.all())

print("=" *40)
print(" \n Loading with the: 'contains_eager' function")
query = (
    session.query(User)
    .outerjoin(Post)
    .options(contains_eager(User.posts))
    .filter(Post.detail.has(Detail.id == 1))
    
)
print(query)
print(query.all())