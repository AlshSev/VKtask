import json

# Delimeter Separated Values
def dsv_formatter(data, omit_header=False, delimeter=','):
    result = []
    if not omit_header:
        result.append(delimeter.join(["first_name", "last_name", 
                                      "country", "city", 
                                      "birthday", "sex"]))

    for friend in data:
        result.append(delimeter.join([friend.fname, friend.lname, 
                                      friend.country, friend.city, 
                                      friend.bdate, friend.sex]))

    return "\n".join(result)

def csv_formatter(data, omit_header=False):
    return dsv_formatter(data, omit_header, ',')

def tsv_formatter(data, omit_header=False):
    return dsv_formatter(data, omit_header, '\t')

# Can also pass kwargs to json.dump
def json_formatter(data, omit_outer_key=False, **dump_kwargs):
    # Puts everything in a list, but uses variable true_result to dump
    # everything. Made that way to make it easy to include/exclude
    # outer key "friends"
    result = [];
    if not omit_outer_key:
        true_result = {"friends" : result}
    else:
        true_result = result

    for friend in data:
        result.append({
            "first_name" : friend.fname,
            "last_name" : friend.lname, 
            "country" : friend.country, 
            "city" : friend.city, 
            "birthday" : friend.bdate, 
            "sex" : friend.sex,
        })

    return json.dumps(true_result, **dump_kwargs)

def get_formatter_by_ext(ext):
    if ext == "CSV":
        return csv_formatter
    elif ext == "TSV":
        return tsv_formatter
    elif ext == "JSON":
        return json_formatter
    else:
        raise Exception("Invalid format specified")

def dump_friends(data, filename="report", 
                 formatter=csv_formatter, **formatter_kwargs):
    text = formatter(data, **formatter_kwargs)
    with open(filename, 'w', encoding="utf-8") as report:
        report.write(text)
