MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
'C':'-.-.', 'D':'-..', 'E':'.',
'F':'..-.', 'G':'--.', 'H':'....',
'I':'..', 'J':'.---', 'K':'-.-',
'L':'.-..', 'M':'--', 'N':'-.',
'O':'---', 'P':'.--.', 'Q':'--.-',
'R':'.-.', 'S':'...', 'T':'-',
'U':'..-', 'V':'...-', 'W':'.--',
'X':'-..-', 'Y':'-.--', 'Z':'--..',
'1':'.----', '2':'..---', '3':'...--',
'4':'....-', '5':'.....', '6':'-....',
'7':'--...', '8':'---..', '9':'----.',
'0':'-----', ', ':'--..--', '.':'.-.-.-',
'?':'..--..', '/':'-..-.', '-':'-....-',
'(':'-.--.', ')':'-.--.-'}
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}


def encode(message):
  encoded_list = []
  for char in message.upper():
    if char == " ":
      encoded_list.append("/")  # Standard space separator in Morse
    elif char in MORSE_CODE_DICT:
      encoded_list.append(MORSE_CODE_DICT[char])
  return " ".join(encoded_list)


def decode(encoded_message):
  decoded_chars = []
  # Split by space to get individual morse symbols, or handle '/' for spaces
  # Note: words are usually separated by '/' or multiple spaces
  words = encoded_message.strip().split(" / ")
  decoded_words = []

  for word in words:
    chars = word.split()
    decoded_word = "".join(REVERSE_MORSE_DICT.get(c, "") for c in chars)
    decoded_words.append(decoded_word)

  return " ".join(decoded_words)


message = input("Enter a message to encode: ")
encoded = encode(message)
print("Encoded:", encoded)
print("Decoded:", decode(encoded))
