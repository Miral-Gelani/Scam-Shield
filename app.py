from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import datetime, uuid, re

app = Flask(__name__)
CORS(app)

# 1. Yeh naya route hai jo aapki website ka main page dikhayega
@app.route('/')
def home():
    return render_template('index.html')

KEYWORDS = {
    r"\burgent\b": "Urgency",
    r"\botp\b": "Financial Scam",
    r"\bbank\b": "Financial Scam",
    r"\bclick\b": "Phishing",
    r"\bverify\b": "Phishing",
    r"\btransfer\b": "Financial Scam",
    r"\bprize\b": "Lottery Scam",
    r"\baccount\b": "Phishing",
    r"\binvest\b": "Investment Scam",
    r"\bsextortion\b": "Sextortion",
    r"\bpassword\b": "Phishing"
}

def analyze(msg):
    msg_l = msg.lower()
    risky = []
    for pattern, category in KEYWORDS.items():
        if re.search(pattern, msg_l):
            risky.append(pattern.strip(r'\b'))
    score = min(100, len(risky) * 20 + 10)
    category = "Unknown"
    if risky:
        match_key = r"\b" + risky[0] + r"\b"
        category = KEYWORDS.get(match_key, "Unknown")
    
    status = "High Risk" if score > 70 else "Medium Risk" if score > 40 else "Low Risk"
    advice = [
        "Never share OTP, passwords, or banking credentials.",
        "Do not click unknown links or download attachments.",
        "Contact official support directly via verified channels.",
        "Report this message to cyber authorities like CERT-In.",
        "Enable two-factor authentication on your accounts."
    ]
    return {
        "case_id": str(uuid.uuid4())[:8],
        "time": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "risky_words": risky,
        "score": score,
        "category": category,
        "target": "General Public",
        "status": status,
        "explanation": "This message employs psychological manipulation, urgency tactics, and financial lures.",
        "advice": advice
    }

@app.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.json
        message = data.get("message", "").strip()
        if not message:
            return jsonify({"error": "No message provided"}), 400
        return jsonify(analyze(message))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000) # Render ke liye port 10000 behtar hai
