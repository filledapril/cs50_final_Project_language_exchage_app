import os
import math

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from helpers import login_required, error_message, check_email
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#database
# db = SQL("sqlite:///langex.db")
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # check if username and password are valid
        if not username or not password:
            return error_message("Invalid username or/and password", 400)
        # match user from database
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        # check username exists and password correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return error_message("Invalid username or password", 403)
        if check_password_hash(user[0]["hash"], password):
            print('correct')
        else:
            print(f'incorrect saved:{user[0]["hash"]} and input:{password}')

        # remember user
        session["user_id"] = user[0]["id"]
        return redirect(url_for("profile"))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        print(username, password, password2)
        #check username and password

        if not username or not password or not password2:
            return error_message("Username and/or Password invalid.", 409)
        if password != password2:
            return error_message("Password not matched.", 409)

        #check if username already exit
        user = db.execute("SELECT username FROM users WHERE username = ?", username)
        if user:
            return error_message("Username already exists", 409)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        return render_template("login.html")

    else:
        return render_template('register.html')

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/home-chart", methods=["GET"])
def home_chart():
    if request.method == "GET":
        data = {}
        top_3_languages = db.execute("""
                                    SELECT
                                        learn as name,
                                        COUNT(DISTINCT userId) as count
                                    FROM
                                        posts
                                    GROUP BY
                                        learn
                                    ORDER BY
                                        count DESC
                                    LIMIT 3""")
        if not top_3_languages:
            return jsonify(success=False, error="No enough posts")
        language_dict = {top["name"]:top["count"] for top in top_3_languages}
        print(language_dict)
        for l in language_dict:
            # get a totol learner number
            remain = language_dict[l]
            total = remain
            print(f"total: {total}")
            top_3_countries = db.execute("""
                                    SELECT
                                        countries.name as country,
                                        COUNT(DISTINCT users.id) as count
                                    FROM
                                        posts
                                    INNER JOIN
                                        users ON posts.userId = users.id
                                    INNER JOIN
                                        countries ON users.countryId = countries.id
                                    WHERE
                                        posts.learn = ?
                                    GROUP BY
                                        countries.name
                                    ORDER BY
                                        count DESC
                                    LIMIT 3""", l)
            for c in top_3_countries:
                remain -= c['count']
                percentage = round((c['count'] / total) * 100, 1)
                if l not in data:
                    data[l] = []
                data[l].append({c['country'] : percentage})
            data[l].append({'others': remain})
        return jsonify(data)


@app.route("/navbar")
@login_required
def navbar():
    # pass user via data
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    if not username:
        print("username unavailable")
        session.clear()
        # Redirect user to login form
        return redirect(url_for("login"))
    try:
        has_new_message = db.execute("SELECT read FROM messages WHERE receiverId = ? AND read = ?", session["user_id"], None)
        if has_new_message:
            print("new message")
            return jsonify(username = username, has_new_message=True)
        else:
            print("no new message")
            return jsonify(username = username, has_new_message=False)
    except Exception as e:
        return jsonify(username = username, has_new_message=False, error=str(e))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # pass user and country list via data
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    countries = db.execute("SELECT * FROM countries")
    flag_src = "../static/waiting.png"
    if request.method == "POST":
    # validate input value
        email = request.form.get("email")
        #country = request.form.get("country")
        country_id = request.form.get("country")
        print(email, country_id)
    # pass data to database
        if not user[0]["countryId"]:
            if not country_id:
                return error_message("Please select a country.", 409)
            # since country value set to be id, no need to check exist
            #country_id = db.execute("SELECT id FROM countries WHERE name = ?", country)
            #if len(country_id) != 1:
                return ("Please provide a correct country name.", 409)
            #db.execute("UPDATE users SET countryId = ? WHERE id = ?", country_id[0]["id"], session["user_id"])
            db.execute("UPDATE users SET countryId = ? WHERE id = ?", country_id, session["user_id"])
        else:
            flag_src = db.execute("SELECT flag FROM countries WHERE id = ?", user[0]["countryId"])[0]["flag"]
        if email:
            if check_email(email) == False:
                return error_message("Please provide a correct email address.", 409)
            else:
                db.execute("UPDATE users SET email = ? WHERE id = ?", email, session["user_id"])
        return redirect(url_for("profile"))

    else:
        return render_template("profile.html", user = user, countries = countries, flag_src = flag_src)

@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    # pass user and country list via data
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    countries = db.execute("SELECT * FROM countries")
    flag_src = db.execute("SELECT flag FROM countries WHERE id = ?", user[0]["countryId"])[0]["flag"]
    #if user change something
    if request.method == "POST":
        email = request.form.get("email")
        country_id = request.form.get("country")
        if email != user[0]["email"]:
            if check_email(email) == False:
                    return error_message("Please provide a correct email address.", 409)
            else:
                db.execute("UPDATE users SET email = ? WHERE id = ?", email, session["user_id"])
        if country_id != user[0]["countryId"]:
                db.execute("UPDATE users SET countryId = ? WHERE id = ?", country_id, session["user_id"])
        return redirect(url_for("profile"))
    else:
        return render_template("edit-profile.html", user = user, countries = countries, flag_src = flag_src)

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    languages_dict = db.execute("SELECT name FROM languages")
    languages = [lang['name'] for lang in languages_dict]
    # pass user and country list via data
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    flag_src = db.execute("SELECT flag FROM countries WHERE id = ?", user[0]["countryId"])[0]["flag"]
    # get input value
    if request.method == "POST":
        speak = request.form.get("speak")
        learn = request.form.get("learn")
        intro = request.form.get("intro")
        like = 0
        print(speak, learn, intro)
        if not speak or not learn or not intro:
            return error_message("Information of post can not be empty.", 409)
        try:
            db.execute("INSERT INTO posts(userId, speak, learn, intro, likes) VALUES(?, ?, ?, ?, ?)", session["user_id"], speak, learn, intro, like)
            return redirect(url_for('explore', offset=1))
        except Exception as e:
            print(f"post error: {e}")
            return render_template("post.html", user = user, flag_src = flag_src, languages = languages, error = e)
    else:
        return render_template("post.html", user = user, flag_src = flag_src, languages = languages, error = None)

@app.route("/explore")
@login_required
def render_explore():
    return redirect(url_for('explore', offset=1))

@app.route("/explore/filter")
@login_required
def render_explore_filter():
    return redirect(url_for('explore', offset=1))

@app.route("/explore/<int:offset>")
@login_required
def explore(offset):
    # session status
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    # filters options
    country_list = db.execute("SELECT DISTINCT countries.name FROM countries INNER JOIN users ON countries.id = users.countryId INNER JOIN posts ON users.id = posts.userId ORDER BY countries.name ASC")
    speak_list = db.execute("SELECT DISTINCT speak FROM posts ORDER BY speak ASC")
    learn_list = db.execute("SELECT DISTINCT learn FROM posts ORDER BY learn ASC")
    return render_template("explore.html",
                            user = user,
                            country_list = country_list,
                            speak_list = speak_list,
                            learn_list = learn_list)

@app.route("/api/explore")
def api_explore():
    items_per_page = 2
    delete = False
    # check all post data
    total = db.execute("SELECT COUNT(*) AS rows FROM posts")[0]["rows"]
    if not total:
        redirect(url_for('post'))
    # get offset
    offset = request.args.get('offset', default = 1, type = int)
    # get filters
    speak = request.args.get('speak')
    learn = request.args.get('learn')
    country = request.args.get('country')
    my = request.args.get('my')
    # get delete post id
    delete_post_id = request.args.get('delete')
    print(f"delete id {delete_post_id}")
    # check delete id valid
    delete_post = db.execute("SELECT * FROM posts WHERE id = ?", delete_post_id)
    # check language value valid
    languages_dict = db.execute("SELECT name FROM languages")
    languages = [lang['name'] for lang in languages_dict]
    if speak is not None and speak not in languages:
        return jsonify(success = False, error="Invalid language provided")
    if learn is not None and learn not in languages:
        return jsonify(success = False, error="Invalid language provided")
    # check country value valid
    countries_dict = db.execute("SELECT name FROM countries")
    countries = [country['name'] for country in countries_dict]
    if country is not None and country not in countries:
        return jsonify(success = False, error="Invalid country provided")
    # current user status
    current_user_liked = db.execute("SELECT postId FROM likes WHERE userId = ?", session["user_id"])
    current_user_saved = db.execute("SELECT postId FROM saved WHERE userId = ?", session["user_id"])
    current_user_id = session["user_id"]
    # delete post
    if delete_post:
        try:
            db.execute("DELETE FROM posts WHERE id = ?", delete_post_id)
            delete = True
        except Exception as e:
            return jsonify(delete=False, error="delete failed.")
    # apply filters
    parameters = []
    query = """
        SELECT
            posts.id AS postId,
            posts.userId,
            posts.speak,
            posts.learn,
            posts.likes,
            posts.intro,
            posts.date,
            users.username,
            users.email,
            countries.flag
        FROM
            posts
        INNER JOIN
            users ON posts.userId = users.id
        INNER JOIN
            countries ON users.countryId = countries.id"""
    if speak is not None:
        parameters.append(speak)
        if "WHERE" in query:
            query += " AND posts.speak = ?"
        else:
            query += " WHERE posts.speak = ?"
    if learn is not None:
        parameters.append(learn)
        if "WHERE" in query:
            query += " AND posts.learn = ?"
        else:
            query += " WHERE posts.learn = ?"
    if country is not None:
        parameters.append(country)
        if "WHERE" in query:
            query += " AND countries.name = ?"
        else:
            query += " WHERE countries.name = ?"
    if my:
        parameters.append(session["user_id"])
        if "WHERE" in query:
            query += " AND posts.userId = ?"
        else:
            query += " WHERE posts.userId = ?"
    total_query = query
    final_query = query + " ORDER BY posts.id DESC LIMIT 2 OFFSET ?"
    if parameters:
        try:
            posts_data = db.execute(final_query, *parameters, items_per_page * (offset - 1))
        except Exception as e:
            return jsonify(success=False, error=str(e))
        total_data = db.execute(total_query, *parameters)
    else:
        try:
            posts_data = db.execute(final_query, items_per_page * (offset - 1))
        except Exception as e:
            return jsonify(success=False, error=str(e))
        total_data = db.execute(total_query)
    # get number of all for paginagtion
    total_rows = len(total_data)
    max_offset = math.ceil(total_rows /  float(items_per_page))
    print(f"total rows: {total_rows}, max offset: {max_offset}")
    if offset < 0 or offset > total_rows:
        return jsonify(success=False)
    if not posts_data:
        posts_data = None
    # Convert posts to JSON and return
    if delete:
        return jsonify(posts_data, current_user_liked, current_user_saved, current_user_id, max_offset, delete)
    else:
        return jsonify(posts_data, current_user_liked, current_user_saved, current_user_id, max_offset)


@app.route('/like-action', methods=['POST'])
@login_required
def handle_like():
    data = request.get_json()
    post_id = data['post_id']
    if not post_id:
        return jsonify(success=False, error="No post ID provided")
    post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
    if not post or len(post) != 1:
        return jsonify(success=False, error="Post not found")
    is_liked = db.execute("SELECT id FROM likes WHERE postId = ? AND userId = ?", post_id, session["user_id"])
    if not is_liked:
        try:
            db.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", post_id)
            db.execute("INSERT INTO likes(userId, postId) VALUES(?, ?)", session["user_id"], post_id)
            post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
            return jsonify(success=True, post=post, isLiked=True)
        except Exception as e:
            return jsonify(success=False, error=str(e))
    else:
        try:
            db.execute("UPDATE posts SET likes = likes - 1 WHERE id = ?", post_id)
            db.execute("DELETE FROM likes WHERE userId =? AND postId = ?", session["user_id"], post_id)
            post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
            return jsonify(success=True, post=post, isLiked=False)
        except Exception as e:
            return jsonify(success=False, error=str(e))

@app.route("/save-action", methods=["POST"])
@login_required
def handle_save():
    data = request.get_json()
    post_id = data['post_id']
    if not post_id:
        return jsonify(success=False, error="No post ID provided")
    post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
    if not post or len(post) != 1:
        return jsonify(success=False, error="Post not found")
    is_saved = db.execute("SELECT id FROM saved WHERE userId = ? AND postId = ?", session["user_id"], post_id)
    # save action
    if not is_saved:
        try:
            db.execute("INSERT INTO saved(userId, postId) VALUES(?, ?)", session["user_id"], post_id)
            return jsonify(success=True, isSaved=True)
        except Exception as e:
            return jsonify(success=False, error=str(e))
    else:
        try:
            db.execute("DELETE FROM saved WHERE userId =? AND postId = ?", session["user_id"], post_id)
            return jsonify(success=True, isSaved=False)
        except Exception as e:
            return jsonify(success=False, error=str(e))

@app.route("/send-message", methods=["POST"])
@login_required
def send_message():
    data = request.get_json()
    post_id = data['post_id']
    message = data['message']
    if not post_id or not message:
        return jsonify(success=False, error="No post ID or message provided")
    post = db.execute("SELECT * FROM posts WHERE id = ?", post_id)
    if not post or len(post) != 1:
        return jsonify(success=False, error="Post not found")
    receiver_id = db.execute("SELECT userId FROM posts WHERE id = ?", post_id)[0]['userId']
    if not receiver_id:
        return jsonify(success=False, error="User not found")
    try:
        db.execute("INSERT INTO messages(senderId, receiverId, message) VALUES(?, ?, ?)", session["user_id"], receiver_id, message)
        return jsonify(success=True, isSent=True)
    except Exception as e:
        print (str(e))
        return jsonify(success=False, isSent=False, error=str(e))

@app.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    if request.method == "POST":
        data = request.get_json()
        readId = data.get("msgId", None)
        deleteId = data.get("deletId", None)
        receiverId = data.get("receiverId", None)
        messageText = data.get("message", None)
        if readId:
            try:
                read = db.execute("SELECT read FROM messages WHERE id = ?", readId)
                if read and read[0]["read"] != 1:
                    db.execute("UPDATE messages SET read = ? WHERE id = ?", 1, readId)
            except Exception as e:
                return jsonify(success=False, error=str(e))
            return jsonify(success=True)
        if deleteId:
            try:
                deleteMsg = db.execute("SELECT read FROM messages WHERE id = ?", deleteId)
                if deleteMsg:
                    db.execute("DELETE FROM messages WHERE id = ?", deleteId)
                else:
                    redirect(url_for('messages'))
            except Exception as e:
                return jsonify(success=False, error=str(e))
            return jsonify(success=True)
        if not receiverId and messageText:
            print("no receiver")
            return jsonify(success=False, error="no receiver")
        if receiverId and not messageText:
            print("no message")
            return jsonify(success=False, error="no message")
        if receiverId and messageText:
            try:
                db.execute("INSERT INTO messages(senderId, receiverId, message) VALUES(?, ?, ?)", session["user_id"], receiverId, messageText)
                return jsonify(success=True)
            except Exception as e:
                return jsonify(success=False, error=str(e))
    else:
        try:
            messages = db.execute("""
                                    SELECT
                                        messages.id AS msgId,
                                        messages.message,
                                        messages.read,
                                        messages.senderId,
                                        users.username AS senderName
                                    FROM
                                        messages
                                    INNER JOIN
                                        users
                                    WHERE
                                        messages.senderId = users.id
                                    AND messages.receiverId = ?""",
                                        session["user_id"])
        except Exception as e:
            print (str(e))
            return jsonify(success=False, error=str(e))
    # pass user via data
    # user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("messages.html", messages = messages)


@app.route("/saved", methods=["GET", "POST"])
@login_required
def saved():
    if request.method == "POST":
        data = request.get_json()
        receiver_id = data.get("receiverId", None)
        message = data.get("messageText", None)
        deleteId = data.get("savedId", None)
        # delete from saved
        if deleteId:
            #check if post exist in saved
            saved = db.execute("SELECT * FROM saved WHERE id = ?", deleteId)
            if not saved:
                return jsonify(success=False, isDelete=False, error="You did not save this post. Refresh the page.")
            else:
                try:
                    db.execute("DELETE FROM saved WHERE id =?", deleteId)
                    return jsonify(success=True, isDelete=True)
                except Exception as e:
                    return jsonify(success=False, isDelete=False, error=str(e))
        # check if user exist and store message to db
        if receiver_id and not message:
            print("Error: no message provided.")
            return jsonify(success=False, isSent=False)
        if not receiver_id and message:
            print("Error: no receiver id provided.")
            return jsonify(success=False, isSent=False)
        receiver = db.execute("SELECT * FROM users WHERE id = ?", receiver_id)
        if not receiver:
            return jsonify(success=False, error="Failed to send message. User no longer exist.")
        else:
            try:
                db.execute("INSERT INTO messages(senderId, receiverId, message) VALUES(?, ?, ?)", session["user_id"], receiver_id, message)
                return jsonify(success=True, isSent=True)
            except Exception as e:
                return jsonify(success=False, isSent=False, error=str(e))
    else:
        saved_list = db.execute("""
                                SELECT
                                    saved.id AS savedId,
                                    posts.id AS postId,
                                    posts.userId,
                                    posts.speak,
                                    posts.learn,
                                    posts.likes,
                                    posts.intro,
                                    users.username,
                                    users.email,
                                    countries.flag
                                FROM
                                    saved
                                INNER JOIN
                                    posts ON saved.postId = posts.id
                                INNER JOIN
                                    users ON posts.userId = users.id
                                INNER JOIN
                                    countries ON users.countryId = countries.id
                                WHERE saved.userId = ?
                                ORDER BY saved.id DESC
                                """, session["user_id"])
        # pass user via data
        #user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("/saved.html", saved_list = saved_list)
