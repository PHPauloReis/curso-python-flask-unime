from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = '2ac30843c6fa78461eedd6a3fd5c13e8446f12af'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "curso_python"
app.config["MYSQL_PORT"] = 3306

db = MySQL(app)


def get_all_tasks():
    query = "SELECT * FROM tasks"

    cursor = db.connection.cursor()
    cursor.execute(query)

    tasks = cursor.fetchall()
    task_list = []

    for task in tasks:
        task_list.append({
            "id": task[0],
            "title": task[1],
            "completed": task[2] == "Y",
            "created_at": task[3].strftime('%d/%m/%Y %H:%M')
        })

    cursor.close()

    return task_list


def get_filtered_tasks(filter):
    if filter == "in-course":
        query = "SELECT * FROM tasks WHERE completed='N'"
    elif filter == "completed":
        query = "SELECT * FROM tasks WHERE completed='Y'"
    else:
        return get_all_tasks()

    cursor = db.connection.cursor()
    cursor.execute(query)

    tasks = cursor.fetchall()
    task_list = []

    for task in tasks:
        task_list.append({
            "id": task[0],
            "title": task[1],
            "completed": task[2] == "Y",
            "created_at": task[3].strftime('%d/%m/%Y %H:%M')
        })

    cursor.close()

    return task_list


def insert_task(title):
    query = "INSERT INTO tasks (title) VALUES (%s)"
    cursor = db.connection.cursor()
    cursor.execute(query, [title])
    db.connection.commit()
    cursor.close()


def remove_task(id):
    query = "DELETE FROM tasks WHERE id = %s"
    cursor = db.connection.cursor()
    cursor.execute(query, [id])
    db.connection.commit()
    cursor.close()


def toogle_task(id):
    status = request.args.get("status")

    if status == 'True':
        query = "UPDATE tasks SET completed='N' WHERE id = %s"
    else:
        query = "UPDATE tasks SET completed='Y' WHERE id = %s"

    cursor = db.connection.cursor()
    cursor.execute(query, [id])
    db.connection.commit()
    cursor.close()


@app.route("/")
def index():
    filter_input = request.args.get("filter")

    return render_template("list.html", tasks=get_filtered_tasks(filter_input), filter=filter_input)


@app.route("/store/", methods=['POST'])
def store_task():
    task_title = request.form["task"]

    insert_task(task_title)

    flash("Tarefa cadastrada com sucesso!", "success")

    return redirect(url_for("index"))


@app.route("/delete/<int:id>")
def delete_task(id):
    remove_task(id)

    flash("Tarefa excluída com sucesso!", "success")

    return redirect(url_for("index"))


@app.route("/toogle-task/<int:id>")
def switch_task(id):
    toogle_task(id)

    return redirect(url_for("index"))


@app.route("/sobre-o-nucleo/")
def about():
    return render_template("about.html")


app.run(debug=True)
