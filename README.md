# Thursday 19 November 2026 — The World in One Day

One broadsheet front-page image summing up the world's news of Thursday 19 November 2026: the Kerch bridge attacked again, the World Court rules Myanmar guilty of genocide against the Rohingya, and Anthropic's record IPO soars — 28 stories in all, every one dated that day.

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/Iruwae/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/Iruwae/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119)

See the competition: [news-image-20261119 on make.fun](https://make.fun/bounty/news-image-20261119)

## How it is built

`draw.py` (Python + PIL, no network, no photos) draws the whole 1024×1024 front page — masthead, six-number stat strip, three big leads, ten small drawn stories, a pinned world map, 15 more briefs, and a DATE CHECK box that leaves out 18 and 20 November news and anything not yet happened. `main.ts` copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Verify

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
cmp entry.png out/entry.png
```
