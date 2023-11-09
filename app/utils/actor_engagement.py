import pandas as pd


def change_assessment(verb, object_def_type):
    if object_def_type != 'assessment':
        return object_def_type

    if verb == 'submit' or verb == 'scored':
        object_def_type = 'homework'
    elif verb == 'completed' or verb == 'start':
        object_def_type = 'test'
    return object_def_type


def get_count(actor_df, object_def_type, verb):
    temp = actor_df[['object.definition.type', 'verb.id']].value_counts()
    if (object_def_type, verb) not in temp.index:
        return object_def_type, verb, 0

    count = temp.loc[(object_def_type, verb)]
    return object_def_type, verb, count


def get_score(actor_df, object_def_type, verb):
    scores = actor_df[(actor_df['object.definition.type'] == object_def_type) & (actor_df['verb.id'] == verb)][
        'result.score.scaled']
    if scores.empty:
        return None, None, None

    return min(scores), scores.mean(), max(scores)


def calculate_score(df):
    if df.empty:
        return 0
    total_score = max(0, df[df['result.success'] == True]['result.score.scaled'].fillna(0).mean())
    return total_score


def get_ratio(actor_df: pd.DataFrame, object_definition_type: str, verb_id1: str, verb_id2: str):
    n1 = \
        actor_df[
            (actor_df['object.definition.type'] == object_definition_type) & (actor_df['verb.id'] == verb_id1)].shape[
            0]
    n2 = \
        actor_df[
            (actor_df['object.definition.type'] == object_definition_type) & (actor_df['verb.id'] == verb_id2)].shape[
            0]
    return None if n2 == 0 else n1 / n2


def get_place_in_course(df, actor_id, course):
    course_df = df[df['Course'] == course]

    scores = []
    actor_score = 0
    for actor in set(course_df['actor.id']):
        actor_df = df[(df['actor.id'] == actor)]
        score = calculate_score(actor_df[actor_df['object.definition.type'].isin(['homework', 'quiz', 'test'])][
                                    ['result.score.scaled', 'result.success']])
        if actor == actor_id:
            actor_score = score

        scores.append(score)

    return sorted(list(dict.fromkeys(scores)))[::-1].index(actor_score) + 1, len(scores)


def get_place_in_institution(df, actor_id, instituiton):
    instituiton_df = df[df['Institution'] == instituiton]

    scores = []
    actor_score = 0
    for actor in set(instituiton_df['actor.id']):
        actor_df = df[(df['actor.id'] == actor)]
        score = calculate_score(actor_df[actor_df['object.definition.type'].isin(['homework', 'quiz', 'test'])][
                                    ['result.score.scaled', 'result.success']])
        if actor == actor_id:
            actor_score = score

        scores.append(score)

    return sorted(list(dict.fromkeys(scores)))[::-1].index(actor_score) + 1, len(scores)


def get_successful_assessments(actor_df, type_of_assessment):
    successful_assesment = actor_df[
        (actor_df['object.definition.type'] == type_of_assessment[0]) & (actor_df['verb.id'] == type_of_assessment[1])][
        'result.success'].shape[0]
    return successful_assesment


def resume_actor(df, actor_id):
    # This function makes a resume of an actor.

    df = df.copy()
    df['object.definition.type'] = df.apply(
        lambda row: change_assessment(row['verb.id'], row['object.definition.type']), axis=1)
    df = df[~df['object.definition.type'].isin(['page', 'review', 'meeting', 'survey', 'lesson'])]

    object_definition_types = set(df['object.definition.type'])
    object_def_types_w_verbs = [(object_def_type, verb) for object_def_type in object_definition_types for verb in
                                set(df[df['object.definition.type'] == object_def_type]['verb.id'])]

    items = []  # (object_def_type, verb, count)

    actor_df = df[df['actor.id'] == actor_id]

    for object_def_type, verb in object_def_types_w_verbs:
        object_def_type_with_count = get_count(actor_df, object_def_type, verb)
        items.append(object_def_type_with_count)

    actions_df = pd.DataFrame({'Type': [item[0] for item in items],
                               'Verb': [item[1] for item in items],
                               'Count': [item[2] for item in items]}).sort_values(by=['Count'],
                                                                                  ascending=False).reset_index().drop(
        'index', axis=1)

    min_score_homework, avg_score_homework, max_score_homework = get_score(actor_df, 'homework', 'scored')
    min_score_test, avg_score_test, max_score_test = get_score(actor_df, 'test', 'completed')
    min_score_quiz, avg_score_quiz, max_score_quiz = get_score(actor_df, 'quiz', 'completed')

    successful_assessments = [get_successful_assessments(actor_df, type_of_assessment) for type_of_assessment in
                              [('quiz', 'completed'), ('homework', 'scored'), ('test', 'completed')]]

    scores_df = pd.DataFrame({'Type': ['homework', 'test', 'quiz'],
                              'Min_Score': [min_score_homework, min_score_test, min_score_quiz],
                              'Avg_Score': [avg_score_homework, avg_score_test, avg_score_quiz],
                              'Max_Score': [max_score_homework, max_score_test, max_score_quiz]})

    course = actor_df['Course'].iloc[0]
    institution = actor_df['Institution'].iloc[0]

    place_in_course = get_place_in_course(df, actor_id, course)
    place_in_institution = get_place_in_institution(df, actor_id, institution)
    place = [place_in_course, place_in_institution]

    return actions_df, scores_df, successful_assessments, place


#def display_actor(df, actor_id):
#    actions_df, scores_df, successful_assessments, place = resume_actor(df, actor_id)
#
#    # display(actions_df) -> Тук трябва да го измислим как точно и кое
#    # display(scores_df) -> как точно да го представим
#    print(actions_df)
#    print('*'*50)
#    print(scores_df)
#    print('*'*50)
#    print(f'Number of successful quizzes: {successful_assessments[0]}')
#    print(f'Number of successful homeworks: {successful_assessments[1]}')
#    print(f'Number of successful tests: {successful_assessments[2]}')
#    print('*'*50)
#    print(place)
#    #display(place) -> Пак трябва да измислим как да го направим.


def resume_course_or_institution(df, id):
    institutions = set(df['Institution'])

    type_object = 'Institution' if id in institutions else 'Course'

    df = df.copy()
    df['object.definition.type'] = df.apply(
        lambda row: change_assessment(row['verb.id'], row['object.definition.type']), axis=1)
    df = df[~df['object.definition.type'].isin(['page', 'review', 'meeting', 'survey', 'lesson'])]

    object_definition_types = set(df['object.definition.type'])
    object_def_types_w_verbs = [(object_def_type, verb) for object_def_type in object_definition_types for verb in
                                set(df[df['object.definition.type'] == object_def_type]['verb.id'])]

    items = []  # (object_def_type, verb, count)

    object_df = df[df[type_object] == id]
    total_students = len(set(object_df['actor.id']))
    total_students_in_courses = None if type_object == 'Course' else object_df.groupby('Course')[
        'actor.id'].nunique().reset_index().rename(columns={'actor.id': 'Count'})

    for object_def_type, verb in object_def_types_w_verbs:
        object_def_type_with_count = get_count(object_df, object_def_type, verb)
        items.append(object_def_type_with_count)

    actions_df = pd.DataFrame({'Type': [item[0] for item in items],
                               'Verb': [item[1] for item in items],
                               'Count': [item[2] for item in items]}).sort_values(by=['Count'],
                                                                                  ascending=False).reset_index().drop(
        'index', axis=1)

    min_score_homework, avg_score_homework, max_score_homework = get_score(object_df, 'homework', 'scored')
    min_score_test, avg_score_test, max_score_test = get_score(object_df, 'test', 'completed')
    min_score_quiz, avg_score_quiz, max_score_quiz = get_score(object_df, 'quiz', 'completed')

    successful_assessments = [get_successful_assessments(object_df, type_of_assessment) for type_of_assessment in
                              [('quiz', 'completed'), ('homework', 'scored'), ('test', 'completed')]]

    scores_df = pd.DataFrame({'Type': ['homework', 'test', 'quiz'],
                              'Min_Score': [min_score_homework, min_score_test, min_score_quiz],
                              'Avg_Score': [avg_score_homework, avg_score_test, avg_score_quiz],
                              'Max_Score': [max_score_homework, max_score_test, max_score_quiz]})

    return actions_df, scores_df, successful_assessments, total_students, total_students_in_courses


#def display_course_or_institution(df, name):
#    actions_df, scores_df, successful_assessments, total_students, total_students_in_courses = resume_course_or_institution(
#        df, name)
#    # display(actions_df) -> Тук трябва да го измислим как точно и кое
#    # display(scores_df) -> как точно да го представим
#    print(f'Number of students in {name}: {total_students}')
#    print('*' * 50)
#
#    if total_students_in_courses is not None:
#        print(f"Number of students in {name}'s courses:\n{total_students_in_courses}")
#        print('*' * 50)
#
#    print(actions_df)
#    print('*' * 50)
#
#    print(f'Number of successful quizzes: {successful_assessments[0]}')
#    print(f'Number of successful homeworks: {successful_assessments[1]}')
#    print(f'Number of successful tests: {successful_assessments[2]}')
#    print('*' * 50)
#
#    print(scores_df)
#    print('*' * 50)
