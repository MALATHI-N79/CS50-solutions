import re
import math

def words(text):
    return len(text.split())

def letters(text):
    return sum(1 for char in text if char.isalpha())

def sentences(text):
    return len(re.findall(r'[.!?]', text))

def main():
    text = input("Text: ")
    W = words(text)
    L = letters(text)
    S = sentences(text)

    index = round(0.0588 * (L / W * 100.0) - 0.296 * (S / W * 100.0) - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")

if __name__ == "__main__":
    main()