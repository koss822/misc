def reverse_words(text):
  words = []
  for word in text.split(' '):
      word_array = list(word)
      word_array.reverse()
      words.append(str(''.join(word_array)))
  return ' '.join(words)