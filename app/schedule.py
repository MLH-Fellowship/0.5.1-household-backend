from app import db
from app.models import UserTask, Task, House, User
from app.utils import send_email
import time
import datetime
from app import q


def schedule_user_task(task_id):
    task: Task = Task.query.get(task_id)
    house: House = House.query.get(task.house_id)
    users = list(map(lambda x: {"user": x, "task_count": 0}, house.users))
    for i in range(len(users)):
        user: User = users[i]["user"]
        users[i]["task_count"] = len(user.tasks)
    least_task_user: User = next(sorted(users, lambda x: x["task_count"]))["user"]
    new_user_task = UserTask(
        task_id=task.id,
        user_id=least_task_user.id,
        deadline=time.time() + task.frequency,
        done=False,
    )
    db.session.add(new_user_task)
    db.session.commit()
    send_email(
        user.email,
        "New task.",
        """
    <h1>You have a new task</h1>
    <p>Name: {}</p>
    <p>Description: {}</p>
    <p>Deadline: {}</p>
    """.format(
            task.name,
            task.description,
            datetime.datetime.fromtimestamp(new_user_task.deadline).isoformat(),
        ),
        "You have a new task (Name: {}, Description: {}, Deadline: {})".format(
            task.name,
            task.description,
            datetime.datetime.fromtimestamp(new_user_task.deadline).isoformat(),
        ),
    )
    q.enqueue_at(datetime.datetime.now() + task.frequency, schedule_user_task, task.id)
