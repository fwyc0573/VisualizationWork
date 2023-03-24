import re

path = r'C:\Users\FYC\Desktop\可视化\Microblogs.csv'
keywords_wholeSymptoms = r'flu|fever|chills|aches|coughing|breathing difficulty|nausea and vomiting|vomiting|diarrhea|enlarged lymph nodes'
keywords_wholeSymptoms = str(keywords_wholeSymptoms)

str1 = "I wanna say 'lazy sunday' but i have 2 do so much.. my room is a mess..."

result = re.findall(keywords_wholeSymptoms, str1, re.IGNORECASE)
print(result)
print(result!=[])
#python3
#以读入文件为例：
# f = open(path,"rb")#二进制格式读文件
# while True:
#     line = f.readline()
#     if not line:
#         break
#     else:
#         try:
#             #print(line.decode('utf8'))
#             line.decode('utf8')
#             #为了暴露出错误，最好此处不print
#         except:
#             print(str(lin