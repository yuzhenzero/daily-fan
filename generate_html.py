import json

# Read episode data
with open('D:/Code/daily-fan/episodes.json', 'r', encoding='utf-8') as f:
    episodes = json.load(f)

# Build compact JS array string
ep_js_lines = []
for ep in episodes:
    ep_js_lines.append(
        '    {{"ep_id":{},"title":"{}","long_title":"{}","cover":"{}","url":"{}"}}'.format(
            ep['ep_id'],
            ep['title'].replace('"', '\\"'),
            ep['long_title'].replace('"', '\\"'),
            ep['cover'],
            ep['url']
        )
    )
episodes_js = "const EPISODES = [\n" + ",\n".join(ep_js_lines) + "\n];"

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="referrer" content="no-referrer">
  <title>凡人修仙传 — 每日一集</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0f0f1a;
      --card-bg: #1a1a2e;
      --text: #e0e0e0;
      --text-secondary: #a0a0b8;
      --accent: #09b389;
      --accent-hover: #0cc9a0;
      --link: #00a1d6;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", Roboto, sans-serif;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      background-image: radial-gradient(ellipse at 50% 0%, #1a1a3e 0%, var(--bg) 60%);
    }

    #app {
      width: 100%;
      max-width: 520px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    header {
      text-align: center;
      margin-bottom: 28px;
    }

    header h1 {
      font-size: 2rem;
      font-weight: 700;
      background: linear-gradient(135deg, #09b389, #0cc9a0);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 4px;
    }

    .subtitle {
      font-size: 0.95rem;
      color: var(--text-secondary);
      letter-spacing: 0.05em;
    }

    #card {
      background: var(--card-bg);
      border-radius: 16px;
      padding: 24px;
      width: 100%;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 2px 8px rgba(0, 0, 0, 0.2);
      transition: opacity 0.2s ease, transform 0.2s ease;
      opacity: 1;
    }

    #card.fade-out { opacity: 0; transform: translateY(8px); }

    #card:hover {
      box-shadow: 0 12px 40px rgba(9, 179, 137, 0.15), 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    #episode-link {
      display: block;
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 20px;
      line-height: 0;
      transition: transform 0.2s ease;
    }

    #episode-link:hover { transform: scale(1.02); }

    #episode-cover {
      width: 100%;
      aspect-ratio: 16 / 9;
      object-fit: cover;
      background: #2a2a3e;
      border-radius: 12px;
      display: block;
    }

    #episode-cover.loading {
      animation: shimmer 1.5s infinite;
      background: linear-gradient(90deg, #2a2a3e 25%, #35355a 50%, #2a2a3e 75%);
      background-size: 200% 100%;
    }

    @keyframes shimmer {
      0% { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }

    #episode-link-title {
      display: block;
      text-decoration: none;
      color: var(--text);
      margin-bottom: 24px;
      transition: color 0.2s ease;
    }

    #episode-link-title:hover { color: var(--link); }

    #episode-title {
      font-size: 1.25rem;
      font-weight: 600;
      text-align: center;
      line-height: 1.5;
      word-break: break-word;
      overflow-wrap: break-word;
    }

    .ep-num {
      color: var(--accent);
      font-weight: 700;
    }

    #reroll-btn {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      width: 100%;
      padding: 14px 36px;
      font-size: 1.1rem;
      font-weight: 600;
      color: #fff;
      background: linear-gradient(135deg, #09b389, #078f6e);
      border: none;
      border-radius: 50px;
      cursor: pointer;
      transition: all 0.25s ease;
      box-shadow: 0 4px 16px rgba(9, 179, 137, 0.3);
    }

    #reroll-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(9, 179, 137, 0.45);
    }

    #reroll-btn:active {
      transform: translateY(0);
      box-shadow: 0 2px 8px rgba(9, 179, 137, 0.3);
    }

    #reroll-btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    .btn-icon {
      display: inline-block;
      font-size: 1.3rem;
      transition: transform 0.4s ease;
    }

    #reroll-btn:active .btn-icon { transform: rotate(180deg); }

    footer {
      margin-top: 24px;
      text-align: center;
      font-size: 0.8rem;
      color: var(--text-secondary);
    }

    footer a { color: var(--link); text-decoration: none; }
    footer a:hover { text-decoration: underline; }

    @media (max-width: 600px) {
      #card { padding: 16px; border-radius: 12px; }
      header h1 { font-size: 1.6rem; }
      #episode-title { font-size: 1.1rem; }
      #reroll-btn { padding: 12px 28px; font-size: 1rem; }
    }
  </style>
</head>
<body>
  <div id="app">
    <header>
      <h1>凡人修仙传</h1>
      <p class="subtitle">随缘看一集</p>
    </header>

    <main id="card">
      <a id="episode-link" href="#" target="_blank" rel="noopener">
        <img id="episode-cover" class="loading"
             src=""
             alt=""
             referrerpolicy="no-referrer"
             onerror="handleImageError(this)">
      </a>

      <a id="episode-link-title" href="#" target="_blank" rel="noopener">
        <h2 id="episode-title">加载中...</h2>
      </a>

      <button id="reroll-btn">
        <span class="btn-icon">🎲</span> 换一集
      </button>
    </main>

    <footer>
      <p id="footer-status">数据来源 <a href="https://www.bilibili.com/bangumi/play/ss28747" target="_blank" rel="noopener">Bilibili</a> · 共 __EP_COUNT__ 集 · 更新于 2026-07-04</p>
    </footer>
  </div>

  <noscript>
    <div style="text-align:center;padding:40px;color:#e0e0e0;font-family:sans-serif;">
      <p>请启用 JavaScript 以使用此页面。</p>
    </div>
  </noscript>

  <script>
__EPISODES_JS__

(function() {
  var currentIdx = -1;

  function getRandomIdx() {
    if (EPISODES.length === 0) return -1;
    if (EPISODES.length === 1) return 0;
    var idx;
    do {
      idx = Math.floor(Math.random() * EPISODES.length);
    } while (idx === currentIdx);
    return idx;
  }

  function displayEpisode(idx) {
    var ep = EPISODES[idx];
    if (!ep) return;

    var img = document.getElementById('episode-cover');
    img.classList.remove('loading');
    img.src = ep.cover;
    img.alt = ep.long_title || ('第' + ep.title + '集');

    var titleEl = document.getElementById('episode-title');
    var displayTitle;
    if (ep.long_title) {
      displayTitle = '第<span class="ep-num">' + ep.title + '</span>集 ' + ep.long_title;
    } else {
      displayTitle = '第<span class="ep-num">' + ep.title + '</span>集';
    }
    titleEl.innerHTML = displayTitle;

    var linkImg = document.getElementById('episode-link');
    var linkTitle = document.getElementById('episode-link-title');
    linkImg.href = ep.url;
    linkTitle.href = ep.url;

    currentIdx = idx;
  }

  function onReroll() {
    var idx = getRandomIdx();
    if (idx < 0) return;

    var card = document.getElementById('card');
    card.classList.add('fade-out');
    setTimeout(function() {
      displayEpisode(idx);
      card.classList.remove('fade-out');
    }, 200);
  }

  window.handleImageError = function(img) {
    img.classList.remove('loading');
    img.src = 'data:image/svg+xml,' + encodeURIComponent(
      '<svg xmlns="http://www.w3.org/2000/svg" width="480" height="270" viewBox="0 0 480 270">' +
      '<rect fill="#2a2a3e" width="480" height="270"/>' +
      '<text fill="#a0a0b8" font-family="sans-serif" font-size="18" x="50%" y="50%" text-anchor="middle" dy=".3em">封面加载失败</text>' +
      '</svg>'
    );
    img.alt = '封面加载失败';
  };

  // Init
  if (EPISODES.length === 0) {
    document.getElementById('episode-cover').classList.remove('loading');
    document.getElementById('episode-cover').style.display = 'none';
    document.getElementById('episode-title').textContent = '暂无剧集数据';
    document.getElementById('episode-link').removeAttribute('href');
    document.getElementById('episode-link-title').removeAttribute('href');
    document.getElementById('reroll-btn').disabled = true;
  } else {
    document.getElementById('reroll-btn').addEventListener('click', onReroll);
    displayEpisode(getRandomIdx());
  }
})();
</script>
</body>
</html>'''

html = html.replace('__EP_COUNT__', str(len(episodes)))
html = html.replace('__EPISODES_JS__', episodes_js)

with open('D:/Code/daily-fan/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'index.html written successfully')
print(f'Episodes embedded: {len(episodes)}')
print(f'File size: {len(html.encode("utf-8")):,} bytes')
