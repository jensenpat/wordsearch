<p align="center">
  <img src="https://user-images.githubusercontent.com/84298137/151912997-9f2d2583-d7c2-4870-bd08-f19521d3a9b4.png" width="220" alt="wordsearch">
</p>

<p align="center">
  <strong>wordsearch</strong> — a classic word search, in your terminal.
</p>

<p align="center">
  <a href="https://github.com/jensenpat/wordsearch/releases"><img src="https://img.shields.io/github/v/release/jensenpat/wordsearch?color=0b6" alt="release"></a>
  <a href="https://github.com/jensenpat/wordsearch/commits/master"><img src="https://img.shields.io/github/last-commit/jensenpat/wordsearch?color=0b6" alt="last commit"></a>
  <img src="https://img.shields.io/github/downloads/jensenpat/wordsearch/total.svg?color=0b6" alt="downloads">
  <img src="https://img.shields.io/github/stars/jensenpat/wordsearch.svg?color=0b6" alt="stars">
  <img src="https://img.shields.io/github/license/jensenpat/wordsearch?color=0b6" alt="license">
</p>

Relax and find the words. There is no clock on the puzzle — score is the length of each word you find. Built for 80-column serial terminals, tmux panes, and iTerm alike.

Based on a printable word search generator by [Christian Hill](https://scipython.com).

<p align="center">
  <img width="780" alt="wordsearch in the terminal" src="https://user-images.githubusercontent.com/84298137/136885856-792937bd-da47-4b01-be29-f2cfca099ffd.png">
</p>

## Features

- **100+ category puzzles** — ham radio, Unix, pizza, national parks, and plenty of nostalgia
- **Untimed scoring** — each word is worth its letter count; play at your own pace
- **Resize-aware curses UI** — the grid recenters, the word list wraps, small panes wait instead of crashing
- **Mouse in iTerm and tmux** — hover bolds a letter, click selects it (same rules as Space)
- **Keyboard** — arrows or vi keys (`hjkl`); Home / End jump the corners
- **Color themes** — `red`, `blue`, `green`, `purple`, `black`, or inherit your terminal palette
- **Finished puzzle stays up** — last word highlighted for a look or a screenshot before the next category
- **Session stats and high scores** — words found, puzzles, time played, averages; full-screen list on quit
- **Your own lists** — one word per line in a text file
- **BSD ports, macOS, Linux** — Python 3 and the standard `curses` module, nothing else

## Requirements

- Python 3
- A terminal that speaks ANSI / curses (including classic 80×24 serial)

No pip packages. `curses` ships with Python on Unix.

## Install and run

### From this repository

```sh
git clone https://github.com/jensenpat/wordsearch.git
cd wordsearch
chmod +x wordsearch
./wordsearch
```

Or download a [release](https://github.com/jensenpat/wordsearch/releases) archive and run `./wordsearch` from that tree.

### Packages

| System | Command |
| --- | --- |
| NetBSD pkgsrc | `pkgin add wordsearch` |
| OpenBSD ports | `pkg_add wordsearch` |
| FreeBSD ports | `pkg install wordsearch` |

After a ports install, `man wordsearch` has the full command list.

### tmux and iTerm

The game tracks window size (`KEY_RESIZE`) and works in a split. For mouse hover and click in tmux:

```sh
set -g mouse on
```

A 15×15 grid needs about **33×22** cells; 80×24 is the classic fit. If the pane is smaller, wordsearch waits for a resize instead of exiting.

## Play

Find every word in the category. Letters must be a **straight line** (including diagonals), in order, matching a placed word.

| Key | Action |
| --- | --- |
| Arrows or `h` `j` `k` `l` | Move |
| Space or left click | Select the letter under the cursor |
| Return | Clear the current selection (found words stay) |
| `Q` or Escape | Quit to the high-score screen |
| Ctrl-L | Redraw |

When a category is complete, the filled grid stays on screen. Any key starts a new random category; `Q` / Esc leaves.

On exit you get this session’s score, words, puzzles, time (and averages once a puzzle is finished), plus the top 10. Time is not shown during play.

## Command line

```
./wordsearch
./wordsearch -t blue
./wordsearch -s
./wordsearch -v
./wordsearch -h
```

| Flag | Meaning |
| --- | --- |
| `-t red\|blue\|black\|green\|purple` | Color theme. Omit `-t` to use the terminal’s own colors. |
| `-s` | Full-screen high score list (does not record a new score) |
| `-v` | Version |
| `-h` | Usage |

## Your own puzzles

Drop a `.txt` file in one of:

- `puzzles/` next to the `wordsearch` script
- `puzzles/` in the current working directory
- `/usr/local/share/wordsearch/`
- `/usr/pkg/share/wordsearch/`

One word per line, uppercase or mixed case (they are uppercased). Blank lines and `#` comments are ignored. A category is the file’s basename. Startup picks a random list from the first directory that has files.

Keep the whole list reasonably short so it wraps cleanly on a small pane.

## Contributing

Playing on a real serial terminal? A photo would make my day.

New word lists are welcome — email **wordsearch at passpackets.com** or open a pull request.

## License

[BSD-2-Clause](LICENSE). Copyright (c) 2022 Pat Jensen.
