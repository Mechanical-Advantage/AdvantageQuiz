# Quiz Tool Usage Examples

## Real-World Scenarios

### Scenario 1: Student Wants to Fix a Typo

**Problem:** Question 15 has "TELEOP" spelled as "TELOP"

**Solution:**
```bash
# 1. Extract current questions
python3 quiz-tool.py decode encoded-data.txt -o questions.json

# 2. Edit the file
nano questions.json
# Find question with id: 15, fix typo

# 3. Update the HTML
python3 quiz-tool.py update questions.json quiz-student-team.html

# 4. Test it
open quiz-student-team.html
```

---

### Scenario 2: Adding a New Question

**Problem:** Need to add a new question about FUEL diameter

**Solution:**
```bash
# 1. Get current questions
python3 quiz-tool.py decode current.txt -o questions.json

# 2. Edit questions.json, add new question:
```
```json
{
  "id": 41,
  "question": "What is the diameter of FUEL in inches?",
  "options": ["5.91 inches", "6.0 inches", "5.5 inches", "15 cm"],
  "correct": 0,
  "explanation": "FUEL is 5.91 inches (15 cm) in diameter.",
  "category": "Game Pieces",
  "citation": {
    "rule": "N/A",
    "section": "Section 5.10.1: FUEL",
    "excerpt": "A FUEL is a 5.91in (15.0cm) diameter, high density foam ball."
  }
}
```
```bash
# 3. Update HTML
python3 quiz-tool.py update questions.json quiz-student-team.html
```

---

### Scenario 3: Removing Question 32

**Problem:** Question 32 is confusing and needs to be removed

**Solution:**
```bash
# 1. Decode questions
python3 quiz-tool.py decode quiz-data.txt -o questions.json

# 2. Edit questions.json
# - Remove the question object with "id": 32
# - Renumber all subsequent questions (33→32, 34→33, etc.)

# 3. Update the HTML
python3 quiz-tool.py update questions.json quiz.html

# 4. Update landing page stats if needed
# Open index.html and change "40 questions" to "39 questions"
```

---

### Scenario 4: Changing Correct Answer

**Problem:** Question 14's correct answer should be option 0, not option 1

**Solution:**
```bash
# 1. Interactive mode is easiest for this
python3 quiz-tool.py interactive

# Choose: 2 (Decode questions)
# Enter: encoded.txt
# Choose: y (Save to file)
# Enter: questions.json

# 2. Edit questions.json
# Find question with "id": 14
# Change "correct": 1 to "correct": 0

# 3. Back to interactive mode
python3 quiz-tool.py interactive

# Choose: 3 (Update HTML file)
# Enter: questions.json
# Enter: quiz.html
```

---

### Scenario 5: Updating Multiple Quizzes at Once

**Problem:** Fixed a citation format, need to update all 4 quizzes

**Solution:**
```bash
# Create a script: update-all.sh
cat > update-all.sh << 'EOF'
#!/bin/bash

echo "Updating all quizzes..."

python3 quiz-tool.py update questions-2024-2025.json quiz-2024-2025.html
python3 quiz-tool.py update questions-2025-2026.json quiz-2025-2026.html  
python3 quiz-tool.py update questions-2026-game.json quiz-2026-game.html
python3 quiz-tool.py update questions-student-team.json quiz-student-team.html

echo "All quizzes updated!"
EOF

chmod +x update-all.sh
./update-all.sh
```

---

### Scenario 6: Validating Before Committing

**Problem:** Want to make sure JSON is valid before pushing to git

**Solution:**
```bash
# Use interactive mode validation
python3 quiz-tool.py interactive

# Choose: 4 (Validate JSON file)
# Enter: questions.json

# Output will show:
# ✅ All questions valid!
# or
# ⚠️ Found 2 issues:
#   • Question 5: Missing 'correct' field
#   • Question 10: Missing 'options' field
```

---

### Scenario 7: Creating a Brand New Quiz

**Problem:** Starting from scratch for a new season

**Solution:**
```bash
# 1. Create questions file
cat > new-quiz-questions.json << 'EOF'
[
  {
    "id": 1,
    "question": "First question here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0,
    "explanation": "Explanation here",
    "category": "Category Name",
    "citation": {
      "rule": "R001",
      "section": "Section 1",
      "excerpt": "Rule text..."
    }
  }
]
EOF

# 2. Add more questions...
nano new-quiz-questions.json

# 3. Validate
python3 quiz-tool.py interactive
# Choose option 4, validate

# 4. Copy an existing quiz HTML as template
cp quiz-student-team.html quiz-new.html

# 5. Update with your questions
python3 quiz-tool.py update new-quiz-questions.json quiz-new.html

# 6. Edit quiz-new.html metadata:
# - Change title
# - Change description
# - Update any team branding
```

---

### Scenario 8: Extracting Questions from HTML

**Problem:** Someone only has the HTML file, needs to edit questions

**Solution:**
```bash
# 1. Open HTML file and find the encoded data
# Look for: const encodedData = "...very long string...";
# Copy everything between the quotes

# 2. Save to a text file
cat > extracted.txt << 'EOF'
[paste the long encoded string here]
EOF

# 3. Decode
python3 quiz-tool.py decode extracted.txt -o questions.json

# 4. Now you can edit questions.json
```

---

### Scenario 9: Comparing Two Versions

**Problem:** Want to see what changed between old and new versions

**Solution:**
```bash
# 1. Decode both versions
python3 quiz-tool.py decode old-encoded.txt -o old-questions.json
python3 quiz-tool.py decode new-encoded.txt -o new-questions.json

# 2. Use diff
diff old-questions.json new-questions.json

# 3. Or use a visual diff tool
code --diff old-questions.json new-questions.json  # VSCode
```

---

### Scenario 10: Batch Converting from Google Forms

**Problem:** Have 40 questions in Google Forms CSV, need to convert

**Solution:**
```python
# Create convert.py
import csv
import json

questions = []
with open('google-forms-export.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        question = {
            "id": i,
            "question": row['Question'],
            "options": [
                row['Option1'],
                row['Option2'],
                row['Option3'],
                row['Option4']
            ],
            "correct": int(row['CorrectAnswer']),
            "explanation": row['Explanation'],
            "category": row['Category'],
            "citation": {
                "rule": row.get('Rule', 'N/A'),
                "section": row.get('Section', ''),
                "excerpt": row.get('Excerpt', '')
            }
        }
        questions.append(question)

with open('questions.json', 'w') as f:
    json.dump(questions, f, indent=2)

print(f"Converted {len(questions)} questions!")
```
```bash
# Run conversion
python3 convert.py

# Update quiz
python3 quiz-tool.py update questions.json quiz.html
```

---

## Tips and Tricks

### Tip 1: Use Version Control
```bash
# Only track JSON files, regenerate HTML
echo "*.txt" >> .gitignore
echo "quiz-*.html" >> .gitignore

git add questions-*.json
git commit -m "Updated questions"
```

### Tip 2: Pre-commit Hook
```bash
# Create .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Regenerate quiz HTML before committing

for json in questions-*.json; do
    html="${json/questions-/quiz-}"
    html="${html/.json/.html}"
    python3 quiz-tool.py update "$json" "$html"
    git add "$html"
done
EOF

chmod +x .git/hooks/pre-commit
```

### Tip 3: Question ID Auto-numbering
```python
# renumber.py - Automatically fix question IDs
import json
import sys

with open(sys.argv[1], 'r') as f:
    questions = json.load(f)

for i, q in enumerate(questions, 1):
    q['id'] = i

with open(sys.argv[1], 'w') as f:
    json.dump(questions, f, indent=2)

print(f"Renumbered {len(questions)} questions")
```

### Tip 4: Quick Stats
```bash
# Count questions by category
python3 -c "
import json
with open('questions.json') as f:
    qs = json.load(f)
cats = {}
for q in qs:
    cat = q.get('category', 'Unknown')
    cats[cat] = cats.get(cat, 0) + 1
for cat, count in sorted(cats.items()):
    print(f'{cat}: {count}')
"
```

### Tip 5: Find Duplicate IDs
```bash
python3 -c "
import json
with open('questions.json') as f:
    qs = json.load(f)
ids = [q['id'] for q in qs]
dups = [i for i in ids if ids.count(i) > 1]
if dups:
    print(f'Duplicate IDs: {set(dups)}')
else:
    print('No duplicates!')
"
```

---

## Common Errors and Solutions

### Error: "Invalid JSON"
```bash
# Validate JSON syntax
python3 -m json.tool questions.json

# Find the error line
python3 -c "import json; json.load(open('questions.json'))"
```

### Error: "Could not find const encodedData"
```bash
# Check HTML structure
grep -n "const encodedData" quiz.html

# If not found, add it:
# Look for <script> tag and add:
# const encodedData = "";
```

### Error: Decode fails
```bash
# Check if Base64 is valid
python3 -c "
import base64
with open('encoded.txt') as f:
    data = f.read().strip()
try:
    base64.b64decode(data)
    print('Valid Base64')
except:
    print('Invalid Base64')
"
```

---

**Happy Quiz Building! 🚀**
