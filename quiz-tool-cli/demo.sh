#!/bin/bash
# FRC 6328 Quiz Tool - Quick Start Demo
# This script demonstrates common usage patterns

echo "=========================================="
echo "FRC 6328 Quiz Tool - Demo"
echo "=========================================="
echo ""

# 1. Show help
echo "1. Viewing help:"
echo "   $ python3 quiz-tool.py --help"
echo ""
python3 quiz-tool.py --help
echo ""
read -p "Press Enter to continue..."

# 2. Encode questions
echo ""
echo "=========================================="
echo "2. Encoding Questions"
echo "=========================================="
echo "   $ python3 quiz-tool.py encode sample-questions.json -o encoded.txt"
echo ""
python3 quiz-tool.py encode sample-questions.json -o encoded.txt
echo ""
read -p "Press Enter to continue..."

# 3. Show encoded data
echo ""
echo "=========================================="
echo "3. Viewing Encoded Data"
echo "=========================================="
echo "   $ cat encoded.txt"
echo ""
head -c 200 encoded.txt
echo "..."
echo ""
echo "(Showing first 200 characters)"
echo ""
read -p "Press Enter to continue..."

# 4. Decode questions
echo ""
echo "=========================================="
echo "4. Decoding Questions"
echo "=========================================="
echo "   $ python3 quiz-tool.py decode encoded.txt -o decoded.json"
echo ""
python3 quiz-tool.py decode encoded.txt -o decoded.json
echo ""
read -p "Press Enter to continue..."

# 5. Compare files
echo ""
echo "=========================================="
echo "5. Verifying Round-Trip"
echo "=========================================="
echo "   Comparing sample-questions.json with decoded.json"
echo ""
if diff -q sample-questions.json decoded.json > /dev/null; then
    echo "   ✅ Files are identical! Encoding/decoding works perfectly."
else
    echo "   ⚠️  Files differ (might be formatting)"
fi
echo ""
read -p "Press Enter to continue..."

# 6. Show workflow
echo ""
echo "=========================================="
echo "6. Typical Workflow"
echo "=========================================="
cat << 'EOF'

STUDENT WORKFLOW FOR EDITING QUESTIONS:

Step 1: Get current questions
   $ python3 quiz-tool.py decode encoded.txt -o questions.json

Step 2: Edit questions
   $ nano questions.json
   (or use your favorite editor)

Step 3: Update quiz HTML
   $ python3 quiz-tool.py update questions.json quiz.html

Step 4: Test in browser
   $ open quiz.html

That's it! Your changes are now in the quiz.

EOF
echo ""
read -p "Press Enter to continue..."

# 7. Interactive mode
echo ""
echo "=========================================="
echo "7. Interactive Mode"
echo "=========================================="
echo "   For a menu-driven experience, use:"
echo "   $ python3 quiz-tool.py interactive"
echo ""
echo "   Try it yourself!"
echo ""

# Cleanup
echo "=========================================="
echo "Demo Complete!"
echo "=========================================="
echo ""
echo "Generated files:"
echo "  • encoded.txt - Obfuscated questions"
echo "  • decoded.json - Round-trip decoded questions"
echo ""
echo "Clean up demo files:"
echo "  $ rm encoded.txt decoded.json"
echo ""
