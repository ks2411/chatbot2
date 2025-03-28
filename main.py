from flask import Flask, request, render_template, jsonify
from sales_bot import get_seller_answer

app = Flask(__name__)

history_user = []
history_manager = []
history_chat = []

@app.route("/", methods=["GET", "POST"])
def chat():
    global history_user, history_manager, history_chat

    if request.method == "POST":
        user_message = request.get_json().get("message")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        if user_message.lower() in ["выход", "exit", "quit"]:
            return jsonify({"response": "Chat closed"}), 200

        response = get_seller_answer(
            history_user=history_user + [user_message],
            history_manager=history_manager,
            history_chat=history_chat + [user_message]
        )

        history_user.append(user_message)
        history_chat.append(user_message)
        history_chat.append(response)

        return jsonify({"response": response}), 200

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)