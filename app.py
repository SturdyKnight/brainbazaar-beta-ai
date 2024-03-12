from flask import Flask, render_template, send_from_directory, request as req
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route('/static/favicon.ico')
def static_files():
    return send_from_directory('static', 'favicon.ico')

@app.route('/static/logo.png')
def serve_logo():
    return send_from_directory('static', 'logo.png')

@app.route("/Summarize", methods=["POST"])
def Summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer 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"}
        data = req.form["data"]
        
        try:
            maxL = int(req.form["maxL"])
        except KeyError:
            maxL = 512  # Default value if maxL is not provided

        minL = maxL // 4

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })

        if output:
            summary_text = output[0]["summary_text"]
        else:
            summary_text = "No summary available"

        return render_template("index.html", result=summary_text)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
