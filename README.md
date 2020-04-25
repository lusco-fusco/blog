# Blog ![CD/CI](https://github.com/lusco-fusco/blog/workflows/CD/CI/badge.svg)
Our custom blog

## 👩‍💻👨‍💻 Development notes
First, configure your environment using .env file

Then, deploy the database container:
``sh
docker-compose up -d postgres
``

Migrate the schema (in project's root folder):
``sh
flask db init # First time you migrate app
flask db migrate
flask db upgrade
``

Leaving the debug variable as True edit your code while this is running:
 ``sh
python app.py
``

## 🚀 Deployment notes

If you want to deploy this blog:

First, configure your environment using .env file either filling secrets in your deployment platform.

Then build the blog image:
``sh
docker-compose build --no-cache app
``

Finally deploy the container:
``sh
docker-compose up -d app
``

## 🛠 Development requirements

* 🐍 Python ~ 3.7.6
* 🐋 Docker
* 🐙 Docker Compose
* 🐘 Dbeaver (recommed to do queries against Postgres)

## ✏🗒TODO list

* User
  * user's profile 
  * edit user details
  * update password
  * delete my account
  * Recommend articles
  * Retrieve my account
* Roles
  * Populate database if there is no roles in database
* Article
  * Tag articles
  * Recommend similar articles
  * Search by tags, author or raw text
  * Publish button
  * add pagination in home page, all articles page and comments
  * Render markdown as html
  * add markdown editor in creation article page
  * Create tag in article creation
* Reactions
  * Add animations to reactions emotions
