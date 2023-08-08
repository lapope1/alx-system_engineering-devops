#!/usr/bin/python3
'''A module containing functions for working with the Reddit API.
'''
import requests

def sort_histogram(histogram={}):
    '''Sorts and prints the given histogram.
    '''
    filtered_histogram = list(filter(lambda kv: kv[1], histogram))
    histogram_dict = {}
    for item in filtered_histogram:
        if item[0] in histogram_dict:
            histogram_dict[item[0]] += item[1]
        else:
            histogram_dict[item[0]] = item[1]
    sorted_histogram = list(histogram_dict.items())
    sorted_histogram.sort(
        key=lambda kv: kv[0],
        reverse=False
    )
    sorted_histogram.sort(
        key=lambda kv: kv[1],
        reverse=True
    )
    result_str = '\n'.join(list(map(
        lambda kv: '{}: {}'.format(kv[0], kv[1]),
        sorted_histogram
    )))
    if result_str:
        print(result_str)

def count_words(subreddit, word_list, word_histogram=[], word_count=0, after=None):
    '''Counts the number of times each word in a given wordlist
    occurs in a given subreddit.
    '''
    api_headers = {
        'Accept': 'application/json',
        'User-Agent': ' '.join([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/97.0.4692.71',
            'Safari/537.36',
            'Edg/97.0.1072.62'
        ])
    }
    sort_order = 'hot'
    post_limit = 30
    response = requests.get(
        '{}/r/{}/.json?sort={}&limit={}&count={}&after={}'.format(
            'https://www.reddit.com',
            subreddit,
            sort_order,
            post_limit,
            word_count,
            after if after else ''
        ),
        headers=api_headers,
        allow_redirects=False
    )
    if not word_histogram:
        normalized_word_list = list(map(lambda word: word.lower(), word_list))
        word_histogram = list(map(lambda word: (word, 0), normalized_word_list))
    if response.status_code == 200:
        data = response.json()['data']
        posts = data['children']
        titles = list(map(lambda post: post['data']['title'], posts))
        word_histogram = list(map(
            lambda kv: (kv[0], kv[1] + sum(list(map(
                lambda txt: txt.lower().split().count(kv[0]),
                titles
            )))),
            word_histogram
        ))
        if len(posts) >= post_limit and data['after']:
            count_words(
                subreddit,
                word_list,
                word_histogram,
                word_count + len(posts),
                data['after']
            )
        else:
            sort_histogram(word_histogram)
    else:
        return
