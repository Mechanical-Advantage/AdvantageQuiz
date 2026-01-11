#!/usr/bin/env python3
"""
FRC 6328 Quiz Question Obfuscator/Deobfuscator
A command-line tool to encode and decode quiz questions for the FRC quiz app.

Usage:
    # Encode questions from JSON file
    python quiz-tool.py encode questions.json -o encoded.txt
    
    # Decode questions to JSON file
    python quiz-tool.py decode encoded.txt -o questions.json
    
    # Update HTML file with new encoded questions
    python quiz-tool.py update questions.json quiz.html
    
    # Interactive mode
    python quiz-tool.py interactive
"""

import argparse
import base64
import json
import sys
import os
import re
from typing import Optional

# Default XOR encryption key (same as used in quiz apps)
DEFAULT_KEY = "T0ssIHlvdSBhcmUgdHJ5aW5nIGhhcmQ="


class QuizObfuscator:
    """Handles encoding and decoding of quiz questions."""
    
    def __init__(self, key: str = DEFAULT_KEY):
        """Initialize with encryption key."""
        self.key = key
    
    def xor_encrypt(self, data: str) -> bytes:
        """XOR encrypt data with key."""
        key_bytes = self.key.encode()
        data_bytes = data.encode()
        encrypted = bytearray()
        
        for i, byte in enumerate(data_bytes):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return bytes(encrypted)
    
    def xor_decrypt(self, data: bytes) -> str:
        """XOR decrypt data with key."""
        key_bytes = self.key.encode()
        decrypted = bytearray()
        
        for i, byte in enumerate(data):
            decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return decrypted.decode('utf-8')
    
    def encode(self, questions: list) -> str:
        """Encode questions list to obfuscated base64 string."""
        json_str = json.dumps(questions, indent=2)
        encrypted = self.xor_encrypt(json_str)
        encoded = base64.b64encode(encrypted).decode('utf-8')
        return encoded
    
    def decode(self, encoded_str: str) -> list:
        """Decode obfuscated base64 string to questions list."""
        encrypted = base64.b64decode(encoded_str)
        json_str = self.xor_decrypt(encrypted)
        questions = json.loads(json_str)
        return questions


def load_json_file(filepath: str) -> list:
    """Load questions from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in '{filepath}': {e}")
        sys.exit(1)


def save_json_file(filepath: str, questions: list):
    """Save questions to JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        print(f"✅ Questions saved to: {filepath}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)


def load_text_file(filepath: str) -> str:
    """Load encoded string from text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found")
        sys.exit(1)


def save_text_file(filepath: str, content: str):
    """Save encoded string to text file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Encoded data saved to: {filepath}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)


def update_html_file(html_path: str, encoded_data: str) -> bool:
    """Update HTML file with new encoded data."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Find and replace encoded data
        pattern = r'const encodedData = "(.*?)";'
        match = re.search(pattern, html_content)
        
        if not match:
            print(f"❌ Error: Could not find 'const encodedData' in {html_path}")
            return False
        
        # Replace the encoded data
        new_html = re.sub(pattern, f'const encodedData = "{encoded_data}";', html_content, count=1)
        
        # Write back
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"✅ HTML file updated: {html_path}")
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File '{html_path}' not found")
        return False
    except Exception as e:
        print(f"❌ Error updating HTML: {e}")
        return False


def print_quiz_info(questions: list):
    """Print information about quiz questions."""
    total = len(questions)
    
    # Count by category
    categories = {}
    for q in questions:
        cat = q.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📊 Quiz Information:")
    print(f"   Total Questions: {total}")
    print(f"   Categories:")
    for cat, count in sorted(categories.items()):
        print(f"      • {cat}: {count} questions")


def cmd_encode(args):
    """Handle encode command."""
    obfuscator = QuizObfuscator(args.key)
    
    # Load questions
    print(f"📖 Loading questions from: {args.input}")
    questions = load_json_file(args.input)
    
    # Print info
    print_quiz_info(questions)
    
    # Encode
    print(f"\n🔒 Encoding questions...")
    encoded = obfuscator.encode(questions)
    
    # Save or print
    if args.output:
        save_text_file(args.output, encoded)
    else:
        print(f"\n📝 Encoded data ({len(encoded)} characters):")
        print(encoded)
    
    print(f"\n✨ Encoding complete!")


def cmd_decode(args):
    """Handle decode command."""
    obfuscator = QuizObfuscator(args.key)
    
    # Load encoded data
    print(f"📖 Loading encoded data from: {args.input}")
    encoded = load_text_file(args.input)
    
    # Decode
    print(f"🔓 Decoding questions...")
    try:
        questions = obfuscator.decode(encoded)
    except Exception as e:
        print(f"❌ Error decoding: {e}")
        sys.exit(1)
    
    # Print info
    print_quiz_info(questions)
    
    # Save or print
    if args.output:
        save_json_file(args.output, questions)
    else:
        print(f"\n📝 Decoded questions:")
        print(json.dumps(questions, indent=2))
    
    print(f"\n✨ Decoding complete!")


def cmd_update(args):
    """Handle update command."""
    obfuscator = QuizObfuscator(args.key)
    
    # Load questions
    print(f"📖 Loading questions from: {args.questions}")
    questions = load_json_file(args.questions)
    
    # Print info
    print_quiz_info(questions)
    
    # Encode
    print(f"\n🔒 Encoding questions...")
    encoded = obfuscator.encode(questions)
    print(f"   Encoded size: {len(encoded)} characters")
    
    # Update HTML
    print(f"\n📝 Updating HTML file: {args.html}")
    if update_html_file(args.html, encoded):
        print(f"\n✨ Update complete!")
    else:
        sys.exit(1)


def cmd_interactive(args):
    """Handle interactive mode."""
    obfuscator = QuizObfuscator(args.key)
    
    print("=" * 60)
    print("FRC 6328 Quiz Tool - Interactive Mode")
    print("=" * 60)
    
    while True:
        print("\nWhat would you like to do?")
        print("  1. Encode questions (JSON → Base64)")
        print("  2. Decode questions (Base64 → JSON)")
        print("  3. Update HTML file")
        print("  4. Validate JSON file")
        print("  5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            # Encode
            json_file = input("Enter JSON file path: ").strip()
            if not os.path.exists(json_file):
                print(f"❌ File not found: {json_file}")
                continue
            
            questions = load_json_file(json_file)
            print_quiz_info(questions)
            
            encoded = obfuscator.encode(questions)
            
            save_choice = input("\nSave to file? (y/n): ").strip().lower()
            if save_choice == 'y':
                output_file = input("Enter output file path: ").strip()
                save_text_file(output_file, encoded)
            else:
                print(f"\n📝 Encoded data:\n{encoded}")
        
        elif choice == '2':
            # Decode
            encoded_file = input("Enter encoded file path: ").strip()
            if not os.path.exists(encoded_file):
                print(f"❌ File not found: {encoded_file}")
                continue
            
            encoded = load_text_file(encoded_file)
            
            try:
                questions = obfuscator.decode(encoded)
                print_quiz_info(questions)
                
                save_choice = input("\nSave to file? (y/n): ").strip().lower()
                if save_choice == 'y':
                    output_file = input("Enter output JSON file path: ").strip()
                    save_json_file(output_file, questions)
                else:
                    print(f"\n📝 First question preview:")
                    print(json.dumps(questions[0], indent=2))
            except Exception as e:
                print(f"❌ Error decoding: {e}")
        
        elif choice == '3':
            # Update HTML
            json_file = input("Enter JSON file path: ").strip()
            html_file = input("Enter HTML file path: ").strip()
            
            if not os.path.exists(json_file):
                print(f"❌ File not found: {json_file}")
                continue
            if not os.path.exists(html_file):
                print(f"❌ File not found: {html_file}")
                continue
            
            questions = load_json_file(json_file)
            print_quiz_info(questions)
            
            encoded = obfuscator.encode(questions)
            update_html_file(html_file, encoded)
        
        elif choice == '4':
            # Validate
            json_file = input("Enter JSON file path: ").strip()
            if not os.path.exists(json_file):
                print(f"❌ File not found: {json_file}")
                continue
            
            try:
                questions = load_json_file(json_file)
                print_quiz_info(questions)
                
                # Basic validation
                issues = []
                for i, q in enumerate(questions):
                    if 'question' not in q:
                        issues.append(f"Question {i+1}: Missing 'question' field")
                    if 'options' not in q:
                        issues.append(f"Question {i+1}: Missing 'options' field")
                    if 'correct' not in q:
                        issues.append(f"Question {i+1}: Missing 'correct' field")
                
                if issues:
                    print(f"\n⚠️  Found {len(issues)} issues:")
                    for issue in issues:
                        print(f"   • {issue}")
                else:
                    print(f"\n✅ All questions valid!")
                
            except Exception as e:
                print(f"❌ Error validating: {e}")
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='FRC 6328 Quiz Question Obfuscator/Deobfuscator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encode questions
  %(prog)s encode questions.json -o encoded.txt
  
  # Decode questions
  %(prog)s decode encoded.txt -o questions.json
  
  # Update HTML file
  %(prog)s update questions.json quiz.html
  
  # Interactive mode
  %(prog)s interactive
        """
    )
    
    parser.add_argument(
        '--key',
        default=DEFAULT_KEY,
        help='Custom XOR encryption key (default: built-in key)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode questions to obfuscated string')
    encode_parser.add_argument('input', help='Input JSON file with questions')
    encode_parser.add_argument('-o', '--output', help='Output file for encoded data (optional)')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode obfuscated string to questions')
    decode_parser.add_argument('input', help='Input file with encoded data')
    decode_parser.add_argument('-o', '--output', help='Output JSON file for questions (optional)')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update HTML file with encoded questions')
    update_parser.add_argument('questions', help='JSON file with questions')
    update_parser.add_argument('html', help='HTML file to update')
    
    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Interactive mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == 'encode':
        cmd_encode(args)
    elif args.command == 'decode':
        cmd_decode(args)
    elif args.command == 'update':
        cmd_update(args)
    elif args.command == 'interactive':
        cmd_interactive(args)


if __name__ == '__main__':
    main()
