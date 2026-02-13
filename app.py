from flask import Flask, request, jsonify, render_template
import json
import os
app = Flask(__name__)
MEMORY_FILE = "memory.json"
# 初始化记忆文件
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)
def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    memory = load_memory()

    # 记录当前输入
    memory.append({"user": user_input})
    save_memory(memory)

    # 取最近3条历史
    recent_memory = memory[-3:]

    response = "You have told me before:\n"
    for item in recent_memory:
        response += "- " + item["user"] + "\n"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
