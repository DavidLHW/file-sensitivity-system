from celery import Celery, group

app = Celery("task")
app.config_from_object("celeryconfig")

@app.task(trail=True)
def calculate_score(filepath, score_matrix):
    """ Calculate all the sensitivity score of individual file """
    try:
        # Open and read file.
        f = open(filepath)
        content = f.read().lower()

    except:
        # If file / filepath is wrong.
        return {"filepath": filepath, "score": -1}
    
    total_score = 0        

    # Calculate score.
    for keyword, score in score_matrix.items():
        count = content.count(keyword.lower())
        total_score += score * count

    return {"filepath": filepath, "score": total_score}


@app.task(trail=True)
def group_calculate_score(filepaths, score_matrix):
    """ Calculate all the sensitivity score of files uploaded currently """
    
    return group(calculate_score.s(filepath, score_matrix) for filepath in filepaths)()