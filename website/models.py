from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_communities = db.relationship('UserCommunity')
    posts = db.relationship('Post')
    comments = db.relationship('Comment')

class Community(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    category = db.Column(db.String(150))
    posts = db.relationship('Post')
    user_communities = db.relationship('UserCommunity')

class UserCommunity(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_community_id = db.Column(db.Integer, db.ForeignKey('user_community.id'))

class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(300))
    text = db.Column(db.String(1000))
    comments = db.relationship('Comment')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Comment(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
