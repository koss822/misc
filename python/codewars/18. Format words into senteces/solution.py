def format_words(words):
    if not words:
        return ''
    words = [a for a in words if a]
    lw = len(words)
    if lw==0:
        return ''
    elif lw>1:
        return ', '.join(words[:-1])+' and '+words[-1:][0]
    else:
        return words[0]