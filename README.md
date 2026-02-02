ALU Regex Data Extraction Tool
What this project does
I built this program to solve the problem of extracting specific, sensitive data from messy, real-world text files. It doesn't just "find" strings; it validates them against strict business rules and security standards.

The script scans an input file (sample_input.txt) and harvests five types of data:

Emails (University/Standard formats)

Cameroonian Phone Numbers (Specific +237 formatting)

Credit Card Numbers (With automatic masking for privacy)

24-Hour Time (Logical HH:MM format)

Currency (USD format with thousands separators)

How to use it
Place your raw text in a file named sample_input.txt in the same folder as the script.

Run the script:

Bash
python main.py
The program will generate a sample_output.json file containing all the valid data it found, organized by category.

The Logic Behind the Validation
I chose a two-stage validation approach because real-world data is often "dirty" or malicious.

1. Extraction vs. Validation
Instead of just grabbing anything that looks like a number or email, the program uses a "Greedy" regex approach. It finds a potential match and then hands it over to a Python Security Guard. This guard checks two things:

Sanitization: It looks for hidden "Injection" characters like < > or newlines (\n). If someone tries to attach a <script> tag to a phone number, the program detects it and blocks it.

Manual Length Check: Since data is often buried in long sentences, I check the length of the extracted data only. This prevents the program from getting confused by the length of the surrounding paragraph.

2. Why use finditer?
I used re.finditer because it allows the program to scan a single line and find multiple occurrences of the same data type. If a paragraph has three different emails, this tool catches all of them instead of stopping at the first one.

3. Privacy & Masking
For the Credit Card module, I implemented PII (Personally Identifiable Information) masking. Using regex capturing groups, the script identifies the full number but replaces the middle 8 digits with stars before saving. This ensures that even if the output file is stolen, the sensitive financial data remains protected.




Regex Pattern Breakdown
To keep the system secure, I used specific regex "formulas" for each data type. Here is the logic for each:

1. Email
r"\w[\w.-]{0,63}@[\w.-]{1,192}\.[a-zA-Z]{2,63}"

The Logic: It starts with a word character, allows dots and hyphens in the name and domain, and requires a TLD (like .com or .edu) that is at least 2 characters long.


2. Cameroonian Phone Number
r"\+237\s[623]\d{2}-\d{3}-\d{3}"

The Logic: This follows the specific format for Cameroon. It must start with the +237 country code and a space.

Service Codes: The first digit of the number must be a 6 (Mobile), 2 (Fixed line), or 3 (Nexttel/Fixed). This prevents fake numbers from being collected.

3. Credit Card (with Masking)
r"(\d{4})-\d{4}-\d{4}-(\d{4})"

The Logic: It looks for four groups of four digits separated by hyphens.

Capturing Groups: I wrapped the first (\d{4}) and last (\d{4}) in parentheses. This allows the program to "remember" those specific numbers while replacing the middle ones with **** during the masking phase.

4. 24-Hour Time
r"([01]\d|2[0-3]):[0-5]\d\S*"

The Logic: This uses "Alternation" logic.

[01]\d handles hours from 00 to 19.

2[0-3] handles hours from 20 to 23.

Security: This pattern makes it mathematically impossible to match a time like 25:70.

5. Currency (USD)
r"\$\d{1,3}(,\d{3})*\.\d{2}"

The Logic: * \d{1,3} handles the first one-to-three digits.

(,\d{3})* handles thousands separators (commas followed by exactly three digits).

\.\d{2} requires exactly two decimal places for cents.

Security Considerations
The primary threat this program defends against is Injection Attacks.

XSS (Cross-Site Scripting): By searching for < and > in the extracted data, we ensure that a hacker cannot hide an executable script inside a data field.

Log/Header Injection: The check for \n (newlines) prevents an attacker from "splitting" a line of data to inject fake log entries or unauthorized commands into a server.