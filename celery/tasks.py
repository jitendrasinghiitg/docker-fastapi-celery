import traceback
from time import sleep
from celery import states

from worker import celery_app


# create celery worker for 'hello.task' task
@celery_app.task(name="hello.task", bind=True)
def hello_world(self, name):
    try:
        # if name is error
        if name == "error":
            # will raise ZeroDivisionError
            a, b = 1, 0
            a = a / b

        # update task state every 1 second
        for i in range(60):
            sleep(1)
            self.update_state(state="PROGRESS", meta={"done": i, "total": 60})

        # return result
        return {"result": f"hello {name}"}

    # if any error occurs
    except Exception as ex:
        # update task state to failure
        self.update_state(
            state=states.FAILURE,
            meta={
                "exc_type": type(ex).__name__,
                "exc_message": traceback.format_exc().split("\n"),
            },
        )

        # raise exception
        raise ex
