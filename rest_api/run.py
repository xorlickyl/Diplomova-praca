from flask import Flask

def create_app():
    app = Flask(__name__)
    from rest_api.main import app_bl
    app.register_blueprint(app_bl, url_prefix='/api')
    return app

if __name__ == '__main__':
    app=create_app()
    #app.run(host='147.175.106.115:7799')
    app.run(debug=True,host='127.0.0.1')
