#!/usr/bin/env python3

import base64
import re
import binascii
import codecs
from urllib.parse import unquote
import json
import sys

def detect_and_decode(input_text):
    """Analyze the input text and attempt to decode it based on detected encoding."""
    results = []
    
    # Clean the input (remove whitespace if it's not relevant)
    clean_input = input_text.strip()
    
    # Check if input might be ASCII representation of binary (like "30313031...")
    if re.match(r'^[0-9]+$', clean_input) and len(clean_input) % 2 == 0:
        # Try ASCII to binary conversion (e.g., "30" -> "0", "31" -> "1")
        try:
            binary_string = ""
            for i in range(0, len(clean_input), 2):
                pair = clean_input[i:i+2]
                if pair == "30":
                    binary_string += "0"
                elif pair == "31":
                    binary_string += "1"
                else:
                    break
            
            if len(binary_string) > 0 and len(binary_string) % 8 == 0:
                ascii_result = binary_to_ascii(binary_string)
                if is_printable_ascii(ascii_result):
                    results.append({
                        "type": "ASCII representation of binary digits",
                        "decoding": "ASCII digits to binary, then to text",
                        "result": ascii_result
                    })
        except Exception as e:
            pass
    
    # Check if input is binary (consists of only 0s and 1s)
    if re.match(r'^[01]+$', clean_input):
        # If the length is a multiple of 8, it might be ASCII binary
        if len(clean_input) % 8 == 0:
            try:
                ascii_result = binary_to_ascii(clean_input)
                if is_printable_ascii(ascii_result):
                    results.append({
                        "type": "Binary",
                        "decoding": "Binary to ASCII",
                        "result": ascii_result
                    })
            except Exception as e:
                pass
    
    # Check if input is hexadecimal
    if re.match(r'^[0-9A-Fa-f]+$', clean_input) and len(clean_input) % 2 == 0:
        try:
            hex_result = binascii.unhexlify(clean_input).decode('utf-8', errors='ignore')
            if is_printable_ascii(hex_result):
                results.append({
                    "type": "Hexadecimal",
                    "decoding": "Hex to ASCII",
                    "result": hex_result
                })
        except Exception as e:
            pass
    
    # Check if input is Base64
    if re.match(r'^[A-Za-z0-9+/=]+$', clean_input) and len(clean_input) % 4 == 0:
        try:
            base64_result = base64.b64decode(clean_input).decode('utf-8', errors='ignore')
            if is_printable_ascii(base64_result):
                results.append({
                    "type": "Base64",
                    "decoding": "Base64 to ASCII",
                    "result": base64_result
                })
        except Exception as e:
            pass
    
    # Check if input is URL encoded
    if '%' in clean_input:
        try:
            url_decoded = unquote(clean_input)
            if url_decoded != clean_input and is_printable_ascii(url_decoded):
                results.append({
                    "type": "URL Encoding",
                    "decoding": "URL decode",
                    "result": url_decoded
                })
        except Exception as e:
            pass
    
    # Check for ROT13 encoding
    try:
        rot13_result = codecs.decode(clean_input, 'rot13')
        if rot13_result != clean_input and is_printable_ascii(rot13_result):
            results.append({
                "type": "ROT13",
                "decoding": "ROT13 decode",
                "result": rot13_result
            })
    except Exception as e:
        pass
    
    # Check for Morse code (simplified)
    if re.match(r'^[.\- ]+$', clean_input):
        try:
            morse_result = morse_to_text(clean_input)
            if morse_result and is_printable_ascii(morse_result):
                results.append({
                    "type": "Morse Code",
                    "decoding": "Morse to text",
                    "result": morse_result
                })
        except Exception as e:
            pass
    
    # Check for ASCII codes separated by spaces
    if re.match(r'^(\d+ )*\d+$', clean_input):
        try:
            ascii_codes = [int(code) for code in clean_input.split()]
            ascii_result = ''.join(chr(code) for code in ascii_codes)
            if is_printable_ascii(ascii_result):
                results.append({
                    "type": "ASCII Codes",
                    "decoding": "ASCII codes to text",
                    "result": ascii_result
                })
        except Exception as e:
            pass
    
    return results

def binary_to_ascii(binary_string):
    """Convert a binary string to ASCII text."""
    ascii_text = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:  # Ensure we have a full byte
            ascii_text += chr(int(byte, 2))
    return ascii_text

def morse_to_text(morse_code):
    """Convert Morse code to text."""
    morse_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
        '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
        '-----': '0', '.-.-.-': '.', '--..--': ',', '..--..': '?', '.----.': "'",
        '-.-.--': '!', '-..-.': '/', '-.--.': '(', '-.--.-': ')', '.-...': '&',
        '---...': ':', '-.-.-.': ';', '-...-': '=', '.-.-.': '+', '-....-': '-',
        '..--.-': '_', '.-..-.': '"', '...-..-': '$', '.--.-.': '@'
    }
    
    words = morse_code.strip().split('  ')
    text = []
    
    for word in words:
        chars = word.split(' ')
        word_text = ''
        for char in chars:
            if char in morse_dict:
                word_text += morse_dict[char]
        text.append(word_text)
    
    return ' '.join(text)

def is_printable_ascii(text):
    """Check if text consists primarily of printable ASCII characters."""
    printable_count = sum(32 <= ord(c) <= 126 for c in text)
    return printable_count / len(text) > 0.8 if text else False

def main():
    if len(sys.argv) > 1:
        # Get input from command line argument
        input_text = sys.argv[1]
    else:
        # Get input from user
        print("Enter the encoded text to analyze:")
        input_text = input()
    
    results = detect_and_decode(input_text)
    
    if results:
        print("\nDetected encodings:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['type']}:")
            print(f"   Method: {result['decoding']}")
            print(f"   Result: {result['result']}")
    else:
        print("\nNo recognizable encoding detected or unable to decode the input.")
        print("You may need to provide more context about the encoding method.")

if __name__ == "__main__":
    main()

