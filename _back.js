/* 由门户注入到各游戏页面里的「返回大全」入口。
   游戏仓库本身不含这个文件，也不引用它：
   - 线上由 deploy.yml 在构建时往各游戏的 index.html 插一行 script
   - 本地由 serve.py 在响应时即时注入（不落盘，绝不改动游戏仓库）
   做成左边缘的一条窄条，悬停才展开 —— 各游戏自己的顶栏和底部按钮都占满了，
   贴边最不容易挡住东西。*/
(function () {
  if (window.__arcadeBack) return;
  window.__arcadeBack = true;

  var zh = true;
  try { zh = (localStorage.getItem('arcade_lang') || 'zh') === 'zh'; } catch (e) {}

  var css = document.createElement('style');
  css.textContent =
    '#arcade-back{position:fixed;left:0;top:50%;transform:translateY(-50%);z-index:2147483000;' +
    'display:flex;align-items:center;gap:6px;height:64px;width:17px;padding:0 4px;overflow:hidden;' +
    'background:rgba(8,14,12,.78);border:1px solid rgba(255,255,255,.16);border-left:none;' +
    'border-radius:0 11px 11px 0;color:#cfe0d4;text-decoration:none;white-space:nowrap;' +
    'font:600 12px/1 -apple-system,"PingFang SC","Hiragino Sans GB",system-ui,sans-serif;' +
    'letter-spacing:1px;cursor:pointer;backdrop-filter:blur(6px);' +
    'transition:width .18s ease,background .18s ease;}' +
    '#arcade-back:hover,#arcade-back:focus-visible{width:112px;background:rgba(12,22,18,.95);outline:none}' +
    '#arcade-back .chev{flex:0 0 auto;width:9px;text-align:center;color:#7fd8ab;font-size:15px}' +
    '@media (max-width:420px){#arcade-back{height:54px}}';
  document.head.appendChild(css);

  var a = document.createElement('a');
  a.id = 'arcade-back';
  a.href = '../';
  a.title = zh ? '返回小游戏大全' : 'Back to the arcade';
  a.innerHTML = '<span class="chev">‹</span><span>' +
    (zh ? '小游戏大全' : 'ARCADE') + '</span>';
  (document.body || document.documentElement).appendChild(a);
})();
