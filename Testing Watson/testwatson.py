import json 
from watson_developer_cloud import AlchemyLanguageV1

s = 2
actualpos = 0
actualneg = 0
posasneg = 0
negaspos = 0

with open("test.txt") as f:
  content = f.readlines()
  alchemy_language = AlchemyLanguageV1(api_key='30d76f945d0b9cc098b98f4ee11b90777602cdea')
  for x in content:
    y = x[len(x) - 2]
    x = x[:-2]
    response = alchemy_language.sentiment(text=x, language='english')
    if response['status'] == 'OK':
      if(response['docSentiment']['type'] == "negative"):
        s = 0
      elif(response['docSentiment']['type'] == "positive"):
        s = 1

    if(s == 1 and y == '1'):
      actualpos = actualpos + 1
    elif(s == 0 and y == '0'):
      actualneg = actualneg + 1
    elif(s == 1 and y == '0'):
      negaspos = negaspos + 1
    elif(s == 0 and y == '1'):
      posasneg = posasneg + 1

  print(actualpos, posasneg)
  print(negaspos, actualneg)
  
