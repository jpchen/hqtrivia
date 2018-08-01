from googleapiclient.discovery import build
from detect_text import prune_question
import time

# load config
import json
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

CUSTOM_SEARCH_API_KEY = data["GOOGLE"]["CUSTOM_SEARCH_API_KEY"]
CUSTOM_SEARCH_ENGINE_ID = data["GOOGLE"]["CUSTOM_SEARCH_ENGINE_ID"]

def run_query_all(question, answers, is_negative=False):
    """
    Runs queries according to two heuristics:
    - num results that appear the most on a question search
    - num of hits on a google search with the answer
    :param str question: question
    :param list answers: answers
    :return: answer with the highest score
    :rtype: str
    """
    max_count = -999
    min_count = 999
    if 'which' not in question.lower():
        # answers that appear ibe webpage the most
        result_counts = []
        output = search(question)['items']
        total_hits = 0
        for answer in answers:
            count = 0
            for result in output:
                count += result['title'].lower().count(answer.lower())
                count += result['snippet'].lower().count(answer.lower())
            total_hits += count
            if is_negative:
                if count < min_count:
                    min_count = count
                    best_ans = answer
            else:
                if count > max_count:
                    max_count = count
                    best_ans = answer
            result_counts.append((answer, count))
        for answer, result in result_counts:
            if answer == best_ans:
                print('\033[92m' + answer + ':  ' + str(result) + '\033[0m')
            else:
                print(answer + ':  ' + str(result))
        return best_ans
    else:
        # answers with the most results
        results = []
        question = question.lower().replace('which of the following', '')
        question = prune_question(question)
        for answer in answers:
            if (answer.startswith('"')):
                query = question + " " + answer
            else:
                query = question + ' "' + answer + '"'
            result = search(query)['searchInformation']['formattedTotalResults']
            score = int(result.replace(',', ''))
            if is_negative:
                if score < min_count:
                    min_count = score
                    best_ans = answer
            else:
                if score > max_count:
                    max_count = score
                    best_ans = answer
            results.append((answer, result))
        for answer, result in results:
            if answer == best_ans:
                print('\033[92m' + answer + ':  ' + result + '\033[0m')
            else:
                print(answer + ':  ' + result)
        return best_ans

def search(query):
    service = build("customsearch", "v1", developerKey=CUSTOM_SEARCH_API_KEY)
    res = service.cse().list(
        q=query,
        cx=CUSTOM_SEARCH_ENGINE_ID,
    ).execute()
    return res

