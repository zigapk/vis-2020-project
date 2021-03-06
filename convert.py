import json
import csv


def parse_tag(prefix, obj):
    for tag in obj['tags']:
        if tag.lower().startswith(prefix.lower()):
            return int(tag[1:])
    raise Exception('tag not found')


events_data = json.loads(open('data/events.json').read())
exercises_data = json.loads(open('data/exercises.json').read())
exercise_ratings_data = json.loads(open('data/ratings.json').read())

exercises = {}
guid_to_id_position = {}
exercise_id_to_rating = {}

# parse exercise ratings into `exercise_id_to_rating`
for rating in exercise_ratings_data:
    elo_rating = rating['ratingELO']
    exercise = rating['exerciseId']
    exercise_id_to_rating[exercise] = elo_rating  # overwrite (take last rating)

# iterate over exercises and filter them
# then, parse all the questions as separate entities
for exercise in exercises_data:
    data = json.loads(exercise['data'])
    exercise_id = data['id']
    difficulty = parse_tag('D', data)
    topic = parse_tag('T', data)

    rating = 200 if exercise['exerciseId'] not in exercise_id_to_rating else exercise_id_to_rating[
        exercise['exerciseId']]

    # parametric
    if exercise_id.count('.') > 3:
        exercise_id = '.'.join(exercise_id.split('.')[:-1])

    if exercise_id not in exercises:
        exercises[exercise_id] = {
            'difficulty': difficulty,
            'topic': topic,
            'rating': rating,
            'questions': [],
        }

        for question in data['questions']:
            guid = question['guid']
            exercises[exercise_id]['questions'].append({
                'guid': guid,
                'achieved_points': 0,
                'total_points': 0,
                'questions_in_exercise': len(data['questions']),
                'exercise_id_int': exercise['exerciseId'],
                'answer_count': 0,
            })

    for i in range(len(data['questions'])):
        question = data['questions'][i]
        guid = question['guid']
        guid_to_id_position[guid] = (exercise_id, i)

# only remember last events for a single exercise (user might have changed his mind before submitting the quiz)
events = {}
for event in events_data:
    key = (event['questionGUID'], event['userId'])
    value = event['points'] / event['maxPoints']
    events[key] = value

for key, value in events.items():
    guid = key[0]

    exercise_id, index = guid_to_id_position[guid]

    exercises[exercise_id]['questions'][index]['achieved_points'] += value
    exercises[exercise_id]['questions'][index]['total_points'] += 1
    exercises[exercise_id]['questions'][index]['answer_count'] += 1

# output the data as csv to `data/export.csv`
with open('data/export.csv', 'w', newline='') as f:
    csv_writer = csv.writer(f, delimiter=',')

    # header
    csv_writer.writerow(
        ['exercise_id', 'question_guid', 'rating', 'topic', 'difficulty', 'average_result', 'questions_in_exercise',
         'exercise_id_int', 'answer_count'])

    for exercise_id, exercise_data in exercises.items():
        difficulty = exercise_data['difficulty']
        topic = exercise_data['topic']
        rating = exercise_data['rating']

        for question in exercise_data['questions']:
            avg = 0 if question['total_points'] == 0 else question['achieved_points'] / question['total_points']
            guid = question['guid']
            questions_in_exercise = question['questions_in_exercise']
            answer_count = question['answer_count']

            csv_writer.writerow(
                [exercise_id, guid, str(rating), str(topic), str(difficulty), str(avg), str(questions_in_exercise),
                 str(question['exercise_id_int']), str(answer_count)])
