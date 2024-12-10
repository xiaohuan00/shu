from flask import Flask, render_template, request, jsonify, url_for
from main import XiaohongshuTitleGenerator

app = Flask(__name__, static_url_path='/static')
generator = XiaohongshuTitleGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get('user_id', 'default_user')
    message = request.json.get('message')
    context = request.json.get('context')
    
    response = generator.chat_with_ai(user_id, message, context)
    return jsonify({'response': response})

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    user_id = request.json.get('user_id', 'default_user')
    generator.clear_conversation(user_id)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 