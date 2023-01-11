import flask
import os
import dotenv
from utils.discord_utils import *
from utils.discord_db import *

app=flask.Flask(__name__)

dotenv.load_dotenv()

login_cookie=user=None


@app.route("/")
def main():
    global login_cookie, user
    login_cookie=flask.request.cookies.get('login')
    if login_cookie is not None:
        user=get_user_info(get_access_token(login_cookie))
        if user is None:
            data=update_user_tokens(get_refresh_token(login_cookie))
            update_tokens(login_cookie, data["access_token"], data["refresh_token"])
        user=get_user_info(get_access_token(login_cookie))
    print(user)
    return flask.render_template("index.html",login_cookie=login_cookie, user=user)


@app.route('/login')
def login():
    login_cookie=flask.request.cookies.get('login')
    if login_cookie is not None:
        return flask.redirect('/')
    elif flask.request.args.get("code") is not None:
        code=flask.request.args.get("code")
        data=get_user_tokens(code)
        if data is not None:
            response=flask.make_response(flask.redirect('/'))
            id=get_user_info(data["access_token"]).get("id")
            (hashed_id, salt)=create_cookie_hash(id)
            add_user(hashed_id, salt, data["access_token"], data["refresh_token"])
            response.set_cookie('login', hashed_id, max_age=315360000)
            return response
        else:
            return "Login Failed!"
    elif flask.request.args.get("error") is not None:
        return "Login Failed!"
    else:
        return flask.redirect(get_discord_auth_url())
@app.route('/logout')
def logout():
    login_cookie=flask.request.cookies.get('login')
    delete_user(login_cookie)
    response=flask.make_response(flask.redirect('/'))
    response.set_cookie('login', expires=0)
    return response

@app.route('/problem-dispenser')
def problem_dispenser():
    global login_cookie, user
    return flask.render_template("index.html",login_cookie=login_cookie, user=user)

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')