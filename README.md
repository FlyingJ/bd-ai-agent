# Boot.dev AI agent

--

## Prerequisites

* Python 3.10+
* [uv](https://github.com/astral-sh/uv)
* shell access
* Google AI API key (can be created [here](https://aistudio.google.com/api-keys))

## Prepare the project environment

create projects

```
$ uv init your-project-name
$ cd your-project-name
```

create python virtual environment

```
$ uv venv
```

activate virtual environment

```
$ source .venv/bin/activate
```

add project module dependencies

```
$ uv add google-genai==1.12.1
$ uv add python-dotenv==1.1.0
```

## Run the project

```
$ uv run main.py
```

## Resources

[^1][Google AI Studio - API Keys](https://aistudio.google.com/api-keys)
[^2][Google Gen AI SDK Reference](https://googleapis.github.io/python-genai/)