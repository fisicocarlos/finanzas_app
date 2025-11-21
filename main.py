from app import create_app
from app.data.drive_reader import load_data

load_data()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
