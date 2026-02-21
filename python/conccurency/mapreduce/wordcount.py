import re
import os
import glob
import typing as T

Occurrences = T.Dict[str, int]

ENCODING = "ISO-8859-1"

def wordcount(filenames: T.List[str]) -> Occurrences:
    word_counts = {}
    for filename in filenames:
        print(f"Calculating {filename}")
        with open(filename, "r", encoding=ENCODING) as file:
            for line in file:
                words = re.split("\W+", line)
                for word in words:
                    word = word.lower()
                    if word != "":
                        word_counts[word] = 1 + word_counts.get(word, 0)
    return word_counts

if __name__ == "__main__":
    data = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/input_files/*.txt")
    )
    result = wordcount(data)
    print(result)