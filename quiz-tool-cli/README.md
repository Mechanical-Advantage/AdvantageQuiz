# FRC 6328 Quiz Tool

A command-line tool for encoding and decoding quiz questions for the FRC 6328 quiz application.

## Features

- ✅ **Encode** JSON questions to obfuscated Base64 strings
- ✅ **Decode** obfuscated strings back to JSON
- ✅ **Update** HTML quiz files automatically
- ✅ **Validate** question JSON structure
- ✅ **Interactive mode** for easy workflow
- ✅ Built-in XOR encryption with Base64 encoding

## Installation

No installation required! Just Python 3.6+

```bash
# Make executable (optional)
chmod +x quiz-tool.py
```

## Quick Start

### 1. Edit Questions

Create or edit a JSON file with your questions:

```json
[
  {
    "id": 1,
    "question": "What is the robot weight limit?",
    "options": ["90 kg", "125 lb", "115 lb", "120 lb"],
    "correct": 2,
    "explanation": "The robot weight limit is 115 lbs.",
    "category": "Robot",
    "citation": {
      "rule": "R103",
      "section": "Section 8",
      "excerpt": "R103: The ROBOT weight must not exceed 115.0lb..."
    }
  }
]
```

### 2. Encode Questions

```bash
# Encode to file
python quiz-tool.py encode questions.json -o encoded.txt

# Or print to console
python quiz-tool.py encode questions.json
```

### 3. Update HTML

```bash
# Update quiz HTML file directly
python quiz-tool.py update questions.json quiz-student-team.html
```

## Command Reference

### Encode Command

Convert JSON questions to obfuscated Base64 string.

```bash
python quiz-tool.py encode <input.json> [-o output.txt]
```

**Examples:**
```bash
# Save to file
python quiz-tool.py encode questions.json -o encoded.txt

# Print to console
python quiz-tool.py encode questions.json
```

### Decode Command

Convert obfuscated Base64 string back to JSON.

```bash
python quiz-tool.py decode <input.txt> [-o output.json]
```

**Examples:**
```bash
# Save to file
python quiz-tool.py decode encoded.txt -o questions.json

# Print to console
python quiz-tool.py decode encoded.txt
```

### Update Command

Update HTML quiz file with new encoded questions.

```bash
python quiz-tool.py update <questions.json> <quiz.html>
```

**Example:**
```bash
python quiz-tool.py update student-questions.json quiz-student-team.html
```

**What it does:**
1. Loads questions from JSON
2. Encodes them
3. Finds `const encodedData = "..."` in HTML
4. Replaces with new encoded data
5. Saves updated HTML

### Interactive Mode

Launch interactive menu for all operations.

```bash
python quiz-tool.py interactive
```

**Menu options:**
1. Encode questions (JSON → Base64)
2. Decode questions (Base64 → JSON)
3. Update HTML file
4. Validate JSON file
5. Exit

## JSON Question Format

Each question must have these fields:

```json
{
  "id": 1,                          // Required: Unique question ID
  "question": "Question text?",     // Required: The question
  "options": ["A", "B", "C", "D"],  // Required: Answer options
  "correct": 2,                     // Required: Correct answer index (0-based)
  "explanation": "Why it's right",  // Required: Explanation
  "category": "Robot",              // Required: Category name
  "citation": {                     // Optional: Rule citation
    "rule": "R103",
    "section": "Section 8",
    "excerpt": "Rule text..."
  }
}
```

### Categories

Standard categories used in FRC 6328 quizzes:
- `Robot` - Robot construction rules
- `Field` - Field elements and zones
- `Matchplay` - Game timing and scoring
- `Game Pieces` - FUEL and other game elements

## Workflow Examples

### Creating a New Quiz

```bash
# 1. Create questions.json
nano questions.json

# 2. Validate (optional)
python quiz-tool.py interactive
# Choose option 4, enter filename

# 3. Update HTML
python quiz-tool.py update questions.json quiz.html

# Done! Test your quiz
```

### Editing Existing Quiz

```bash
# 1. Extract current questions from HTML
# Find the encoded data in quiz.html between quotes
# Save to encoded.txt

# 2. Decode to JSON
python quiz-tool.py decode encoded.txt -o questions.json

# 3. Edit questions.json
nano questions.json

# 4. Update HTML
python quiz-tool.py update questions.json quiz.html
```

### Batch Processing Multiple Quizzes

```bash
# Update all quiz files
python quiz-tool.py update questions-2024-2025.json quiz-2024-2025.html
python quiz-tool.py update questions-2025-2026.json quiz-2025-2026.html
python quiz-tool.py update questions-2026-game.json quiz-2026-game.html
python quiz-tool.py update questions-student.json quiz-student-team.html
```

## Advanced Usage

### Custom Encryption Key

Use a different XOR key:

```bash
python quiz-tool.py --key "MyCustomKey123" encode questions.json
```

**Note:** You'll need to update the JavaScript in the HTML to use the same key!

### Piping and Scripting

```bash
# Chain commands
python quiz-tool.py encode questions.json | grep "Encoded size"

# Use in scripts
#!/bin/bash
for file in questions-*.json; do
  html="${file/questions-/quiz-}"
  html="${html/.json/.html}"
  python quiz-tool.py update "$file" "$html"
done
```

## Troubleshooting

### "File not found" Error
- Check file path is correct
- Use absolute paths if needed: `/full/path/to/file.json`

### "Invalid JSON" Error
- Validate JSON syntax: https://jsonlint.com
- Check all commas, brackets, quotes
- Ensure no trailing commas

### "Could not find 'const encodedData'" Error
- HTML file must contain: `const encodedData = "...";`
- Check the variable name matches exactly
- Ensure it's in a `<script>` tag

### Decode Fails
- Verify you're using the same encryption key
- Check the encoded data wasn't corrupted
- Ensure complete Base64 string (no truncation)

## Tips & Best Practices

### Version Control
```bash
# Keep JSON in git, not encoded data
git add questions.json
git commit -m "Updated question 5 explanation"

# Regenerate encoded data from JSON
python quiz-tool.py update questions.json quiz.html
```

### Backup Before Updates
```bash
# Backup HTML before updating
cp quiz.html quiz.html.backup
python quiz-tool.py update questions.json quiz.html
```

### Question ID Management
- Keep IDs sequential: 1, 2, 3...
- Don't skip numbers
- When removing questions, renumber remaining ones

### Testing Changes
1. Update questions.json
2. Run update command
3. Open HTML in browser
4. Test affected questions
5. Check scoring logic works

## File Structure

```
project/
├── quiz-tool.py              # This tool
├── sample-questions.json     # Example questions
├── questions-*.json          # Your question files
├── quiz-*.html               # Quiz HTML files
└── README.md                 # This file
```

## Development

### How It Works

1. **Encoding:**
   - JSON → String
   - XOR encrypt with key
   - Base64 encode
   - Result: obfuscated string

2. **Decoding:**
   - Base64 decode
   - XOR decrypt with key
   - Parse JSON
   - Result: questions array

3. **HTML Update:**
   - Regex find: `const encodedData = "...";`
   - Replace with new encoded data
   - Save file

### Security Note

This is **obfuscation**, not encryption! The XOR key is visible in the JavaScript. This prevents casual viewing of questions but is not secure against determined attackers. For student quizzes, this level of obfuscation is appropriate.

## Credits

Created for **FRC Team 6328 - Mechanical Advantage**

2026 REBUILT Season

## License

MIT License - Free to use and modify

---

**Questions?** Open an issue or ask on the team Slack!
