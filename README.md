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

Sample Console Output
If the program encounters an attack or a logic error (like a time of 25:00), it will log a warning to the console: [SECURITY ALERT] Blocked threat/invalid data: victim@test.com