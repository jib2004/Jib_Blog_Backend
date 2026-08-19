from email import message

from flask import Blueprint,request,jsonify,session
from exceptions.exceptions import handle_validation_error,unauthorized,not_found
from config.db import db
from model import Blog

blog = Blueprint('blog', __name__)

@blog.get('/')
def get_all_blogs():
    blogs = Blog.query.all()
    return jsonify([{
        'id':      b.id,
        'title':   b.title,
        'content': b.content,
    } for b in blogs]), 200


@blog.get('/<string:blog_id>')
def get_single_blog(blog_id):
    blog = db.session.get(Blog, blog_id)
    if not blog:
        return jsonify({'message': 'Blog not found'}), 404
    return jsonify({
        'id':      blog.id,
        'title':   blog.title,
        'content': blog.content,
    }), 200


@blog.post('/')
def create_blog():
    data = request.get_json()
    title   = data.get('title')
    content = data.get('content')
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'message': 'User not found'}), 404

    if not title or not content:
        jsonify({"message":'Title and content are required'}),400

    new_blog = Blog(title=title, content=content, user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    return jsonify({'message': 'Blog created successfully'}), 201


@blog.put('/<string:blog_id>')
def update_blog(blog_id):
    blog = db.session.get(Blog, blog_id)
    if not blog:
        return jsonify({'message': 'Blog not found'}), 404

    data = request.get_json()
    blog.title   = data.get('title', blog.title)     # ← keeps old value if not provided
    blog.content = data.get('content', blog.content)
    db.session.commit()
    return jsonify({'message': 'Blog updated successfully'}), 200


@blog.delete('/<string:blog_id>')
def delete_blog(blog_id):
    blog = db.session.get(Blog, blog_id)
    if not blog:
        return jsonify({'message': 'Blog not found'}), 404

    db.session.delete(blog)
    db.session.commit()
    return jsonify({'message': 'Blog deleted successfully'}), 200