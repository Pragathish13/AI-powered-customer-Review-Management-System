from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from textblob import TextBlob
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def generate_reply(sentiment, username):
    if sentiment == "Positive":
        return f"Thank you so much for your kind feedback, {username}! 😊"
    elif sentiment == "Neutral":
        return f"Thanks for your feedback, {username}. We'll continue to improve!"
    else:
        return f"We’re sorry to hear that, {username}. We’ll work to resolve this immediately. 🙏"

@app.route('/api/review', methods=['POST'])
def handle_review():
    data = request.json
    username = data.get('username')
    product_id = data.get('product_id')
    product_name = data.get('product_name')
    review = data.get('review')

    sentiment = get_sentiment(review)
    reply = generate_reply(sentiment, username)

    print(f"\n🔍 New Review Submitted:")
    print(f"User: {username}")
    print(f"Product: {product_name} ({product_id})")
    print(f"Review: {review}")
    print(f"Sentiment: {sentiment}")

    if sentiment == "Negative":
        print(f"\n⚠️ ADMIN ALERT: Negative review from {username} on {product_name}")

    return jsonify({
        "sentiment": sentiment,
        "reply": reply
    })

if __name__ == '__main__':
    app.run(debug=True)
