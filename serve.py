#!/usr/bin/env python3
"""本地开发服务器：一个端口跑齐全部小游戏。

游戏各自还是独立仓库（~/holdem、~/war-economy …），这里**不复制文件**，
而是把 /<游戏名>/ 这样的路径映射到相邻的仓库目录。所以在任何一个游戏里
改完代码，刷新这个端口就能看到 —— 不需要同步。

线上由 .github/workflows/deploy.yml 在构建时把那几个仓库拉到同名子目录，
路径结构和本地一致，所以门户页里用相对链接两边都通。

    python3 serve.py [端口]        默认 8700
"""
import os
import posixpath
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.dirname(ROOT)                 # 各游戏仓库和 arcade 平级

GAMES = ['holdem', 'war-economy', 'balance-of-power', 'covers']


class ArcadeHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean = unquote(path.split('?', 1)[0].split('#', 1)[0])
        parts = [p for p in posixpath.normpath(clean).split('/') if p and p not in ('.', '..')]
        if parts and parts[0] in GAMES:
            # /holdem/art/x.png  ->  ~/holdem/art/x.png
            return os.path.join(HOME, parts[0], *parts[1:])
        return os.path.join(ROOT, *parts)

    def end_headers(self):
        # 不让浏览器缓存，否则改完代码刷新还是旧版（这个坑在 holdem 上踩过）
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

    def send_header(self, keyword, value):
        if keyword == 'Last-Modified':        # 免得浏览器拿它做条件请求命中 304
            return
        super().send_header(keyword, value)

    def log_message(self, fmt, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', 8700))
    missing = [g for g in GAMES if not os.path.isdir(os.path.join(HOME, g))]
    handler = partial(ArcadeHandler, directory=ROOT)
    with ThreadingHTTPServer(('127.0.0.1', port), handler) as httpd:
        print(f'小游戏大全 → http://localhost:{port}')
        for g in GAMES:
            mark = '缺失' if g in missing else os.path.join(HOME, g)
            print(f'  /{g}/'.ljust(22) + '→ ' + mark)
        if missing:
            print(f'\n提示：{", ".join(missing)} 在本地找不到，'
                  f'到 {HOME} 下 git clone 一份就能玩。')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
