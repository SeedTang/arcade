# 小游戏大全 · Arcade

把四个浏览器小游戏收进一个入口：

| 游戏 | 说明 |
| --- | --- |
| [德州扑克](https://github.com/SeedTang/holdem) | 6/8 人桌，12 个性格固定的 AI 对手，德州 + 奥马哈 |
| [战争经济](https://github.com/SeedTang/war-economy) | 二战经济动员主题的 roguelike 卡牌构筑，18 种语言 |
| [势力均衡](https://github.com/SeedTang/balance-of-power) | 三方联盟博弈，跑在前面的会被围攻 |
| [满座](https://github.com/SeedTang/covers) | 餐厅翻台经营，十个晚上 |

**在线试玩：** https://seedtang.github.io/arcade/

## 这个仓库不存游戏代码

四个游戏各自还是独立仓库，这里只有门户页。两边分别这样把它们接进来：

- **线上** —— `.github/workflows/deploy.yml` 在构建时 `git clone` 那四个仓库到同名子目录，
  然后整体发布到 Pages。所以游戏更新后，重跑一次构建门户就同步了
  （push 本仓库 / 在 Actions 页手动触发 / 或等每天 06:00 UTC 的定时构建）。
- **本地** —— `serve.py` 把 `/<游戏名>/` 映射到相邻目录（`~/holdem`、`~/war-economy` …），
  同样不复制文件。在任何一个游戏里改完代码，刷新这个端口就能看到。

两边的路径结构一致，所以门户页里用相对链接即可，不用区分环境。

同理，各游戏左边缘那条「返回大全」窄条来自 `_back.js`，也是构建时插一行 script
（本地则是 `serve.py` 在响应里即时注入，**不落盘**）。游戏仓库里没有这个文件，
也不知道自己被收录了 —— 单独打开游戏仓库的 Pages 依然是原样。

## 本地运行

```bash
python3 serve.py          # 默认 8700
python3 serve.py 9000     # 换端口
```

游戏仓库要和 `arcade/` 平级：

```
~/
├── arcade/            ← 本仓库
├── holdem/
├── war-economy/
├── balance-of-power/
└── covers/
```

缺哪个 clone 哪个，服务器启动时会列出缺失的。

## 加一个新游戏

1. `index.html` 里的 `GAMES` 数组加一项（`dir` 要和仓库名一致）
2. `.github/workflows/deploy.yml` 的 clone 循环里加上仓库名
3. `serve.py` 的 `GAMES` 列表里加上

构建时会检查门户里每个 `dir` 都有对应目录，漏了哪步会直接让构建失败。
