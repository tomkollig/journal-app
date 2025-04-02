"""A simple journal API"""

from flask import Flask, request

from entry_functions import load_all_entries, is_valid_entry, save_new_entry

api = Flask(__name__)


@api.get("/")
def index():
    return {
        "message": "Welcome to the writing app API."
    }


@api.route("/entry", methods=["GET", "POST"])
def get_or_create_entries():
    """Endpoint to manage entries"""
    if request.method == "GET":
        entries = load_all_entries()
        args = request.args

        if "author" in args:
            author = args["author"]
            entries = [entry for entry in entries
                       if entry["author"] == author]

        return entries
    else:
        new_entry = request.json

        if is_valid_entry(new_entry):
            created_entry = save_new_entry(new_entry)
            return created_entry, 201
        else:
            return {"error": True, "message": "Invalid entry."}, 400


if __name__ == "__main__":
    api.run(debug=True, port=5000)
