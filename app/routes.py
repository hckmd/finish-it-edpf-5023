from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Finish it - Home'
