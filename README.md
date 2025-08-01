## Prerequisites
* Python 3.10+
* [uv](https://github.com/astral-sh/uv)
* shell access

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
