import base64
import hashlib
import html
import os
import random
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st


st.set_page_config(
    page_title="ISLAND MATCH｜島時間診断",
    page_icon="◌",
    layout="wide",
    initial_sidebar_state="collapsed",
)


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

:root {
  --paper: #f3f0e7;
  --paper-2: #ebe6d8;
  --ink: #20352c;
  --muted: #6e786f;
  --coral: #d96e55;
  --sage: #708d78;
  --line: rgba(32, 53, 44, .18);
}

html, body, [class*="css"] {
  font-family: "DM Sans", "Noto Sans JP", sans-serif;
}

.stApp {
  background:
    linear-gradient(rgba(32,53,44,.035) 1px, transparent 1px),
    var(--paper);
  background-size: 100% 44px;
  color: var(--ink);
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { right: 1.2rem; }
[data-testid="stMainBlockContainer"] {
  max-width: 1180px;
  padding-top: 2.4rem;
  padding-bottom: 5rem;
}

.masthead {
  border-top: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  padding: 17px 0 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  letter-spacing: .16em;
  font-size: 11px;
  text-transform: uppercase;
}

.issue {
  color: var(--coral);
  font-weight: 700;
}

.hero {
  padding: 54px 0 42px;
  display: grid;
  grid-template-columns: 1.25fr .75fr;
  gap: 40px;
  align-items: end;
}

.eyebrow {
  color: var(--coral);
  letter-spacing: .2em;
  text-transform: uppercase;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 18px;
}

.hero h1 {
  font-family: "Playfair Display", "Noto Sans JP", serif;
  font-size: clamp(48px, 7vw, 88px);
  line-height: .98;
  letter-spacing: -.04em;
  margin: 0;
  color: var(--ink);
}

.hero-copy {
  border-left: 1px solid var(--ink);
  padding-left: 24px;
  color: var(--muted);
  font-size: 14px;
  line-height: 2;
}

.section-label {
  display: inline-block;
  border-bottom: 2px solid var(--coral);
  padding-bottom: 5px;
  margin: 8px 0 22px;
  letter-spacing: .16em;
  text-transform: uppercase;
  font-size: 11px;
  font-weight: 700;
}

.question-note {
  color: var(--muted);
  font-size: 13px;
  margin: -10px 0 24px;
}

.result-shell {
  border: 1px solid var(--ink);
  background: rgba(248,246,239,.82);
  padding: clamp(24px, 5vw, 54px);
  margin-top: 20px;
  position: relative;
  box-shadow: 10px 10px 0 var(--paper-2);
}

.result-no {
  font-size: 11px;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--coral);
  font-weight: 700;
}

.result-shell h2 {
  font-family: "Playfair Display", "Noto Sans JP", serif;
  font-size: clamp(36px, 5vw, 62px);
  line-height: 1.08;
  margin: 14px 0 16px;
  letter-spacing: -.03em;
}

.result-shell .lead {
  max-width: 720px;
  color: var(--muted);
  line-height: 1.9;
  font-size: 15px;
}

.quote {
  border-top: 1px solid var(--line);
  margin-top: 28px;
  padding-top: 20px;
  font-family: "Playfair Display", "Noto Sans JP", serif;
  font-size: 20px;
  font-style: italic;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border-top: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
  margin: 28px 0 10px;
}

.meta-item {
  padding: 16px 14px;
  border-right: 1px solid var(--line);
}
.meta-item:last-child { border-right: 0; }
.meta-item span {
  display: block;
  color: var(--muted);
  font-size: 10px;
  letter-spacing: .14em;
  text-transform: uppercase;
  margin-bottom: 5px;
}
.meta-item strong { font-size: 14px; font-weight: 600; }

.api-card {
  border-top: 1px solid var(--ink);
  padding-top: 18px;
  margin-top: 22px;
}

.connection-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin: 14px 0 12px;
}

.connection-card {
  background: rgba(255,255,255,.52);
  border: 1px solid rgba(32,53,44,.15);
  padding: 12px 14px;
  min-height: 72px;
}

.connection-card span {
  display: block;
  color: var(--muted);
  font-size: 9px;
  letter-spacing: .13em;
  text-transform: uppercase;
  margin-bottom: 5px;
}

.connection-card strong {
  display: block;
  font-size: 13px;
  font-weight: 600;
}

.connection-card.ok { border-left: 4px solid #5f9271; }
.connection-card.wait { border-left: 4px solid #d5a93a; }
.connection-card.off { border-left: 4px solid #a5aaa3; }
.connection-card.error { border-left: 4px solid #c56f61; }

.api-tag {
  display: inline-block;
  background: var(--ink);
  color: var(--paper);
  padding: 5px 9px;
  font-size: 9px;
  letter-spacing: .15em;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.villager-name {
  font-family: "Playfair Display", "Noto Sans JP", serif;
  font-size: 34px;
  line-height: 1.1;
  margin: 5px 0 9px;
}

.letter {
  background: #faf8f1;
  border: 1px solid var(--line);
  box-shadow: 9px 9px 0 var(--paper-2);
  padding: clamp(26px, 5vw, 56px);
  line-height: 2.1;
  font-size: 15px;
  min-height: 340px;
}

.letter-date {
  font-size: 10px;
  letter-spacing: .15em;
  color: var(--muted);
  text-transform: uppercase;
  margin-bottom: 28px;
}

.data-note {
  font-size: 11px;
  color: var(--muted);
  line-height: 1.8;
}

.footer-line {
  margin-top: 55px;
  border-top: 1px solid var(--ink);
  padding-top: 14px;
  display: flex;
  justify-content: space-between;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: var(--muted);
}

div[data-testid="stForm"] {
  background: rgba(248,246,239,.76);
  border: 1px solid var(--line);
  padding: 22px 26px 26px;
}

/* Streamlitの更新で内部DOMが変わっても、ラジオ項目を確実に表示する */
div[data-testid="stRadio"] > label {
  color: var(--ink) !important;
  font-weight: 700 !important;
  opacity: 1 !important;
  visibility: visible !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
}

div[data-testid="stRadio"] label[data-baseweb="radio"] {
  display: flex !important;
  opacity: 1 !important;
  visibility: visible !important;
  background: rgba(255,255,255,.48);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 8px 12px;
  transition: .18s ease;
}

div[data-testid="stRadio"] label[data-baseweb="radio"] p {
  color: var(--ink) !important;
  opacity: 1 !important;
  visibility: visible !important;
}

.stButton > button, .stFormSubmitButton > button {
  border: 1px solid var(--ink) !important;
  border-radius: 0 !important;
  background: var(--ink) !important;
  color: var(--paper) !important;
  font-weight: 600 !important;
  letter-spacing: .08em;
  min-height: 48px;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  background: var(--coral) !important;
  border-color: var(--coral) !important;
  color: white !important;
}

[data-baseweb="tab-list"] {
  gap: 28px;
  border-bottom: 1px solid var(--line);
}
[data-baseweb="tab"] {
  height: 54px;
  padding-left: 0;
  padding-right: 0;
  letter-spacing: .08em;
}

div[data-testid="stExpander"] {
  border: 1px solid var(--line);
  border-radius: 0;
  background: rgba(255,255,255,.35);
}

@media (max-width: 760px) {
  .hero { grid-template-columns: 1fr; padding: 38px 0 28px; }
  .hero-copy { border-left: 0; border-top: 1px solid var(--ink); padding: 18px 0 0; }
  .meta-grid { grid-template-columns: 1fr; }
  .meta-item { border-right: 0; border-bottom: 1px solid var(--line); }
  .meta-item:last-child { border-bottom: 0; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

ISLAND_THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700;800&family=Zen+Maru+Gothic:wght@400;500;700&display=swap');

:root {
  --paper: #fff9e7;
  --paper-2: #f4e6b8;
  --ink: #315b45;
  --muted: #66796d;
  --coral: #f27f64;
  --sage: #79ad72;
  --sky: #a9dfe8;
  --sun: #f5cf66;
  --line: rgba(49, 91, 69, .18);
}

html, body, [class*="css"] {
  font-family: "Nunito", "Zen Maru Gothic", sans-serif;
}

.stApp {
  background-color: #fff9e7;
  background-image:
    radial-gradient(circle at 20px 20px, rgba(121,173,114,.10) 2px, transparent 2.5px),
    radial-gradient(circle at 60px 65px, rgba(169,223,232,.14) 3px, transparent 3.5px);
  background-size: 90px 90px;
  color: var(--ink);
}

[data-testid="stMainBlockContainer"] {
  max-width: 1160px;
  padding-top: 1.4rem;
}

.masthead {
  border: 0;
  border-radius: 999px;
  padding: 12px 20px;
  background: var(--ink);
  color: #fffdf3;
  box-shadow: 0 6px 0 rgba(49,91,69,.13);
}
.issue { color: var(--sun); }

.hero {
  min-height: 480px;
  margin: 24px 0 34px;
  padding: clamp(30px, 6vw, 70px);
  grid-template-columns: minmax(0, .88fr) minmax(250px, .52fr);
  align-items: center;
  border: 5px solid #fffdf3;
  border-radius: 42px;
  background-size: cover;
  background-position: center;
  box-shadow:
    0 20px 50px rgba(54,93,73,.18),
    0 0 0 1px rgba(49,91,69,.10);
  overflow: hidden;
}

.eyebrow {
  display: inline-block;
  color: #fffdf3;
  background: var(--coral);
  padding: 7px 13px;
  border-radius: 999px;
  letter-spacing: .12em;
  margin-bottom: 16px;
  box-shadow: 0 4px 0 rgba(159,75,56,.18);
}

.hero h1 {
  font-family: "Zen Maru Gothic", sans-serif;
  font-size: clamp(46px, 6.6vw, 78px);
  font-weight: 700;
  line-height: 1.14;
  letter-spacing: -.05em;
  color: var(--ink);
  text-shadow: 0 3px 0 rgba(255,255,255,.85);
}

.hero-copy {
  border: 0;
  border-radius: 26px;
  background: rgba(255,253,243,.90);
  padding: 22px 24px;
  color: var(--ink);
  font-size: 14px;
  line-height: 2;
  box-shadow: 0 8px 20px rgba(49,91,69,.12);
  backdrop-filter: blur(6px);
}

.section-label {
  border: 0;
  border-radius: 999px;
  padding: 8px 15px;
  margin-top: 16px;
  background: #ddefd5;
  color: var(--ink);
  letter-spacing: .12em;
}

.question-note {
  margin-top: -8px;
  padding-left: 6px;
}

div[data-testid="stForm"] {
  background: rgba(255,253,243,.94);
  border: 3px solid #b9dbaf;
  border-radius: 32px;
  padding: 28px 30px 32px;
  box-shadow: 0 12px 0 #e2dca7;
}

div[data-testid="stRadio"] label[data-baseweb="radio"] {
  background: #fffdf5;
  border: 2px solid #dbe8d5;
  border-radius: 16px;
  padding: 9px 13px;
  color: var(--ink) !important;
}

div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
  border-color: var(--sage);
  background: #eff8e9;
}

div[data-testid="stRadio"] label[data-baseweb="radio"] p {
  color: var(--ink) !important;
}

.stButton > button, .stFormSubmitButton > button {
  border: 0 !important;
  border-radius: 18px !important;
  background: var(--coral) !important;
  box-shadow: 0 6px 0 #c75e49;
  font-weight: 800 !important;
  min-height: 52px;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  transform: translateY(2px);
  box-shadow: 0 4px 0 #c75e49;
  background: #ef765a !important;
}

[data-baseweb="tab-list"] {
  gap: 8px;
  padding: 6px;
  border: 2px solid #dbe8d5;
  border-radius: 999px;
  background: rgba(255,253,243,.86);
}
[data-baseweb="tab"] {
  height: 46px;
  padding: 0 22px;
  border-radius: 999px;
}

div[data-testid="stExpander"] {
  border: 2px solid #c5e3e8;
  border-radius: 22px;
  background: rgba(235,249,250,.84);
}

.result-shell {
  border: 4px solid #b9dbaf;
  border-radius: 34px;
  background: #fffdf3;
  box-shadow: 11px 11px 0 var(--sun);
  overflow: hidden;
}

.result-no {
  display: inline-block;
  background: var(--sky);
  color: var(--ink);
  border-radius: 999px;
  padding: 7px 13px;
}

.result-shell h2, .villager-name {
  font-family: "Zen Maru Gothic", sans-serif;
  font-weight: 700;
}

.quote {
  font-family: "Zen Maru Gothic", sans-serif;
  color: #578352;
}

.meta-grid {
  gap: 10px;
  border: 0;
}
.meta-item {
  border: 2px solid #dbe8d5;
  border-radius: 18px;
  background: #f5faef;
}
.meta-item:last-child { border-right: 2px solid #dbe8d5; }

.api-card {
  border: 0;
  border-radius: 22px;
  background: #eef8e9;
  padding: 18px;
}
.api-tag {
  border-radius: 999px;
  background: var(--sage);
}

.letter {
  border: 3px solid #b9dbaf;
  border-radius: 28px;
  background:
    linear-gradient(transparent 31px, rgba(89,130,91,.10) 32px),
    #fffdf5;
  background-size: 100% 32px;
  box-shadow: 10px 10px 0 #e2dca7;
}

.footer-line {
  border-top: 3px dotted #9fc395;
}

@media (max-width: 760px) {
  .masthead { border-radius: 20px; gap: 12px; font-size: 9px; }
  .hero {
    min-height: 560px;
    grid-template-columns: 1fr;
    align-content: start;
    padding: 32px 24px;
    background-position: 63% center;
  }
  .hero-copy { margin-top: 205px; }
  [data-baseweb="tab"] { padding: 0 13px; }
}
</style>
"""
st.markdown(ISLAND_THEME, unsafe_allow_html=True)


ARCHETYPES = {
    "coast": {
        "edition": "01 / OPEN COAST",
        "title": "あつまれ どうぶつの森",
        "jp": "余白をつくる、島の編集者",
        "description": "決められた正解より、自分の手で景色を編集したい人。広い余白と自由な選択肢があるほど、あなたの感性はよく働きます。",
        "quote": "好きな景色は、待つものではなくつくるもの。",
        "character": "しずえ",
        "item": "使い込んだスケッチブック",
        "time": "夕暮れ前",
        "personality": "normal",
        "color": "#d96e55",
    },
    "town": {
        "edition": "02 / TOWN STORIES",
        "title": "とびだせ どうぶつの森",
        "jp": "関係を育てる、小さな町長",
        "description": "自分だけの完成より、誰かと少しずつ町を育てる時間を大切にする人。会話の積み重ねがあなたの世界を豊かにします。",
        "quote": "いい町は、いい会話からできていく。",
        "character": "しずえ",
        "item": "小さな予定帳",
        "time": "午前10時",
        "personality": "peppy",
        "color": "#708d78",
    },
    "memory": {
        "edition": "03 / SMALL DAYS",
        "title": "おいでよ どうぶつの森",
        "jp": "日常を集める、記憶の人",
        "description": "大きなイベントより、何気ない一日の手触りを覚えている人。懐かしさを弱さではなく、感性として持っています。",
        "quote": "何でもない日ほど、あとから特別になる。",
        "character": "とたけけ",
        "item": "古い音楽プレイヤー",
        "time": "放課後",
        "personality": "lazy",
        "color": "#b58a63",
    },
    "city": {
        "edition": "04 / MIDNIGHT CITY",
        "title": "街へいこうよ どうぶつの森",
        "jp": "気分で動く、夜の散歩人",
        "description": "予定を詰めるより、その日の気分で寄り道を選びたい人。少しにぎやかな場所のほうが、むしろ自分に戻れます。",
        "quote": "遠回りの途中に、今日の目的が見つかる。",
        "character": "フータ",
        "item": "夜行バスの切符",
        "time": "午後9時",
        "personality": "cranky",
        "color": "#55707b",
    },
    "home": {
        "edition": "05 / PRIVATE ROOM",
        "title": "ハッピーホームデザイナー",
        "jp": "好きで整える、空間の作家",
        "description": "ものの配置や色の組み合わせに、その人らしさを見つける人。あなたにとって部屋は、いちばん正直な自己紹介です。",
        "quote": "居心地は、細部に宿る。",
        "character": "タクミ",
        "item": "色見本のカード",
        "time": "深夜0時",
        "personality": "snooty",
        "color": "#8d7085",
    },
    "pocket": {
        "edition": "06 / POCKET CLUB",
        "title": "どうぶつの森 ポケットキャンプ",
        "jp": "小さく楽しむ、収集の名人",
        "description": "短い時間でも、自分の好きなものを見つけるのが上手な人。かわいさや季節感を軽やかに取り入れるセンスがあります。",
        "quote": "好きなものは、少しずつ集めればいい。",
        "character": "リサ",
        "item": "ポケットサイズのカメラ",
        "time": "昼休み",
        "personality": "smug",
        "color": "#ba7f6d",
    },
}

FALLBACK_VILLAGERS = {
    "normal": {"name": "ドレミ", "species": "シカ", "personality": "ふつう", "phrase": "静かな時間を一緒に楽しめそう"},
    "peppy": {"name": "ブーケ", "species": "ネコ", "personality": "元気", "phrase": "町の空気を明るくしてくれそう"},
    "lazy": {"name": "パッチ", "species": "コグマ", "personality": "ぼんやり", "phrase": "何でもない午後が似合いそう"},
    "cranky": {"name": "アポロ", "species": "ワシ", "personality": "コワイ", "phrase": "夜の散歩で本音を話せそう"},
    "snooty": {"name": "ビアンカ", "species": "オオカミ", "personality": "オトナ", "phrase": "空間づくりの相談相手になりそう"},
    "smug": {"name": "ジュン", "species": "リス", "personality": "キザ", "phrase": "新しい流行を教えてくれそう"},
}


def secret_value(name: str) -> str:
    try:
        return str(st.secrets.get(name, ""))
    except Exception:
        return ""


def score_answers(answers: dict) -> dict:
    scores = {key: 0 for key in ARCHETYPES}
    maps = {
        "pace": {
            "じっくり、自分のペース": {"coast": 3, "home": 1},
            "誰かと相談しながら": {"town": 3, "pocket": 1},
            "その日の気分で": {"city": 3, "memory": 1},
        },
        "favorite": {
            "景色をつくる": {"coast": 3},
            "住民と話す": {"town": 3},
            "思い出を集める": {"memory": 3},
            "家具を整える": {"home": 3},
            "限定アイテムを集める": {"pocket": 3},
            "目的なく歩く": {"city": 3},
        },
        "mood": {
            "朝の海辺": {"coast": 2, "town": 1},
            "雨上がりの商店街": {"city": 2, "town": 1},
            "夕方の自室": {"home": 2, "memory": 1},
            "深夜の広場": {"memory": 2, "city": 1},
            "季節のイベント": {"pocket": 3},
        },
        "weekend": {
            "予定を決めずに過ごす": {"coast": 2, "city": 1},
            "友達と会う": {"town": 2, "pocket": 1},
            "写真や日記を整理する": {"memory": 3},
            "部屋の模様替え": {"home": 3},
        },
        "season": {
            "春": {"pocket": 2, "town": 1},
            "夏": {"coast": 2, "city": 1},
            "秋": {"memory": 2, "home": 1},
            "冬": {"city": 2, "home": 1},
        },
    }
    for question, answer in answers.items():
        for key, points in maps[question][answer].items():
            scores[key] += points
    return scores


def choose_result(scores: dict, nickname: str) -> str:
    top_score = max(scores.values())
    candidates = sorted(key for key, value in scores.items() if value == top_score)
    seed = hashlib.sha256((nickname or "islander").encode("utf-8")).hexdigest()
    return candidates[int(seed[:8], 16) % len(candidates)]


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_villager(api_key: str, personality: str, seed_text: str) -> tuple[dict, str]:
    fallback = FALLBACK_VILLAGERS[personality].copy()
    if not api_key:
        return fallback, "curated"
    try:
        response = requests.get(
            "https://api.nookipedia.com/villagers",
            headers={"X-API-KEY": api_key, "Accept-Version": "1.0.0"},
            params={"game": "NH", "personality": personality, "thumbsize": 360},
            timeout=10,
        )
        response.raise_for_status()
        villagers = response.json()
        if not villagers:
            return fallback, "curated"
        index = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:8], 16) % len(villagers)
        raw = villagers[index]
        return {
            "name": raw.get("name", fallback["name"]),
            "species": raw.get("species", fallback["species"]),
            "personality": raw.get("personality", fallback["personality"]),
            "phrase": raw.get("quote") or raw.get("catchphrase") or fallback["phrase"],
            "image_url": raw.get("image_url") or raw.get("render_url"),
            "url": raw.get("url"),
        }, "nookipedia"
    except Exception:
        return fallback, "curated"


def check_nookipedia(api_key: str) -> tuple[bool, str]:
    if not api_key:
        return False, "キー未入力"
    try:
        response = requests.get(
            "https://api.nookipedia.com/villagers",
            headers={"X-API-KEY": api_key, "Accept-Version": "1.0.0"},
            params={"game": "NH", "thumbsize": 24},
            timeout=10,
        )
        response.raise_for_status()
        return True, "接続済み"
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else ""
        return False, f"接続できません（{status_code}）"
    except requests.RequestException:
        return False, "通信エラー"


def check_gemini(api_key: str) -> tuple[bool, str]:
    if not api_key:
        return False, "キー未入力"
    try:
        response = requests.get(
            "https://generativelanguage.googleapis.com/v1beta/models",
            headers={"x-goog-api-key": api_key},
            timeout=10,
        )
        response.raise_for_status()
        return True, "接続済み"
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else ""
        return False, f"接続できません（{status_code}）"
    except requests.RequestException:
        return False, "通信エラー"


def local_wish_reply(wish: str) -> str:
    wish_text = (wish or "").strip()
    if not wish_text:
        return "まだ願いが言葉になっていなくても大丈夫。気になる方向へ、今日はほんの少しだけ歩いてみてください。"

    if any(word in wish_text for word in ["旅行", "海外", "旅", "留学"]):
        return "まずは行きたい場所をひとつ決めて、写真を眺めたり費用を調べたりするところから。旅は予約する前から、もう始まっています。"
    if any(word in wish_text for word in ["勉強", "資格", "試験", "学び", "語学"]):
        return "今日は教材を開くところまででも十分です。短い時間を重ねるほうが、無理な計画より遠くまで連れていってくれます。"
    if any(word in wish_text for word in ["始め", "挑戦", "新しい"]):
        return "最初から上手にやろうとせず、五分で終わる最初の一歩を決めてみてください。始めたという事実が、次の景色をつくります。"
    if any(word in wish_text for word in ["仕事", "就職", "転職", "将来"]):
        return "答えを一度に決めなくても大丈夫。気になる選択肢をひとつ書き出し、明日の自分が動きやすい形にしておきましょう。"
    if any(word in wish_text for word in ["恋", "好きな人", "友達", "仲直り", "人間関係"]):
        return "相手の答えを急いで想像するより、まずは自分の気持ちを短い言葉にしてみてください。やさしい一言から関係は動きます。"
    if any(word in wish_text for word in ["不安", "怖い", "迷", "疲れ", "つらい"]):
        return "すぐに元気になろうとしなくて大丈夫です。いま一番負担の小さいことを選び、今日はそこまでを一区切りにしましょう。"
    return "その願いを、今日できる小さな行動にひとつだけ言い換えてみてください。小さくても、自分で選んだ一歩なら十分です。"


def generate_letter(api_key: str, profile: dict, nickname: str, wish: str) -> tuple[str, str]:
    wish_text = (wish or "").strip()
    wish_intro = (
        f"「{wish_text}」という気持ち、ちゃんと島まで届いています。"
        if wish_text
        else "まだ言葉になっていない気持ちも、ちゃんと島まで届いています。"
    )
    wish_reply = local_wish_reply(wish_text)
    fallback = (
        f"{nickname or 'あなた'}さんへ\n\n"
        f"{wish_intro}\n"
        f"{wish_reply}\n\n"
        f"あなたに似合うのは「{profile['jp']}」という過ごし方。"
        f"夕方になったら、{profile['item']}を持って少しだけ散歩を。"
        f"{profile['quote']}\n\n"
        "また島で会いましょう。"
    )
    if not api_key:
        return fallback, "template"
    prompt = f"""
あなたは、静かで気の利く島の案内人です。
次の診断結果をもとに、日本語で短い「島からの手紙」を書いてください。
どうぶつの森の固有キャラクターになりきらず、公式作品の文章を引用しないでください。
説教せず、甘すぎず、120〜180字。改行を2〜3回入れてください。
完成した手紙だけを返してください。「改行1」などの制作指示や説明は書かないでください。
「今かなえたいこと」の意味を読み取り、その内容に直接返事をしてください。
入力文を不自然に接続したり、そのまま繰り返したりせず、内容に合う具体的な小さな一歩をひとつ提案してください。

名前: {nickname or 'あなた'}
タイプ: {profile['jp']}
特徴: {profile['description']}
今かなえたいこと: {wish or 'まだ決めていない'}
キーワード: {profile['item']} / {profile['time']}
"""
    try:
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent",
            headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.8, "maxOutputTokens": 320},
            },
            timeout=12,
        )
        response.raise_for_status()
        parts = response.json()["candidates"][0]["content"]["parts"]
        text = "\n".join(
            part.get("text", "").strip()
            for part in parts
            if part.get("text") and not part.get("thought", False)
        ).strip()
        text = text.replace("```text", "").replace("```", "").strip()
        if len(text) < 70:
            return fallback, "template"
        return text, "gemini"
    except Exception:
        return fallback, "template"


def score_chart(scores: dict, highlight: str) -> go.Figure:
    labels = [ARCHETYPES[key]["edition"].split(" / ")[1] for key in ARCHETYPES]
    values = [scores[key] for key in ARCHETYPES]
    colors = [ARCHETYPES[highlight]["color"] if key == highlight else "#c8c8bc" for key in ARCHETYPES]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=colors,
            hovertemplate="%{y}<br>score %{x}<extra></extra>",
        )
    )
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#20352c", size=11),
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(title="", autorange="reversed", fixedrange=True),
        showlegend=False,
    )
    return fig


def safe(value: str) -> str:
    return html.escape(str(value or ""))


@st.cache_data(show_spinner=False)
def hero_image_uri() -> str:
    image_path = Path(__file__).with_name("island_hero.png")
    if not image_path.exists():
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


if "match" not in st.session_state:
    st.session_state.match = None
if "letter" not in st.session_state:
    st.session_state.letter = None
if "api_checks" not in st.session_state:
    st.session_state.api_checks = {"nookipedia": None, "gemini": None}
if "api_key_fingerprints" not in st.session_state:
    st.session_state.api_key_fingerprints = {"nookipedia": "", "gemini": ""}

hero_uri = hero_image_uri()
hero_background = (
    "linear-gradient(90deg, rgba(255,249,231,.97) 0%, rgba(255,249,231,.84) 35%, "
    "rgba(255,249,231,.10) 72%), "
    f"url('{hero_uri}')"
    if hero_uri
    else "linear-gradient(135deg, #fff4c8, #bfe8e4)"
)

st.markdown(
    f"""
    <div class="masthead">
      <span>ISLAND LETTER · PERSONAL MATCH</span>
      <span class="issue">MINAMI'S ISLAND · 2026</span>
    </div>
    <section class="hero" style="background-image:{hero_background};">
      <div>
        <div class="eyebrow">Welcome to a softer day</div>
        <h1>あなたらしい<br>島暮らし。</h1>
      </div>
      <div class="hero-copy">
        木の葉が揺れる音、海辺の小道、住民との短い会話。<br>
        5つの選択から、あなたに似合うシリーズと<br>
        島で出会いたい相棒を見つけよう。
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

server_nook_key = os.getenv("NOOKIPEDIA_API_KEY", "") or secret_value("NOOKIPEDIA_API_KEY")
server_gemini_key = os.getenv("GEMINI_API_KEY", "") or secret_value("GEMINI_API_KEY")

with st.expander("API CONNECTION　—　必要なときだけ開く"):
    st.caption("公開設定のキーは画面へ送信しません。未設定の場合だけ、一時入力できます。")
    api_col1, api_col2 = st.columns(2)
    with api_col1:
        if server_nook_key:
            st.markdown("**Nookipedia API**")
            st.caption("管理者のSecretsで設定済み")
            nook_key = server_nook_key
        else:
            nook_key = st.text_input(
                "Nookipedia API Key",
                type="password",
                help="実在する住民候補の取得に使います。この画面を閉じると消えます。",
            )
    with api_col2:
        if server_gemini_key:
            st.markdown("**Gemini API**")
            st.caption("管理者のSecretsで設定済み")
            gemini_key = server_gemini_key
        else:
            gemini_key = st.text_input(
                "Gemini API Key",
                type="password",
                help="診断結果に合わせた島からの手紙を生成します。この画面を閉じると消えます。",
            )

    current_fingerprints = {
        "nookipedia": hashlib.sha256(nook_key.encode("utf-8")).hexdigest() if nook_key else "",
        "gemini": hashlib.sha256(gemini_key.encode("utf-8")).hexdigest() if gemini_key else "",
    }
    for api_name, fingerprint in current_fingerprints.items():
        if st.session_state.api_key_fingerprints[api_name] != fingerprint:
            st.session_state.api_checks[api_name] = None
            st.session_state.api_key_fingerprints[api_name] = fingerprint

    if st.button("APIの接続を確認する", use_container_width=True):
        with st.spinner("接続を確認しています…"):
            st.session_state.api_checks["nookipedia"] = check_nookipedia(nook_key)
            st.session_state.api_checks["gemini"] = check_gemini(gemini_key)

    def connection_view(api_name: str, has_key: bool, server_configured: bool) -> tuple[str, str]:
        checked = st.session_state.api_checks[api_name]
        if not has_key:
            return "off", "○ 未接続"
        if checked is None:
            label = "△ Secrets設定済み・未確認" if server_configured else "△ キー入力済み・未確認"
            return "wait", label
        return ("ok", "● 接続済み") if checked[0] else ("error", f"× {checked[1]}")

    nook_class, nook_label = connection_view("nookipedia", bool(nook_key), bool(server_nook_key))
    gemini_class, gemini_label = connection_view("gemini", bool(gemini_key), bool(server_gemini_key))
    st.markdown(
        f"""
        <div class="connection-grid">
          <div class="connection-card {nook_class}">
            <span>Nookipedia</span><strong>{safe(nook_label)}</strong>
          </div>
          <div class="connection-card {gemini_class}">
            <span>Gemini</span><strong>{safe(gemini_label)}</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Nookipediaは住民データ、Geminiは「島からの手紙」に使います。")

tab_match, tab_letter = st.tabs(["01　診断する", "02　島からの手紙"])

with tab_match:
    st.markdown('<div class="section-label">Five quiet questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-note">直感で選んでください。正解はありません。</div>', unsafe_allow_html=True)

    with st.form("island_match_form"):
        nickname = st.text_input("島で呼ばれたい名前", placeholder="例：みなみ", max_chars=20)
        q1_col, q2_col = st.columns(2)
        with q1_col:
            pace = st.radio(
                "新しいことを始めるときは？",
                ["じっくり、自分のペース", "誰かと相談しながら", "その日の気分で"],
                key="pace_radio",
            )
            favorite = st.radio(
                "ゲームで一番好きな時間は？",
                ["景色をつくる", "住民と話す", "思い出を集める", "家具を整える", "限定アイテムを集める", "目的なく歩く"],
                key="favorite_radio",
            )
            season = st.radio(
                "いちばん好きな季節は？",
                ["春", "夏", "秋", "冬"],
                horizontal=True,
                key="season_radio",
            )
        with q2_col:
            mood = st.radio(
                "いま惹かれる風景は？",
                ["朝の海辺", "雨上がりの商店街", "夕方の自室", "深夜の広場", "季節のイベント"],
                key="mood_radio",
            )
            weekend = st.radio(
                "予定のない休日なら？",
                ["予定を決めずに過ごす", "友達と会う", "写真や日記を整理する", "部屋の模様替え"],
                key="weekend_radio",
            )
        submitted = st.form_submit_button("島時間を診断する　→", use_container_width=True)

    if submitted:
        answers = {
            "pace": pace,
            "favorite": favorite,
            "mood": mood,
            "weekend": weekend,
            "season": season,
        }
        scores = score_answers(answers)
        result_key = choose_result(scores, nickname)
        profile = ARCHETYPES[result_key]
        villager, villager_source = fetch_villager(
            nook_key, profile["personality"], f"{nickname}-{result_key}"
        )
        st.session_state.match = {
            "nickname": nickname,
            "answers": answers,
            "scores": scores,
            "key": result_key,
            "profile": profile,
            "villager": villager,
            "villager_source": villager_source,
        }
        st.session_state.letter = None

    if st.session_state.match:
        match = st.session_state.match
        profile = match["profile"]
        villager = match["villager"]
        st.markdown(
            f"""
            <section class="result-shell">
              <div class="result-no">{safe(profile['edition'])}</div>
              <h2>{safe(profile['jp'])}</h2>
              <div class="lead">{safe(profile['description'])}</div>
              <div class="quote">“{safe(profile['quote'])}”</div>
              <div class="meta-grid">
                <div class="meta-item"><span>Series</span><strong>{safe(profile['title'])}</strong></div>
                <div class="meta-item"><span>Lucky object</span><strong>{safe(profile['item'])}</strong></div>
                <div class="meta-item"><span>Best hour</span><strong>{safe(profile['time'])}</strong></div>
              </div>
            </section>
            """,
            unsafe_allow_html=True,
        )

        chart_col, villager_col = st.columns([1.15, 0.85], gap="large")
        with chart_col:
            st.markdown('<div class="section-label">Your balance</div>', unsafe_allow_html=True)
            st.plotly_chart(
                score_chart(match["scores"], match["key"]),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with villager_col:
            source_label = "LIVE DATA · NOOKIPEDIA API" if match["villager_source"] == "nookipedia" else "CURATED PREVIEW · API READY"
            st.markdown('<div class="section-label">Island companion</div>', unsafe_allow_html=True)
            image_url = villager.get("image_url")
            if image_url:
                image_col, info_col = st.columns([0.8, 1.2])
                with image_col:
                    st.image(image_url, use_container_width=True)
            else:
                info_col = st.container()
            with info_col:
                if image_url:
                    st.caption("Nookipediaから取得した住民画像")
                st.markdown(
                    f"""
                    <div class="api-card">
                      <span class="api-tag">{source_label}</span>
                      <div class="villager-name">{safe(villager['name'])}</div>
                      <div class="data-note">{safe(villager['species'])} / {safe(villager['personality'])}<br>
                      {safe(villager['phrase'])}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if villager.get("url"):
                    st.link_button("住民データを見る ↗", villager["url"], use_container_width=True)

with tab_letter:
    st.markdown('<div class="section-label">A letter from the island</div>', unsafe_allow_html=True)
    if not st.session_state.match:
        st.info("先に「01 診断する」で島時間を見つけてください。")
    else:
        match = st.session_state.match
        letter_left, letter_right = st.columns([0.72, 1.28], gap="large")
        with letter_left:
            st.markdown("#### 手紙に、いまの気分を少しだけ。")
            wish = st.text_area(
                "いま叶えたいこと",
                placeholder="例：新しいことを始めたい。でも少し不安。",
                height=140,
                max_chars=180,
            )
            if st.button("島から手紙を受け取る　→", use_container_width=True):
                st.session_state.letter = None
                with st.spinner("波の向こうから手紙を運んでいます。少しだけ待ってください…"):
                    text, source = generate_letter(
                        gemini_key,
                        match["profile"],
                        match["nickname"],
                        wish,
                    )
                    st.session_state.letter = {"text": text, "source": source}
                st.success("手紙が届きました。右側に表示しています。")
            st.markdown(
                '<p class="data-note">短い一言でも大丈夫です。Gemini接続時は入力内容に合わせて生成し、未接続時も内容に近い返事を選びます。</p>',
                unsafe_allow_html=True,
            )
        with letter_right:
            if st.session_state.letter:
                letter = st.session_state.letter
                source_label = "GENERATED WITH GEMINI API" if letter["source"] == "gemini" else "LOCAL LETTER PREVIEW"
                letter_html = "<br>".join(safe(letter["text"]).splitlines())
                st.markdown(
                    f"""
                    <article class="letter">
                      <div class="letter-date">{datetime.now().strftime('%d %B %Y')} · {source_label}</div>
                      {letter_html}
                    </article>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <article class="letter" style="display:flex;align-items:center;justify-content:center;color:#8b918c;text-align:center">
                      まだ何も書かれていない便箋。<br>
                      左に、いまの気分を置いてみてください。
                    </article>
                    """,
                    unsafe_allow_html=True,
                )

st.markdown(
    """
    <div class="footer-line">
      <span>Designed & coded by Minami</span>
      <span>Fan-made study project · Data via Nookipedia when connected</span>
    </div>
    """,
    unsafe_allow_html=True,
)
