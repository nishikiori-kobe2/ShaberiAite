# 💬 喋り相手 - AI キャラクターチャットアプリ

4人の個性豊かなキャラクターとチャットできるAIアプリケーションです。

## ✨ 特徴

- **4人のキャラクター**から選んで会話
  - 🌟 ゆうちゃみ - 明るく元気なギャル系
  - 🎭 高倉 健 - 寡黙で渋い男らしさ
  - 🎸 ボブ・ディラン - 詩的で哲学的なミュージシャン
  - 🎵 井上陽水 - 不思議で幻想的なシンガーソングライター

- **最新AI技術**: Google Gemini 2.5 Pro を使用
- **モダンUI**: Streamlit による美しいインターフェース
- **自然な会話**: LangChain で文脈を理解した応答

## 🚀 セットアップ

### 1. リポジトリのクローン

```bash
git clone <your-repository-url>
cd ShaberiAite
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成:

```bash
cp .env.example .env
```

`.env` ファイルを編集して、Google AI APIキーを設定:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

#### APIキーの取得方法:
1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリック
4. 生成されたAPIキーをコピーして `.env` に貼り付け

### 4. アプリケーションの起動

```bash
streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501` でアプリが起動します。

## 📦 Renderへのデプロイ

### 1. GitHubリポジトリにプッシュ

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Renderでデプロイ

1. [Render](https://render.com/) にログイン
2. 「New +」→「Web Service」を選択
3. GitHubリポジトリを接続
4. 以下の設定を入力:
   - **Name**: `shaberi-aite` (任意の名前)
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. 「Environment Variables」セクションで環境変数を追加:
   - Key: `GOOGLE_API_KEY`
   - Value: あなたのGoogle AI APIキー
6. 「Create Web Service」をクリック

デプロイが完了すると、URLが発行されてアプリにアクセスできます。

## 🛠️ 技術スタック

- **フロントエンド**: Streamlit
- **言語**: Python 3.9+
- **AIフレームワーク**: LangChain
- **AIモデル**: Google Gemini 2.5 Pro
- **デプロイ**: Render

## 📝 使い方

1. ドロップダウンリストから会話したいキャラクターを選択
2. テキスト入力欄にメッセージを入力
3. キャラクターが個性的な返答をします
4. 「🔄 会話をリセット」ボタンで会話履歴をクリア

## 🤝 貢献

プルリクエストを歓迎します！大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## 📄 ライセンス

MIT License

## 💡 今後の拡張アイデア

- [ ] さらに多くのキャラクターを追加
- [ ] 会話履歴の保存機能
- [ ] 音声入力/出力
- [ ] マルチモーダル対応（画像の共有）
- [ ] ユーザー認証

---

Made with ❤️ using Streamlit, LangChain, and Gemini AI

