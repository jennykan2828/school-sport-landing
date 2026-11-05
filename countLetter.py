def count_each_letter(text):
      letter_counts = {}
      for char in text.lower():
        if char.isalpha():  # Ignores spaces, numbers, and punctuation
          letter_counts[char] = letter_counts.get(char, 0) + 1
      return letter_counts


message = "Hello, World!"
print(count_each_letter(message))

for item, number in count_each_letter(message).items():
     print(f"{item}: {number}")

