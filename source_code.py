import re
import json

#Regexes

validators = {
    "email": r"^(?!.*[\r\n])(?!.*[<>])(?=.{5,255}$)\w[\w.-]{0,63}@[\w.-]{1,192}\.[a-zA-Z]{2,63}$",
    "phone": r"^(?!.*[\r\n])(?!.*[<>])(?=.{16}$)\+237\s[623]\d{2}-\d{3}-\d{3}$",
    "credit_card": r"^(?!.*[\r\n])(?!.*[<>])(?=.{19}$)(\d{4})-\d{4}-\d{4}-(\d{4})$",
    "time": r"^(?!.*[\r\n])(?!.*[<>])(?=.{5}$)([01]\d|2[0-3]):[0-5]\d$",
    "currency": r"^(?!.*[\r\n])(?!.*[<>])(?=.{4,15}$)\$\d{1,3}(,\d{3})*\.\d{2}$"
}

# This dictionary will store our clean data
extracted_results = {
    "email": [],
    "phone": [],
    "credit_card": [],
    "time": [],
    "currency": []
}

# 2. OPEN AND READ THE FILE LINE-BY-LINE
with open('input.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    clean_line = line.strip() # Removes invisible spaces and \n
    
    if not clean_line:
        continue # Skip empty lines

    # 3. THE LOOP: CHECK EVERY LINE AGAINST EVERY REGEX
    for category, pattern in validators.items():
        if re.match(pattern, clean_line):
            
            # Mask the Credit Card for privacy
            if category == "credit_card":
                masked_card = re.sub(pattern, r"\1-****-****-\2", clean_line)
                extracted_results[category].append(masked_card)
            else:
                extracted_results[category].append(clean_line)
            
            break # Move to next line once we find a match

# 4. SAVE TO JSON
with open('sample_output.json', 'w') as f:
    json.dump(extracted_results, f, indent=4)

print("Mission Accomplished! Your secured data is in sample_output.json")