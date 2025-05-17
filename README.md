# hash-identifier-and-decrypter (hiad.py for short)

I've created a comprehensive Python script that can analyze and decode various types of encoded data. This "Universal Decoder" can handle multiple encoding schemes and will automatically detect the most likely encoding format.

### Features: ###

Detects and decodes multiple encoding formats:

ASCII representation of binary (like your example "30313031...")
Binary (strings of 0s and 1s)
Hexadecimal
Base64
URL encoding
ROT13
Morse code
ASCII codes separated by spaces


Provides multiple possible interpretations when the encoding is ambiguous, shows both the detected encoding type and the decoded result.

## Usage: ##
You can use this script in two ways:

1. Run it and input your encoded text:

     python universal_decoder.py    // Then enter your encoded text when prompted.

or

2.   Pass the encoded text as a command-line argument:

     python universal_decoder.py "30313031303130313030313130303130" 


 The script is designed to be flexible and will attempt multiple decoding methods for each input, presenting all successful results so you can determine which one makes the most sense for your data.
 