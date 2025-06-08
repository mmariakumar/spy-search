# Spy Search

**Spy Search** is an agentic search framework designed to outperform current web search agents with a focus on faster, more efficient daily usage.

While commercial solutions like Manus charge $200 per month, Spy Search leverages open-source models to provide a cost-effective alternative without sacrificing performance.

---

## Roadmap

- **Version 1.0:** Agentic Search Functionality  
- **Version 2.0:** Localized Cache to Accelerate Search Speed  

---

## Installation
First you have to clone the repo
```shell
git clone https://github.com/JasonHonKL/spy-search.git
```

To set up just run 
```shell
python setup.py
```

config the config.json file, you may copy the following template
```json
{
    "provider": "ollama",
    "model": "deepseek-r1:7b",
    "agents": [
        "reporter"
    ]
}
```

After that run 
```shell
docker build -t spy-searcher .   
docker run -p 8000:8000 -p 8080:8080 spy-searcher
```

Now you can access  
[http://localhost:8000](http://localhost:8000)

## Example Report
[Example](./report.md)


## Community 
[Discord](https://discord.gg/rrsMgBdJJt)

## Contribution

We welcome contributions of all kinds! Please note that Spy Search is currently in a rapid development phase focused on performance optimization. As a result, the codebase is evolving quickly and may undergo significant changes.

Join us in building the future of fast, affordable search!

## v0.3 
- [x] User Interface
- [x] pdf search
- [x] API
- [] Add log
- [] Local search
- [x] Report generation (pdf)
- [] Docker
- [] Email API & Notion API & Obsidian API


## Thank you everyone's support :) 
[![Star History Chart](https://api.star-history.com/svg?repos=JasonHonKL/spy-search&type=Date)](https://star-history.com/#JasonHonKL/spy-search&Date)
