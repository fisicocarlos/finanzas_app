from app import create_app
from app.data.drive_reader import fetch_and_store_transactions

fetch_and_store_transactions()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
