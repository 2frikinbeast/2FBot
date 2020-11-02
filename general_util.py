from datetime import datetime

import Levenshtein


def current_time():
    return datetime.utcnow()


def list_to_linebroken_string(string_list):
    output = ""
    for item in string_list:
        output += (item + "\n")
    return output


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:(-1 * len(suffix))]
    return text


def most_similar_string(query, search_list):
    similarity_min = 10000
    output = ""
    for item in search_list:
        if Levenshtein.distance(query, item) < similarity_min:
            similarity_min = Levenshtein.distance(query, item)
            output = item
    return output
