def retweet_check(status):
    if hasattr(status, 'retweeted_status'):
        return True
    else:
        return False

def spam_test(text, filter):
    palavras_deteck = 0
    lista_de_palavras = text.upper().split()
    for filtro in filter:
        for palavra in lista_de_palavras:
            if palavra == filtro.upper():
                palavras_deteck += 1
    if palavras_deteck > 7:
        return True
    else:
        return False

def len_test(text):
    if len(text) > 15:
        return True
    else:
        return False

