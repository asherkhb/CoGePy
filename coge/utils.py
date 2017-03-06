def printstatement(text):
    print(text)


def valid_response(status_code):
    if status_code == 200:
        return True
    elif status_code == 201:
        return True
    else:
        return False

def report_invalid_response(response):
    print("INVALID RESPONSE: %s" % str(response.status_code))
    print(response.text)
    return False