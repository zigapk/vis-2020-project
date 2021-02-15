import json


def parse_tag(prefix, obj):
    for tag in obj['tags']:
        if tag.lower().startswith(prefix.lower()):
            return int(tag[1:])
    raise Exception('tag not found')


def


events_data = json.loads(open('data/events.json').read())
exercises_data = json.loads(open('data/exercises.json').read())

guid_to_data = {}

# parse all the questions (without parametric exercises)
for exercise in exercises_data:
    data = json.loads(exercise['data'])

    difficulty = parse_tag('D', data)
    topic = parse_tag('T', data)
    exercise_id = data['id']

    if exercise_id.count('.') > 3:
        continue  # skip parametric exercises

    for question in data['questions']:
        guid = question['guid']

        guid_to_data[guid] = {
            'achieved_points': 0,
            'total_points': 0,
            'exercise_id': exercise_id,
            'topic': topic,
            'difficulty': difficulty,
        }

events = {}

# only remember last events
for event in events_data:
    key = (event['questionGUID'], event['userId'])
    value = event['points'] / event['maxPoints']
    events[key] = value

for key, value in events.items():
    guid = key[0]

    if guid not in guid_to_data:
        continue

    guid_to_data[guid]['achieved_points'] += value
    guid_to_data[guid]['total_points'] += 1

print(','.join(['exercise_id', 'question_guid', 'topic', 'difficulty', 'average_result']))
for key, value in guid_to_data.items():
    avg = 0 if value['total_points'] == 0 else value['achieved_points'] / value['total_points']
    exercise_id = value['exercise_id']
    difficulty = value['difficulty']
    topic = value['topic']

    print(','.join([exercise_id, key, str(topic), str(difficulty), str(avg)]))
