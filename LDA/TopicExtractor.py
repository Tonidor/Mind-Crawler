import requests
import json

text = "I’m so upset!! I don’t even know where to begin!  To start off, I think I completely failed my geometry quiz, which I know I should’ve studied more for...my dad’s not gonna be happy about that. :( Then, we had a pop quiz in history on the reading homework from last night, and I completely forgot most of what I read, which made me even more upset because I actually did the reading! But what really made me mad was the note that Sarah slipped into my locker during passing period. She said she was sad that I’ve been hanging out with Jane more lately and thinks that I don’t want to be her friend anymore. I can’t believe she thinks that, especially after talking with her on the phone for hours and hours last month while she was going through her breakup with Nick! Just because I’ve been hanging out with Jane a little more than usual doesn’t mean I’m not her friend anymore. She completely blew me off at lunch, and when I told Jane, she thought that Sarah was being a “drama queen.”This is just what I need! My parents are getting on my case about doing more extracurricular activities, I have a huge paper due for AP English soon, and I can’t understand a thing in advanced Spanish! The last thing I need is for my best friend to think I hate her and barely text me back anymore.  Uggh! I can’t concentrate on anything right now because of it. I hope she gets over it!!!"
text2 = "hello my name is matti"
url = "https://api.meaningcloud.com/topics-2.0"

payload = "key=b96a7c53a9d795bf47c19609b8a68341&lang=en&tt=ec&url=https://www.wikihow.com/Sample/Blog-Post"
headers = {'content-type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url=url, data=payload, headers=headers)

topicJson = json.loads(response.text)

for entity in topicJson["entity_list"]:
    print(entity["form"])

for concept in topicJson["concept_list"]:
        print(concept["form"])
#with open('data.json', 'w') as outfile:
#   json.dump(response.text, outfile)
