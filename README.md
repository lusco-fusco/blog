# Blog ![CD/CI](https://github.com/lusco-fusco/blog/workflows/CD/CI/badge.svg)
Our custom blog

## 👩‍💻👨‍💻 Development notes
First, configure your environment using .env file

Then, deploy the database container:
```sh
docker-compose up -d postgres
```

Migrate the schema (in project's root folder):
```sh
flask db init # First time you migrate app
flask db migrate
flask db upgrade
```

Leaving the debug variable as True edit your code while this is running:
 ```sh
python app.py
```

## 🚀 Deployment notes

If you want to deploy this blog:

First, configure your environment using .env file either filling secrets in your deployment platform.

Then build the blog image:
```sh
docker-compose build --no-cache app
```

Finally deploy the container:
```sh
docker-compose up -d app
```

## 🛠 Development requirements

* 🐍 Python ~ 3.7.6
* 🐋 Docker
* 🐙 Docker Compose
* 🐘 Dbeaver (recommed to do queries against Postgres)

