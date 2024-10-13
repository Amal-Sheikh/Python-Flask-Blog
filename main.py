import os  # Import os module for operating system dependent functionality
from datetime import datetime  # Import datetime for handling date and time
from flask import Flask, render_template, request, flash, redirect, url_for, session  # Import necessary Flask components for web development
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for ORM database operations
import json  # Import json module for working with JSON data
from werkzeug.utils import secure_filename  # Import secure_filename to safely save files
import math

# Load configuration parameters from a JSON file
with open("config.json", "r") as c:  # Open the config.json file in read mode
    params = json.load(c)["params"]  # Load parameters under the key "params" into a variable

app = Flask(__name__)  # Create an instance of the Flask class to initialize the application
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management (should be unique and secure)
app.config['UPLOAD_FOLDER'] = params['upload_location']  # Set the upload folder location from params
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]  # Set the database URI from params for database connection
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
db = SQLAlchemy(app)  # Initialize SQLAlchemy with the Flask app

# Define the Contacts model for the 'contacts' table in the database
class Contacts(db.Model):
    __tablename__ = 'contacts'  # Set the table name for this model
    sno = db.Column(db.Integer, primary_key=True)  # Define 'sno' as an integer primary key
    name = db.Column(db.Text, nullable=False)  # Define 'name' as a non-nullable text field
    email = db.Column(db.String(50), nullable=False)  # Define 'email' as a non-nullable string field
    phone_num = db.Column(db.String(20), nullable=False)  # Define 'phone_num' as a non-nullable string field
    msg = db.Column(db.Text, nullable=False)  # Define 'msg' as a non-nullable text field
    date = db.Column(db.DateTime, nullable=True, default=datetime.now)  # Define 'date' with current time as default

# Define the Posts model for the 'posts' table in the database
class Posts(db.Model):
    __tablename__ = 'posts'  # Set the table name for this model
    sno = db.Column(db.Integer, primary_key=True)  # Define 'sno' as an integer primary key
    title = db.Column(db.Text, nullable=False)  # Define 'title' as a non-nullable text field
    tagline = db.Column(db.Text, nullable=False)  # Define 'tagline' as a non-nullable text field
    slug = db.Column(db.String(25), nullable=False)  # Define 'slug' as a non-nullable string field
    content = db.Column(db.Text, nullable=False)  # Define 'content' as a non-nullable text field
    date = db.Column(db.DateTime, nullable=True, default=datetime.now)  # Define 'date' with current time as default
    img_file = db.Column(db.String(25), nullable=True)  # Define 'img_file' as a nullable string field


# Define the route for the home page
@app.route('/')
def home():
    # Query the database to get all posts from the Posts table
    posts = Posts.query.all()

    # Get the number of posts to display per page from params and convert it to an integer
    no_of_posts = int(params["no_of_posts"])

    # Calculate the total number of pages required to display all posts
    last = math.ceil(len(posts) / no_of_posts)

    # Get the current page number from the query parameters, default to 1 if not provided
    page = request.args.get('page', 1)

    # Check if the page number is a valid integer and at least 1
    if not str(page).isnumeric() or int(page) < 1:
        page = 1  # If invalid, set to the first page
    else:
        page = int(page)  # Convert the valid page number to an integer

    # Slice the posts list to get only the posts for the current page
    posts = posts[(page - 1) * no_of_posts: page * no_of_posts]


    # Initialize variables for pagination links
    if page == 1:  # If on the first page
        prev = "#"  # No previous page link
        next = f'/?page={page + 1}'  # Link to the next page
    elif page == last:  # If on the last page
        prev = f'/?page={page - 1}'  # Link to the previous page
        next = "#"  # No next page link
    else:  # If on any middle page
        prev = f'/?page={page - 1}'  # Link to the previous page
        next = f'/?page={page + 1}'  # Link to the next page


    # Render the HTML template 'index.html' with the context variables
    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)


# About route
@app.route("/about")  # Define the route for the about page
def about():
    return render_template("about.html", params=params)  # Render the about page

# Dashboard route for admin functions
@app.route("/dashboard", methods=["GET", "POST"])  # Define the route for the admin dashboard
def dashboard():
    if "user" in session and session["user"] == params["admin_dashboard"]:  # Check if user is logged in and is an admin
        posts = Posts.query.all()  # Fetch all posts from the database
        return render_template("dashboard.html", params=params, posts=posts)  # Render the dashboard with posts

    # Handle login if the request method is POST
    if request.method == "POST":
        username = request.form.get("uname")  # Get username from the form
        userpass = request.form.get("pass")  # Get password from the form

        # Check if the credentials match the admin credentials
        if username == params["admin_user"] and userpass == params["admin_password"]:
            session["user"] = params["admin_dashboard"]  # Set session variable for logged-in user
            return redirect(url_for('dashboard'))  # Redirect to the dashboard on successful login
        else:
            flash('Invalid credentials, please try again.', 'danger')  # Show flash message for invalid login
            return redirect(url_for('dashboard'))  # Redirect back to the dashboard

    return render_template("login.html", params=params)  # Render the login page if GET request

# Edit route for creating or editing posts
@app.route("/edit/<string:sno>", methods=["GET", "POST"])  # Define route to edit a post identified by sno
def edit(sno):
    if "user" in session and session["user"] == params["admin_dashboard"]:  # Check if user is logged in and is an admin
        if request.method == "POST":  # If the request is a POST
            # Get form data for creating or editing a post
            box_title = request.form.get('title')  # Get title from form
            tline = request.form.get('tline')  # Get tagline from form
            slug = request.form.get('slug')  # Get slug from form
            content = request.form.get('content')  # Get content from form
            img_file = request.form.get('img_file')  # Get image file name from form
            date = datetime.now()  # Get the current date and time

            # Check if sno is '0' for a new post
            if sno == '0':
                # Create a new post with the provided data
                post = Posts(title=box_title, slug=slug, content=content, tagline=tline, img_file=img_file, date=date)
                db.session.add(post)  # Stage the new post for insertion
                db.session.commit()  # Commit the changes to the database
            else:
                # Edit existing post by fetching it with the given sno
                post = Posts.query.filter_by(sno=sno).first()  # Fetch the post from the database
                if post:  # Check if the post exists
                    post.title = box_title  # Update title
                    post.slug = slug  # Update slug
                    post.content = content  # Update content
                    post.tagline = tline  # Update tagline
                    post.img_file = img_file  # Update image file name
                    post.date = date  # Update date
                    db.session.commit()  # Commit changes to the existing post
                    return redirect('/edit/' + sno)  # Redirect to the edit page after updating

        # If it's a GET request, fetch the post data for editing
        post = Posts.query.filter_by(sno=sno).first()  # Get the post by sno
        if post:  # Check if the post exists
            return render_template('edit.html', post=post, params=params)  # Render the edit page with existing post data

    return redirect(url_for('dashboard'))  # Redirect to dashboard if not authorized

# Route to view individual posts based on their slug
@app.route("/post/<string:post_slug>", methods=['GET'])  # Define route to view a post identified by its slug
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()  # Fetch the post by slug from the database
    if post is None:  # Check if the post was found
        flash('Post not found', 'danger')  # Show flash message if post not found
        return redirect(url_for('home'))  # Redirect to home if post not found

    return render_template("post.html", params=params, post=post)  # Render the post detail page with post data

# Uploader route for file uploads
@app.route('/uploader', methods=['GET', 'POST'])  # Define route for file uploads
def uploader():
    print("Session user:", session.get("user"))  # Debug: Check the current session user

    if "user" in session and session["user"] == params["admin_dashboard"]:  # Check if user is logged in and is an admin
        if request.method == "POST":  # If the request is a POST
            # Check if the file is part of the request
            if 'file1' not in request.files:
                print("No file part in the request")  # Debug output
                return "No file part", 400  # Return error if no file part

            f = request.files['file1']  # Get the file from the request

            # Check if the filename is empty
            if f.filename == '':
                print("No file selected")  # Debug output
                return "No selected file", 400  # Return error if no file is selected

            # Print filename for debugging
            print(f"File received: '{f.filename}'")  # Debug output
            filename = secure_filename(f.filename.strip())  # Secure the filename
            print(f"Secure filename: '{filename}'")  # Debug output
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Create the full file path
            print(f"File will be saved to: '{file_path}'")  # Debug output

            try:
                f.save(file_path)  # Save the file to the specified location
                print(f"File uploaded successfully at: {file_path}")  # Debug output
                return "Uploaded Successfully", 200  # Return success message
            except Exception as e:
                print(f"Error saving file: {e}")  # Debug output
                return "Error uploading file", 500  # Return error if save fails

    print("Unauthorized access attempt")  # Debug output for unauthorized access
    return "Unauthorized", 403  # Return unauthorized error

# Logout route to end user session
@app.route("/logout")  # Define route for logging out
def logout():
    session.pop("user", None)  # Remove user from session
    flash("You have been logged out successfully.", "success")  # Show flash message
    return redirect("/dashboard")  # Redirect to the dashboard


# Delete route for removing posts
@app.route("/delete/<string:sno>", methods=["GET", "POST"])  # Define route for deleting a post identified by sno
def delete(sno):
    if "user" in session and session["user"] == params["admin_dashboard"]:  # Check if user is logged in and is an admin
        post = Posts.query.filter_by(sno=sno).first()  # Fetch the post by sno
        if post:  # Check if the post exists
            db.session.delete(post)  # Delete the post
            db.session.commit()  # Commit the deletion
        else:
            print(f"Post with sno {sno} not found.")  # Debug output if post not found
    else:
        print("Unauthorized access attempt")  # Debug output for unauthorized access

    return redirect('/dashboard')  # Redirect back to the dashboard

# Contact route for handling messages from users
@app.route('/contact', methods=['GET', 'POST'])  # Define route for the contact page
def contact():
    if request.method == 'POST':  # Handle POST request for submitting the contact form
        # Get form data
        name = request.form.get('name')  # Get name from form
        email = request.form.get('email')  # Get email from form
        phone = request.form.get('phone_num')  # Get phone number from form
        msg = request.form.get('msg')  # Get message from form

        # Validate form fields
        if not all([name, email, phone, msg]):
            flash('All fields are required!', 'danger')  # Show flash message for incomplete form
            return redirect(url_for('contact'))  # Redirect back to contact page

        # Create a new contact entry in the database
        entry = Contacts(name=name, email=email, phone_num=phone, msg=msg)
        try:
            db.session.add(entry)  # Stage the new contact entry for insertion
            db.session.commit()  # Commit the changes to the database
            flash('Your message has been sent successfully!', 'success')  # Show success message
            return redirect(url_for('contact'))  # Redirect back to contact page
        except Exception as e:
            db.session.rollback()  # Rollback changes in case of error
            flash('There was an error sending your message. Please try again.', 'danger')  # Show error message

    posts = Posts.query.all()  # Fetch all posts for display on the contact page
    return render_template("contact.html", params=params, posts=posts)  # Render the contact page

# Main entry point of the application
if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode



# http://127.0.0.1:5000/post/first-post






