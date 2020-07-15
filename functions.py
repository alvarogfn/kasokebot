def no_text(text):
    return lambda filter: text.split()[0] != filter

def get_phrases():
    with open('frase.txt', 'r', encoding='utf-8') as outfile:
        frases = outfile.read()
        frases = frases.split(sep='\n\n')
        outfile.close()
        return frases