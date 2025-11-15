from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/generate-message", methods=["POST"])
def generate_message():
    data = request.json

    records = data.get("records", [])
    format_settings = data.get("format", {})

    # If 'records' is a string (template variable like {{test}})
    if isinstance(records, str):
        try:
            records = json.loads(records)
        except:
            return jsonify({"error": "Invalid JSON in 'records' string"}), 400

    final_msg = "🧾 Invoice Details\n\n━━━━━━━━━━━━━━━━━━━\n\n"

    for inv in records:
        for item in format_settings:
            label = item.get("label", "")
            field = item.get("field", "")
            emoji = item.get("emoji", "")

            value = inv.get(field, "")

            if isinstance(value, list) and len(value) > 1:
                value = value[1]

            final_msg += f"{emoji} {label}: {value}\n\n"

        final_msg += "━━━━━━━━━━━━━━━━━━━\n\n"

    return jsonify({
        "message": final_msg.strip()
    })


if __name__ == "__main__":
    app.run(debug=True)
