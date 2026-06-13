"""
紧固件AI问答 Web应用 - Flask后端
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from qa_engine import qa_system

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    """首页"""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """问答接口"""
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "请输入您的问题。", "suggestions": qa_system.get_suggestions()})

    answer = qa_system.ask(question)
    return jsonify({"answer": answer, "suggestions": qa_system.get_suggestions()})


@app.route("/api/welcome", methods=["GET"])
def welcome():
    """欢迎信息"""
    return jsonify({"answer": qa_system.get_welcome(), "suggestions": qa_system.get_suggestions()})


@app.route("/api/clear", methods=["POST"])
def clear():
    """清除对话"""
    msg = qa_system.clear_history()
    return jsonify({"answer": msg, "suggestions": qa_system.get_suggestions()})


if __name__ == "__main__":
    print("=" * 50)
    print("  紧固件AI知识问答系统")
    print("  访问地址: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host="127.0.0.1", port=5000, debug=True)
