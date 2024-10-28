from flask import Flask, render_template, jsonify, request, url_for
import json

from werkzeug.utils import redirect

app = Flask(__name__)

def load_posts():
    """
    Load blog posts from the JSON file.

    :return: List of blog posts as dictionaries.
    """
    with open('blog_data.json', 'r') as f:
        return json.load(f)

def save_posts(posts):
    """
    Save blog posts to the JSON file.

    :param posts: List of blog posts to save.
    """
    with open('blog_data.json', 'w') as f:
        return json.dump(posts, f, indent=4)

@app.route('/')
def index():
    """
    Display the main blog page with all blog posts.

    :return: Rendered HTML template for the index page.
    """
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
# @app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle adding a new blog post.
    - GET request: Show the form to add a new post.
    - POST request: Process form data and add the post to the list.

    :return: Redirect to index page after adding the post or render add page on GET request.
    """
    if request.method == 'POST':
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")

        posts = load_posts()

        new_post = {
            "id": len(posts) + 1,
            "author": author,
            "title": title,
            "content": content,
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route("/delete/<int:post_id>", methods=['POST'])
def delete(post_id):
    """
    Handle deleting a blog post by its ID.

    :param post_id: ID of the post to delete.
    :return: Redirect to index page after deleting the post.
    """
    with open('blog_data.json', 'r') as file:
        posts = json.load(file)


    posts = [post for post in posts if post["id"] != post_id]

    with open('blog_data.json', 'w') as file:
        json.dump(posts, file, indent=4)

    return redirect(url_for('index'))

@app.route("/update/<int:post_id>", methods=['GET', 'POST'])
def update(post_id):
    """
    Handle updating a blog post by its ID.
    - GET request: Show the form to update the post.
    - POST request: Process form data and update the post.

    :param post_id: ID of the post to update.
    :return: Redirect to index page after updating or render update page on GET request.
    """
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if not post:
        return jsonify({'error': 'post not found'}), 404

    if request.method == 'POST':
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")

        save_posts(posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)