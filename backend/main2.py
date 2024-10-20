from flask import Flask, request, jsonify, render_template
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import re
import os

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("API_KEY")

# 環境変数にOpenAIのAPIキーを設定
os.environ["OPENAI_API_KEY"] = api_key

# PDFから教員情報を取得する関数


def load_documents(pdf_paths):
    documents = []
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
    return documents

# ドキュメントの前処理を行う関数


def preprocess_documents(documents):
    for i in range(len(documents)):
        # 不要なエスケープシーケンスを削除
        documents[i].page_content = re.sub(
            r"\u2003|\x0032|\uf128", "", documents[i].page_content)

        # 名前と読み仮名の間にスペースを挿入
        documents[i].page_content = re.sub(
            r'([ぁ-んァ-ヶ一-龥])([A-Z])', r'\1 \2', documents[i].page_content)

        # 役職と氏名の間にスペースを追加
        documents[i].page_content = re.sub(
            r'(教授|准教授|学長|副学長|コース長|情報アーキテクチャ学科⻑)([ぁ-んァ-ヶ一-龥])', r'\1 \2', documents[i].page_content)

        # 余分な改行コードとスペースを1つにまとめる
        documents[i].page_content = re.sub(
            r'\s+', ' ', documents[i].page_content)

        # メールアドレスの小文字のアルファベットを削除
        documents[i].page_content = re.sub(
            r'(\d{3}).([a-z_-]+)', r' 部屋番号:\1\n', documents[i].page_content)

        # 特定の不要な文字列パターンを削除
        documents[i].page_content = re.sub(
            r"([ぁ-ん]|[ぁ-ん] )(名前 name 室名メール \(@以降省略\))", "", documents[i].page_content)

    return documents

# メイン処理


def main():
    # 読み込むPDFファイルのパスをリストとして定義
    pdf_paths = [
        "2024professor.pdf",
        "campus_tour.pdf"
    ]

    # PDFからドキュメントを読み込む
    documents = load_documents(pdf_paths)
    documents = preprocess_documents(documents)
    print(documents)

    # テキストスプリッターを初期化
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # 埋め込みを初期化し、ベクターストアに文書と埋め込みを格納
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embeddings)
    retriever = db.as_retriever()

    # LLM ラッパーを読み込む
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # チェーンを作成
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, output_key="description_str")

    return qa_chain


# QAチェーンを初期化
qa_chain = main()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    # LangChainでユーザーのメッセージに応答
    response = qa_chain.run(user_input)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
