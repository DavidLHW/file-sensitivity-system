
from datetime import datetime
import json
import sys

sys.path.append("..")

from tasks import group_calculate_score
from tqdm import tqdm

from api.models.models import File
from api.database.database import db_session
from api.schemas.schemas import FileSchema

SCORE_MATRIX = json.load(open("scoreconfig.json"), encoding="utf8")

def retrieve_file_info():
    # Retrieve files from db.
    files = db_session.query(File).all()

    # Return serialised files.
    file_schema = FileSchema()
    data = file_schema.dump(files, many=True)

    print(f"Retrieved {len(data)} Files")

    return data


def update_file_info(data):
    if data==[]:
        print("No valid files found in database")
        return
    
    for file_info in data:
        # Identify file with filepath.
        filepath = file_info["filepath"]
        
        # Filter file by filepath.
        file = db_session.query(File).filter_by(filepath=filepath).first()

        if file_info["score"] == -1:
            print("File score not calculated:", file)
            continue

        # Update score and last_updated time.
        file.score = file_info["score"]
        file.last_updated = datetime.now()

        print("Updating File:", file.filename)

        db_session.commit()

    # Close session to prevent memory leaks.
    db_session.close()


def assign_tasks(data):
    print("Assigning tasks...")

    # Identify file with filepath.
    filepaths = [file_info["filepath"] for file_info in data]

    # Call celery task.
    delayed_results = group_calculate_score.delay(filepaths, SCORE_MATRIX)

    print("Tasks assigned", delayed_results)
    
    return delayed_results


def retrieve_task_results(delayed_results, data):
    # Wait for parent task to be ready.
    delayed_results.get()
    
    results = []
    # tqdm displays loading bar.
    for result in tqdm(delayed_results.children[0], total=len(data)):
        
        # Retrieve result.
        results.append(result.get())
    
    print(results)
    
    return results

    
if __name__ == '__main__':
    # Retrieve file information.
    data = retrieve_file_info()

    # Assign task to celery app.
    delayed_results = assign_tasks(data)

    # Retrieve results.
    results = retrieve_task_results(delayed_results, data)

    # Update results.
    update_file_info(results)