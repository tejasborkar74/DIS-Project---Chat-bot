import requests

api_key = 'qxf7w45ra2s5xsmydv2j14hizdxvjattwuqygwye72nrw2l4z'

def retrive_defination(word):
    result = requests.get('https://api.wordnik.com/v4/word.json/'+ word+'/definitions?limit=200&includeRelated=false&useCanonical=false&includeTags=false&api_key='+api_key)
    if result.status_code != 200:
        res = "Sorry word not found :("
        return res
    res = result.json()
    # print(res)
    for node in res:
        if not (node.get('text') is None):
            return node['text']
    return "Sorry word not found :("



def retrive_example(word):
    result = requests.get('https://api.wordnik.com/v4/word.json/' + word + '/examples?includeDuplicates=false&useCanonical=false&limit=5&api_key='+api_key)
    if result.status_code != 200:
        res = "Sorry word not found :("
        return res
    res = result.json()
    # print(res)
    return res['examples'][0]['text']


def retrive_synonym(word):
    result = requests.get('https://api.wordnik.com/v4/word.json/' + word + '/relatedWords?useCanonical=false&limitPerRelationshipType=10&api_key='+api_key)
    if result.status_code != 200:
        res = "Sorry word not found :("
        return res
    res = result.json()
    for node in res:
        if node['relationshipType'] == "synonym":
            l = node['words']
            ans = 'Synonyms for ' + word + ' are '
            for x in l:
                ans = ans + x + ', '
            ans = ans + 'etc'
            return ans 
    ans = "Sorry Synonyms for the given word not found :("
    return ans


def retrive_phrases(word):
    result = requests.get('https://api.wordnik.com/v4/word.json/' + word + '/phrases?limit=5&useCanonical=false&api_key=' + api_key)
    if result.status_code != 200:
        res = "Sorry word not found :("
        return res
    res = result.json()
    ans = 'Some Phrases related to '+word+' are '
    for node in res:
        phrase = node['gram1'] + ' ' + node['gram2']
        ans = ans + phrase + ', '
    ans = ans + 'etc'
    return ans
    

removal_words = {'can', 'is', 'are', 'what', 'tell', 'the', 'me', 'of', 'some', 'you', 'your', 'give', 'related'}
identify_defination = {'defination', 'meaning'}
identify_example = {'example','examples'}
identify_synonym = {'synonym', 'synonyms'}    
identify_phrase = {'phrase', 'phrases'}


def get_response(input):

    if input == '':
        res = 'Hey, I am a dictionary chat bot, you can ask me meaning, example, and other information related to words :)'
        return res

    input = input.lower()
    vec = input.split()
    type = -1
    check = 0
    # n = len(vec)
    # print(n)
    if len(vec) == 1:
        res = retrive_defination(vec[0])
        return res
    
    if len(vec) == 2:
        if vec[1] in identify_defination:
            res = retrive_defination(vec[0])
            return res
        elif vec[1] in identify_example:
            res = retrive_example(vec[0])
            return res
        elif vec[1] in identify_synonym:
            res = retrive_synonym(vec[0])
            return res

            
    for x in vec:
        # x = vec[i]
        # print(x)
        if x == 'related' or x == 'word' or x == 'words':
            check += 1
        if x in identify_defination:
            type = 1
        elif x in identify_example:
            type = 2
        elif x in identify_synonym:
            type = 3
        elif x in identify_phrase:
            type = 4
        elif check == 2:
            type = 3
            check = 0
        elif x not in removal_words:
            word = x
        # print(check)
        
    # res = ''
    if type == -1 or type == 1: 
        res = retrive_defination(word)
    elif type == 2:
        res = retrive_example(word)
    elif type == 3:
        res = retrive_synonym(word)
    elif type == 4:
        res = retrive_phrases(word)
    return res 

# def get_response(input):
#     res = retrive_defination(input)
#     return res


print('Bot: Hey, I am a dictionary chat bot, you can ask me meaning, example, and other information related to words :');
while True:
    print('Bot: ' + get_response(input('You: ')))