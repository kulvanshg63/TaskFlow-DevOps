from flask import Flask, render_template, request, redirect, url_for
from database import initialize_database, get_db_connection

app = Flask(__name__)

initialize_database()


@app.route("/")
def home():
    connection = get_db_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    description = request.form["description"]

    connection = get_db_connection()

    connection.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):

    connection = get_db_connection()

    task = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]

        connection.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?
            WHERE id = ?
            """,
            (title, description, task_id)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    connection.close()

    return render_template("edit.html", task=task)


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

