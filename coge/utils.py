def printstatement(text):
    print(text)


def response_is_valid(status_code):
    if status_code == 200:
        return True


def report_invalid_response(response):
    print("INVALID RESPONSE: %s" % str(response.status_code))
    print(response.text)
    return False