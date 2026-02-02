import re
import json

#Regexes
validators = {
    "email": r"\w[\w.-]{0,63}@[\w.-]{1,192}\.[a-zA-Z]{2,63}",
    "phone": r"\+237\s[623]\d{2}-\d{3}-\d{3}",
    "credit_card": r"(\d{4})-\d{4}-\d{4}-(\d{4})",
    "time": r"([01]\d|2[0-3]):[0-5]\d",
    "currency": r"\$\d{1,3}(,\d{3})*\.\d{2}"
}

# This dictionary will store our clean data
extracted_results = {
    "email": [],
    "phone": [],
    "credit_card": [],
    "time": [],
    "currency": []
}

# 2. OPEN AND READ THE FILE
with open('sample_input.txt', 'r') as file:
    lines = file.readlines()

#sorting our regex patterns from the messed up data
for line in lines:
    clean_line = line.strip()
    if not clean_line:
        continue

    # Loop through each category/regex pair
    for category, pattern in validators.items():
       
        matches = re.finditer(pattern, clean_line)
        
        for match in matches:
            found_data = match.group(0)
            
            # --- THE SECURITY GATEKEEPER ---
            
            # Check 1: No malicious characters (XSS or Newlines)
            is_safe = not re.search(r"[\r\n<>]", found_data)
            
            # Check 2: Manual Length Validation for each category
            length_ok = False
            data_len = len(found_data)
            
            if category == "email": 
                length_ok = 5 <= data_len <= 255
            elif category == "phone": 
                length_ok = data_len == 16
            elif category == "credit_card": 
                length_ok = data_len == 19
            elif category == "time": 
                length_ok = data_len == 5
            elif category == "currency": 
                length_ok = 4 <= data_len <= 15

            # If it passes Security Checks, we save it!
            if is_safe and length_ok:
                if category == "credit_card":
                    # Mask the card for privacy
                    masked = re.sub(pattern, r"\1-****-****-\2", found_data)
                    extracted_results[category].append(masked)
                else:
                    extracted_results[category].append(found_data)
            else:
                print(f"Blocked potential threat or invalid data: {found_data}")

# 4. SAVE TO JSON
with open('sample_output.json', 'w') as f:
    json.dump(extracted_results, f, indent=4)

print("\n--- Processing Complete ---")
print("All valid, secure data has been harvested into sample_output.json")