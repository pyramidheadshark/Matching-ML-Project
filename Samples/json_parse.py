import json

# считываем данные из json-файла с первоначальными данными
with open('obuchenie.json', mode='r', encoding='utf-8') as srcfl:
    data = json.load(srcfl)

outdata_final = []
# собираем нужные нам данные из записей
for i in data:
    outdata = [i['vacancy']['uuid'], i['vacancy']['keywords'], i['vacancy']['description']]
    outdata_final.append(outdata)
# сохраняем данные в новый json-файл
with open(r'vacancys.json', mode='w', encoding='utf-8') as outfl:
    json.dump(outdata_final, outfl, sort_keys=True, indent=4)