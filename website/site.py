import os
import config

from flask import Flask, render_template, abort, g, request
from distros_installs import distros_installs

from flask.ext.babel import Babel

app = Flask(__name__)
app._static_folder = os.getcwd() + '/website/static'
app.config['SECRET_KEY'] = os.urandom(64)
if app.debug:
    from flaskext.lesscss import lesscss
    lesscss(app)
#app.config.from_pyfile('translations.cfg')
babel = Babel(app, default_locale="en_US.ISO8859-1")

from events import get_rss

from flask_wtf.csrf import CsrfProtect

CsrfProtect(app)


'''
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token        
'''


@babel.localeselector
def get_locale():
    lang = request.cookies.get('lang')
    if lang in config.LANGUAGES:
        return lang
    return request.accept_languages.best_match(config.LANGUAGES)

@app.route('/')
def index():
    #from placeholders import news, events, press, security
    return render_template('index.html',
            news=get_rss('news')[:5],
            events=get_rss('upcoming')[:5],
            press=get_rss('press')[:5],
            security=get_rss('security')[:5],
    )

@app.route('/about')
def about():
    return render_template('about/index.html')

@app.route('/docs')
def docs():
    return render_template('docs/index.html')

@app.route('/community')
def community():
    return render_template('community/index.html')

@app.route('/developers')
def developers():
    return render_template('developers/index.html')

@app.route('/support')
def support():
    return render_template('support/index.html')

@app.route('/download/<distro>')
def simple_install(distro=None):
    distro = distros_installs.get(distro)
    if not distro: abort(404)
    return render_template('simple_install.html', distro=distro)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='run website.')
    parser.add_argument('--debug', action='store_true', help='run in debug mode')
    parser.add_argument('--host', default='127.0.0.1', help='what ip to bind to')
    parser.add_argument('--port', type=int, default=5000, help='what port to bind to')
    args = parser.parse_args()
    if args.host == '*':
        args.host = '0.0.0.0'

    app.run(debug=args.debug, host=args.host, port=args.port)

