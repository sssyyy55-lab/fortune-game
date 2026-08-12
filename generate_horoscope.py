#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
山羊座 毎朝運勢ジェネレーター
------------------------------------
実行するたびに「今日の日付」をシード値として、山羊座の運勢データを1つ生成する。
同じ日に何度実行しても同じ結果になる(日付固定シード)。

生成物:
  1. horoscope_today.json   … 今日の運勢データ(構造化データ)
  2. sns_post.txt           … SNS投稿用の短文
  3. fortune_game.html      … 診断形式の占いゲーム(和紙・朱色デザイン、1ファイル完結)

毎朝の自動実行を想定しているため、日付が変わるだけで内容が更新される。
"""

import json
import random
import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# 1. データプール
# ----------------------------------------------------------------------

HEADLINES = [
    "地道な努力が、静かに花開く一日",
    "足元を固めることで運が味方する日",
    "小さな決断が大きな信頼につながる日",
    "焦らず着実に進むほど道が開ける日",
    "積み重ねてきたものが評価される日",
    "自分のペースを守ることが吉と出る日",
    "誠実さが思わぬ形で報われる日",
    "計画を見直すと新しい発見がある日",
]

LOVE = [
    "素直な気持ちを伝えると、関係がぐっと深まりそう。飾らない言葉が響きます。",
    "焦って距離を縮めようとせず、相手のペースに合わせると◎。",
    "過去の誤解が解ける兆し。素直に歩み寄ってみて。",
    "一人の時間を大切にすることで、かえって魅力が増す一日。",
    "さりげない気配りが、相手の心をつかむきっかけに。",
    "本音を隠さず伝えることで、信頼関係が強まります。",
]

WORK = [
    "地道な作業ほど成果につながりやすいタイミング。手を抜かずコツコツと。",
    "周囲との連携がスムーズに進む日。一人で抱え込まず相談を。",
    "計画の見直しが吉。細部を詰めることで評価が上がります。",
    "新しい提案は今日ではなく、準備を整えてから動くと吉。",
    "責任感が評価され、任される仕事の幅が広がりそう。",
    "小さなミスに気づきやすい日。確認作業を丁寧に。",
]

MONEY = [
    "無駄遣いを見直すことで、思わぬ余裕が生まれそう。",
    "堅実な選択が吉。大きな買い物は少し様子を見て。",
    "臨時収入のチャンスあり。情報はしっかり確認を。",
    "貯蓄や資産管理を見直すのに向いている一日。",
    "人との金銭のやり取りは、細かい部分まで確認して。",
    "節約より「価値ある使い方」を意識すると満足度アップ。",
]

HEALTH = [
    "睡眠の質を意識すると、一日のパフォーマンスが上がります。",
    "軽いストレッチや散歩が、心身のバランスを整えてくれそう。",
    "無理をせず、休むことも仕事のうちと心得て。",
    "肩や首まわりの緊張に注意。こまめに体をほぐして。",
    "食生活を整えることで、気持ちも安定しやすい一日。",
    "深呼吸を意識するだけで、集中力が取り戻せそう。",
]

ADVICE = [
    "「継続は力なり」を胸に、今日も一歩ずつ。",
    "完璧を求めすぎず、六割の出来で前に進んでみて。",
    "頼れる人には、素直に頼ってみるのが吉。",
    "小さな達成感を積み重ねることが、明日への自信に。",
    "予定に余白を作ると、心にもゆとりが生まれます。",
    "「まあいいか」と流す勇気も、今日は必要かも。",
]

LUCKY_COLORS = ["朱色", "深緑", "生成り", "藍色", "山吹色", "墨色", "紅梅色"]
LUCKY_ITEMS = ["万年筆", "手帳", "湯呑み", "腕時計", "折り紙", "扇子", "御守り"]

# ----------------------------------------------------------------------
# 2. 今日のデータ生成(日付シードで固定)
# ----------------------------------------------------------------------

def generate_today_data(target_date: datetime.date) -> dict:
    seed = int(target_date.strftime("%Y%m%d"))
    rng = random.Random(seed)

    data = {
        "date": target_date.isoformat(),
        "date_jp": f"{target_date.year}年{target_date.month}月{target_date.day}日",
        "sign": "山羊座",
        "overall_score": rng.randint(2, 5),  # 2〜5の星
        "headline": rng.choice(HEADLINES),
        "love": rng.choice(LOVE),
        "work": rng.choice(WORK),
        "money": rng.choice(MONEY),
        "health": rng.choice(HEALTH),
        "advice": rng.choice(ADVICE),
        "lucky_color": rng.choice(LUCKY_COLORS),
        "lucky_item": rng.choice(LUCKY_ITEMS),
        "lucky_number": rng.randint(1, 9),
    }
    return data


# ----------------------------------------------------------------------
# 3. SNS投稿用テキスト生成
# ----------------------------------------------------------------------

def build_sns_post(data: dict) -> str:
    stars = "★" * data["overall_score"] + "☆" * (5 - data["overall_score"])
    text = (
        f"【今日の山羊座】{data['date_jp']}\n"
        f"{stars}\n"
        f"{data['headline']}。\n"
        f"✨ラッキーカラー：{data['lucky_color']}／ラッキーアイテム：{data['lucky_item']}\n"
        f"{data['advice']}\n"
        f"#今日の運勢 #山羊座 #占い"
    )
    return text


# ----------------------------------------------------------------------
# 4. 診断ゲーム(HTML)生成
# ----------------------------------------------------------------------

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>山羊座 今日の運勢診断</title>
<style>
  :root{
    --washi: #f3ecd9;
    --washi-dark: #e8dfc4;
    --ink: #3a2e26;
    --ink-soft: #6b5c4d;
    --shu: #c8390d;
    --shu-dark: #9c2c08;
    --shu-soft: #e0703f;
    --gold: #b8860b;
  }
  *{ box-sizing: border-box; }
  html,body{
    margin:0; padding:0;
    min-height:100vh;
    font-family: "Hiragino Mincho ProN","Yu Mincho","Noto Serif JP",serif;
    color: var(--ink);
    background-color: var(--washi);
    background-image:
      radial-gradient(circle at 20% 30%, rgba(255,255,255,0.35) 0, transparent 40%),
      radial-gradient(circle at 80% 70%, rgba(255,255,255,0.25) 0, transparent 45%),
      repeating-linear-gradient(0deg, rgba(120,100,70,0.03) 0px, rgba(120,100,70,0.03) 1px, transparent 1px, transparent 3px),
      repeating-linear-gradient(90deg, rgba(120,100,70,0.025) 0px, rgba(120,100,70,0.025) 1px, transparent 1px, transparent 3px);
    background-blend-mode: multiply;
  }
  .washi-noise{
    position: fixed; inset: 0; pointer-events:none; opacity:.5; mix-blend-mode: multiply;
  }
  .container{
    max-width: 520px;
    margin: 0 auto;
    padding: 32px 20px 64px;
    position: relative;
    z-index: 1;
  }
  header{
    text-align:center;
    margin-bottom: 28px;
  }
  .kamon{
    width:56px; height:56px; margin:0 auto 10px;
    border: 2px solid var(--shu);
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    color: var(--shu);
    font-size: 26px;
    background: radial-gradient(circle, rgba(200,57,13,0.06), transparent 70%);
  }
  h1{
    font-size: 22px;
    letter-spacing: 0.12em;
    margin: 0 0 6px;
    color: var(--ink);
  }
  .sub{
    font-size: 12px;
    letter-spacing: 0.15em;
    color: var(--ink-soft);
  }
  .card{
    background: linear-gradient(180deg, #fffdf6, #f7f0dc);
    border: 1px solid rgba(150,110,60,0.25);
    border-radius: 6px;
    padding: 24px 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(80,50,20,0.08);
    position: relative;
  }
  .card::before{
    content:"";
    position:absolute; top:6px; left:6px; right:6px; bottom:6px;
    border: 1px solid rgba(200,57,13,0.15);
    border-radius: 4px;
    pointer-events:none;
  }
  .q-title{
    font-size: 15px;
    line-height: 1.7;
    margin: 0 0 18px;
    text-align:center;
    color: var(--ink);
  }
  .q-count{
    text-align:center;
    font-size: 11px;
    color: var(--shu);
    letter-spacing: .1em;
    margin-bottom: 6px;
  }
  .options{
    display:flex; flex-direction:column; gap:10px;
  }
  .option-btn{
    font-family: inherit;
    font-size: 14px;
    padding: 12px 16px;
    background: #fff;
    border: 1px solid rgba(150,110,60,0.4);
    border-radius: 4px;
    cursor: pointer;
    text-align: left;
    color: var(--ink);
    transition: all .15s ease;
  }
  .option-btn:hover{
    background: rgba(200,57,13,0.08);
    border-color: var(--shu);
    color: var(--shu-dark);
  }
  .start-btn, .restart-btn{
    display:block;
    margin: 8px auto 0;
    font-family: inherit;
    font-size: 15px;
    letter-spacing: .1em;
    padding: 13px 30px;
    background: var(--shu);
    color: #fff8ee;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    box-shadow: 0 3px 0 var(--shu-dark);
  }
  .start-btn:active, .restart-btn:active{
    transform: translateY(2px);
    box-shadow: 0 1px 0 var(--shu-dark);
  }
  .intro-text{
    text-align:center;
    font-size: 13px;
    line-height: 2;
    color: var(--ink-soft);
    margin-bottom: 20px;
  }
  .progress{
    display:flex;
    justify-content:center;
    gap:6px;
    margin-bottom: 18px;
  }
  .dot{
    width:7px; height:7px; border-radius:50%;
    background: rgba(150,110,60,0.3);
  }
  .dot.active{ background: var(--shu); }
  .result-title{
    text-align:center;
    font-size: 12px;
    letter-spacing: .2em;
    color: var(--shu);
    margin-bottom: 6px;
  }
  .result-type{
    text-align:center;
    font-size: 20px;
    font-weight:bold;
    margin-bottom: 16px;
    color: var(--ink);
  }
  .stars{
    text-align:center;
    color: var(--gold);
    font-size: 20px;
    letter-spacing: 3px;
    margin-bottom: 14px;
  }
  .result-headline{
    text-align:center;
    font-size: 15px;
    margin-bottom: 18px;
    color: var(--ink);
  }
  .result-section{
    border-top: 1px dashed rgba(150,110,60,0.35);
    padding-top: 14px;
    margin-top: 14px;
  }
  .result-section .label{
    font-size: 11px;
    letter-spacing: .15em;
    color: var(--shu);
    margin-bottom: 6px;
  }
  .result-section .body{
    font-size: 14px;
    line-height: 1.9;
    color: var(--ink);
  }
  .lucky-row{
    display:flex;
    justify-content: space-around;
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px dashed rgba(150,110,60,0.35);
    font-size: 12px;
    color: var(--ink-soft);
    text-align:center;
  }
  .lucky-row b{
    display:block;
    color: var(--shu-dark);
    font-size: 14px;
    margin-top: 2px;
  }
  .advice-box{
    margin-top: 18px;
    padding: 14px 16px;
    background: rgba(200,57,13,0.06);
    border-left: 3px solid var(--shu);
    font-size: 13px;
    line-height: 1.8;
  }
  footer{
    text-align:center;
    font-size: 10px;
    color: var(--ink-soft);
    letter-spacing: .1em;
    margin-top: 24px;
    opacity:.7;
  }
  .hidden{ display:none; }
</style>
</head>
<body>

<svg class="washi-noise" width="0" height="0">
  <filter id="washiFilter">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" result="noise"/>
    <feColorMatrix in="noise" type="matrix"
      values="0 0 0 0 0.6
              0 0 0 0 0.55
              0 0 0 0 0.45
              0 0 0 0.05 0"/>
  </filter>
</svg>
<div class="washi-noise" style="filter:url(#washiFilter);"></div>

<div class="container">
  <header>
    <div class="kamon">卯</div>
    <h1>今日の山羊座 診断</h1>
    <div class="sub">CAPRICORN DAILY FORTUNE</div>
  </header>

  <!-- INTRO -->
  <div class="card" id="screen-intro">
    <p class="intro-text">
      いくつかの質問に答えると、<br>
      今日のあなたに必要な運勢を占います。<br>
      <span style="color:var(--shu-dark);">%%DATE_JP%%</span> の山羊座
    </p>
    <button class="start-btn" onclick="startQuiz()">診断をはじめる</button>
  </div>

  <!-- QUIZ -->
  <div class="card hidden" id="screen-quiz">
    <div class="progress" id="progress"></div>
    <div class="q-count" id="q-count"></div>
    <p class="q-title" id="q-title"></p>
    <div class="options" id="q-options"></div>
  </div>

  <!-- RESULT -->
  <div class="card hidden" id="screen-result">
    <div class="result-title">今日、あなたが向き合うテーマは</div>
    <div class="result-type" id="result-type"></div>
    <div class="stars" id="result-stars"></div>
    <div class="result-headline" id="result-headline"></div>

    <div class="result-section">
      <div class="label" id="result-label"></div>
      <div class="body" id="result-body"></div>
    </div>

    <div class="advice-box" id="result-advice"></div>

    <div class="lucky-row">
      <div>ラッキーカラー<b id="lucky-color"></b></div>
      <div>ラッキーアイテム<b id="lucky-item"></b></div>
      <div>ラッキーナンバー<b id="lucky-number"></b></div>
    </div>

    <button class="restart-btn" onclick="restartQuiz()">もう一度診断する</button>
  </div>

  <footer>%%DATE_JP%% ・ 山羊座の今日の運勢より</footer>
</div>

<script>
// ---- 今日の運勢データ(スクリプトにより毎朝自動更新) ----
const TODAY = %%DATA_JSON%%;

// ---- 診断質問(回答ごとに恋愛/仕事/金運/健康のいずれかにポイント) ----
const QUESTIONS = [
  {
    title: "今、一番気になっているのはどれ？",
    options: [
      { text: "気になる人との関係", axis: "love" },
      { text: "仕事や勉強の進み具合", axis: "work" },
      { text: "お財布事情", axis: "money" },
      { text: "最近の体調", axis: "health" }
    ]
  },
  {
    title: "今日の気分に近いのは？",
    options: [
      { text: "誰かと話したい気分", axis: "love" },
      { text: "何かに集中したい気分", axis: "work" },
      { text: "先のことを考えたい気分", axis: "money" },
      { text: "ゆっくり休みたい気分", axis: "health" }
    ]
  },
  {
    title: "最近、少し引っかかっていることは？",
    options: [
      { text: "素直になれない自分がいる", axis: "love" },
      { text: "頑張りが評価されているか不安", axis: "work" },
      { text: "出費が増えている気がする", axis: "money" },
      { text: "疲れが抜けにくい", axis: "health" }
    ]
  },
  {
    title: "今日、誰かに褒められるならどんな言葉がうれしい？",
    options: [
      { text: "「一緒にいると安心する」", axis: "love" },
      { text: "「頼りになるね」", axis: "work" },
      { text: "「しっかりしてるね」", axis: "money" },
      { text: "「元気そうで良かった」", axis: "health" }
    ]
  }
];

const AXIS_LABEL = {
  love: "💞 恋愛運",
  work: "💼 仕事運",
  money: "💰 金運",
  health: "🌿 健康運"
};
const AXIS_TYPE = {
  love: "情熱型 〜心で動くあなたへ〜",
  work: "着実型 〜積み上げるあなたへ〜",
  money: "堅実型 〜備えるあなたへ〜",
  health: "癒し型 〜整えるあなたへ〜"
};

let current = 0;
const scores = { love: 0, work: 0, money: 0, health: 0 };

function startQuiz(){
  current = 0;
  scores.love = scores.work = scores.money = scores.health = 0;
  document.getElementById('screen-intro').classList.add('hidden');
  document.getElementById('screen-result').classList.add('hidden');
  document.getElementById('screen-quiz').classList.remove('hidden');
  renderQuestion();
}

function renderQuestion(){
  const q = QUESTIONS[current];
  document.getElementById('q-count').textContent = `Q${current+1} / ${QUESTIONS.length}`;
  document.getElementById('q-title').textContent = q.title;

  const progress = document.getElementById('progress');
  progress.innerHTML = "";
  QUESTIONS.forEach((_, i) => {
    const dot = document.createElement('div');
    dot.className = 'dot' + (i <= current ? ' active' : '');
    progress.appendChild(dot);
  });

  const optsEl = document.getElementById('q-options');
  optsEl.innerHTML = "";
  q.options.forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = opt.text;
    btn.onclick = () => {
      scores[opt.axis]++;
      current++;
      if(current < QUESTIONS.length){
        renderQuestion();
      } else {
        showResult();
      }
    };
    optsEl.appendChild(btn);
  });
}

function showResult(){
  let topAxis = 'love';
  let topScore = -1;
  for(const axis in scores){
    if(scores[axis] > topScore){
      topScore = scores[axis];
      topAxis = axis;
    }
  }

  document.getElementById('screen-quiz').classList.add('hidden');
  document.getElementById('screen-result').classList.remove('hidden');

  document.getElementById('result-type').textContent = AXIS_TYPE[topAxis];
  document.getElementById('result-stars').textContent =
    "★".repeat(TODAY.overall_score) + "☆".repeat(5 - TODAY.overall_score);
  document.getElementById('result-headline').textContent = TODAY.headline;
  document.getElementById('result-label').textContent = AXIS_LABEL[topAxis];
  document.getElementById('result-body').textContent = TODAY[topAxis];
  document.getElementById('result-advice').textContent = "✦ 今日のひとこと　" + TODAY.advice;
  document.getElementById('lucky-color').textContent = TODAY.lucky_color;
  document.getElementById('lucky-item').textContent = TODAY.lucky_item;
  document.getElementById('lucky-number').textContent = TODAY.lucky_number;
}

function restartQuiz(){
  document.getElementById('screen-result').classList.add('hidden');
  document.getElementById('screen-intro').classList.remove('hidden');
}
</script>
</body>
</html>
"""


def build_game_html(data: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False)
    html = HTML_TEMPLATE.replace("%%DATA_JSON%%", data_json)
    html = html.replace("%%DATE_JP%%", data["date_jp"])
    return html


# ----------------------------------------------------------------------
# 5. メイン処理
# ----------------------------------------------------------------------

def main():
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()  
    data = generate_today_data(today)

    # 1) JSON保存
    json_path = os.path.join(SCRIPT_DIR, "horoscope_today.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 2) SNS投稿文
    sns_text = build_sns_post(data)
    sns_path = os.path.join(SCRIPT_DIR, "sns_post.txt")
    with open(sns_path, "w", encoding="utf-8") as f:
        f.write(sns_text)

    # 3) 診断ゲームHTML
    html = build_game_html(data)
    html_path = os.path.join(SCRIPT_DIR, "fortune_game.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("=== 生成完了 ===")
    print(f"- {json_path}")
    print(f"- {sns_path}")
    print(f"- {html_path}")
    print()
    print("--- SNS投稿文プレビュー ---")
    print(sns_text)


if __name__ == "__main__":
    main()
