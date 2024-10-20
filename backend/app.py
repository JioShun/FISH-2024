from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from main2 import qa_chain

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/api/process', methods=['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE'])
def process_input():
    if request.method == 'OPTIONS':

        
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization'
        return response

    if request.method == 'POST':
        data = request.json  # フロントエンドからのJSONデータを取得
        user_input = data.get('input')
        response_message = qa_chain.run(user_input)

        response = jsonify({'message': f'{response_message}'})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # 他のリクエストメソッド (GETなど) に対しても、CORSヘッダーを含めたレスポンスを返す
    response = make_response("ok")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
