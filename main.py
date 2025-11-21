from app import create_app
from app.data.sync_transactions import sync_transactions

sync_transactions()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
