**publish** is one of the simplest static site generators
### Usage
Put your markdown files to the *md-files* folder and launch *publish.py*:
```bash
python publish.py
```

### Installation

```bash
git clone git@github.com:Zamony/publish.git
pip install -r requirements.txt
```

### Visit your newly generated website
```bash
python -m http.server 8080
```
If you go to the *localhost:8080*, you will see your website.