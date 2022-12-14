from datetime import datetime
# The function below is the one provided by the instructors in project 4
def current_time() -> str:
    return datetime.now().strftime("%B %d, %Y at %H:%M:%S")