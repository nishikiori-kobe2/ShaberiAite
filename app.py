import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv
import html

# .envファイルから環境変数を読み込む
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="喋り相手",
    page_icon="💬",
    layout="centered"
)

# カスタムCSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .ai-message {
        background: linear-gradient(135deg, #e0e7ff 0%, #cfd9ff 100%);
        color: #1e293b;
        margin-right: 20%;
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
    }
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# タイトル
st.title("💬 喋り相手")

# キャラクター定義
CHARACTERS = {
    "ゆうちゃみ": {
        "system_prompt": """あなたは「ゆうちゃみ」として会話してください。
ゆうちゃみは明るく元気でフレンドリーな性格です。
語尾に「〜だよ！」「〜なんだよね」など、親しみやすい言葉遣いをします。
若者らしいポジティブな雰囲気と、時々使う流行語やギャル語が特徴です。
絵文字を時々使い、明るく楽しい会話を心がけてください。""",
        "emoji": "🌟"
    },
    "高倉 健": {
        "system_prompt": """あなたは「高倉健」として会話してください。
高倉健は寡黙で渋く、男らしい日本の俳優です。
言葉少なく、簡潔で重みのある言葉を選びます。
「そうだな」「ああ」など、短い相槌や返答が多く、深い思慮を感じさせる語り口です。
義理人情を大切にし、古風で誠実な人柄を表現してください。""",
        "emoji": "🗡️"
    },
    "ボブ・ディラン": {
        "system_prompt": """あなたは「ボブ・ディラン」として会話してください。
ボブ・ディランは詩的で哲学的な表現を好む伝説のミュージシャンです。
比喩や詩的な言い回しを使い、深い洞察や人生の真理を語ります。
時に謎めいた表現や、風刺的なユーモアも交えます。
音楽、自由、人生について独自の視点で語り、芸術家らしい感性を表現してください。
日本語で会話しますが、時々英語のフレーズも織り交ぜることがあります。""",
        "emoji": "🎸"
    },
    "井上陽水": {
        "system_prompt": """あなたは「井上陽水」として会話してください。
井上陽水は独特の世界観を持つ日本のシンガーソングライターです。
不思議で幻想的、時にシュールな表現を好みます。
「傘がない」「夢の中へ」など、日常の中に非日常を見出す感性があります。
穏やかで優しい語り口ながら、独特のユーモアと詩的な表現が特徴です。
少し不思議で、でも心に響く言葉を紡いでください。""",
        "emoji": "🎵"
    }
}

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_character" not in st.session_state:
    st.session_state.selected_character = "ゆうちゃみ"

# キャラクター選択
col1, col2 = st.columns([3, 1])
with col1:
    selected_character = st.selectbox(
        "会話する相手を選んでください",
        options=list(CHARACTERS.keys()),
        index=list(CHARACTERS.keys()).index(st.session_state.selected_character),
        key="character_selector"
    )

with col2:
    st.markdown(f"<div style='text-align: center; font-size: 1.5rem; margin-top: 0.5rem;'>{CHARACTERS[selected_character]['emoji']}</div>", unsafe_allow_html=True)

# キャラクター変更時の処理
if selected_character != st.session_state.selected_character:
    st.session_state.selected_character = selected_character
    st.session_state.messages = []
    st.rerun()

# スペース追加
st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

# 会話履歴のクリアボタン
if st.button("🔄 会話をリセット", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# 会話履歴の表示
st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        # HTMLエスケープして安全に表示
        escaped_content = html.escape(message["content"]).replace('\n', '<br>')
        
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <b>👤 あなた</b>
                    <p>{escaped_content}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # キャラクター名を取得（メッセージに保存されている場合はそれを使用）
            char_name = message.get("character", selected_character)
            char_emoji = CHARACTERS.get(char_name, {}).get("emoji", "🤖")
            st.markdown(f"""
                <div class="chat-message ai-message">
                    <b>{char_emoji} {char_name}</b>
                    <p>{escaped_content}</p>
                </div>
                """, unsafe_allow_html=True)

# ユーザー入力フォーム
st.markdown("---")
st.markdown("##### 💭 メッセージを送る")
st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

with st.form(key="message_form", clear_on_submit=True):
    user_input = st.text_area(
        "メッセージを入力してください",
        placeholder="ここにメッセージを入力...",
        height=100,
        key="user_input_text"
    )
    submit_button = st.form_submit_button("→", use_container_width=True)

if submit_button and user_input:
    # APIキーの確認
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEYが設定されていません。環境変数を設定してください。")
        st.stop()
    
    # ユーザーメッセージを追加
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # LangChainでGeminiモデルを使用
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=api_key,
            temperature=0.9,
            max_tokens=2000  # トークン数を増やす
        )
        
        # メッセージの構築（最新のメッセージのみを使用）
        messages = [
            SystemMessage(content=CHARACTERS[selected_character]["system_prompt"])
        ]
        
        # 直近の会話履歴を追加（最大10往復分）
        recent_messages = st.session_state.messages[-20:] if len(st.session_state.messages) > 20 else st.session_state.messages
        for msg in recent_messages:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # AIの応答を取得
        with st.spinner(f"{selected_character}が考えています..."):
            response = llm.invoke(messages)
            ai_message = response.content
        
        # 空の応答チェック
        if not ai_message or ai_message.strip() == "":
            ai_message = "すみません、うまく返答できませんでした。もう一度お願いします。"
            st.warning("⚠️ AIからの応答が空でした。")
        
        # AIメッセージを追加（キャラクター名も保存）
        st.session_state.messages.append({
            "role": "assistant", 
            "content": ai_message,
            "character": selected_character
        })
        
        # 画面を更新
        st.rerun()
        
    except Exception as e:
        # エラーが発生した場合、追加したユーザーメッセージを削除
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            st.session_state.messages.pop()
        
        # エラーメッセージを表示
        st.error(f"❌ エラーが発生しました: {str(e)}")
        st.info("💡 ヒント: モデル名やAPIキーを確認してください。")

# フッター
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>💬 喋り相手 - AI キャラクターチャットアプリ</p>
        <p style='font-size: 0.8rem;'>Powered by Gemini 2.5 Pro & LangChain</p>
    </div>
    """, unsafe_allow_html=True)

