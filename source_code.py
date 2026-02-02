import re
import json

#My Regexes for different data types
patterns = {
    "email": r"(?!.*[\r\n])(?=.{5,255}$)\w[\w.-]{0,63}@[\w.-]{1,192}\.[a-zA-Z]{2,63}",
    "phone": r"(?!.*[\r\n])(?=.{16}$)\+237\s[623]\d{2}-\d{3}-\d{3}",
    "credit_card": r"(\d{4})-\d{4}-\d{4}-(\d{4})",
    "time": r"([01]\d|2[0-3]):[0-5]\d",
    "currency": r"\$\d{1,3}(,\d{3})*\.\d{2}"
}

#Getting the input data
with open('input.txt', 'r') as file:
    data = file.read()

results = {}

# Data Extraction and Validation
for label, regex in patterns.items():
    # findall() gets all matches from the messy text
    matches = re.findall(regex, data)
    results[label] = matches

#print output in a JSON format
print(json.dumps(results, indent=4))