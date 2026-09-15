A totally serious, mathematically advanced CLI tool to generate and debug DuckyScript payloads before your USB stick embarrasses you in public.

Works on macOS, Linux, and Windows. Probably runs on an overpriced smart fridge if it has Python 3.

---

### Why?
Because you forgot to put a `DELAY` after pressing the GUI key, your computer lagged for 0.2 seconds, and now your payload typed your commands into a random Spotify search bar instead of a terminal.

### What it does
- **Generates** a basic payload so you can pretend your computer is haunted.
- **Analyzes** your sketchy `.txt` files to find missing delays and typos before hardware does.
- **Tells you** how many seconds of your life are spent waiting on `DELAY` statements.
- **Zero external dependencies**: written in standard Python, because installing 400 MB of pip packages for a text parser is criminal.

---

### Usage

Run it directly:

python3 ducky_tool.py