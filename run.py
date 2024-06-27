from app import create_app

App = create_app()

if __name__ == '__main__':
    App.run(debug=True)
    App.run(port=5000)