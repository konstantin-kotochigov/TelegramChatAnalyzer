from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas
import os

filesdir = "/home/konstantin/Downloads/Telegram Desktop/ChatExport_14_01_2019 (3)"
files = [x for x in os.listdir(filesdir) if x.endswith(".html")]

def convert_data(message):
    id = message['id']
    from_name = message.find("div",{"class":"from_name"})
    if not (from_name is None):
        from_name = from_name.contents[0]
    else:
        from_name = ""
    textTag = message.find("div",{"class":"text"})
    if not (textTag is None):
        text = textTag.contents[0]
    else:
        text = ""
    return {"id":id, "from_name":from_name, "text":text}

df = pandas.DataFrame()
for filename in tqdm(files, unit="file", total=len(files)):
  f = open(filesdir+"/"+filename)
  bs = BeautifulSoup(f.read(), "html.parser")
  hist = bs.find("div",{"class":"history"})
  messages = hist.findAll("div",{"class":["message default clearfix", "message default clearfix joined"]})
  text_data = [convert_data(message) for message in messages]
  df = df.append(pandas.DataFrame.from_records(text_data))
  f.close()

df.text = df.text.apply(lambda x: x.replace("\n","").strip())
df.from_name = df.from_name.apply(lambda x: x.replace("\n","").strip())
df.id = pandas.to_numeric(df.id.apply(lambda x: x.replace("\n","")[7:]))

df.sort_values(by="id", inplace=True)

df.from_name[df.from_name==""] = None 
df['from_name'] = df.from_name.ffill()

df.to_csv(filesdir+"/df.csv", sep=";")