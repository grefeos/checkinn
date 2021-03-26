from dadata import Dadata
from datetime import datetime
import time
with open('token.conf', encoding='utf-8') as f:
    token=f.read()
dadata = Dadata(token)
result = dadata.find_by_id("party", "261803043695")
inn = result[0].get('data').get('inn')
status = result[0].get('data').get('state').get('status')
my_file = open("list.txt", "r")
content = my_file.read()
content_list = content.split("\n")
my_file.close()
resulttext = 'Inn;Status;Actuality_date;Registration_date;Liquidation_date\n'
failtext = 'Inn;Status;Actuality_date;Registration_date;Liquidation_date\n'
for current in range(len(content_list)-1):
    result = dadata.find_by_id("party", content_list[current])
    actuality_date = ''
    registration_date = ''
    liquidation_date = ''
    if not result:
        failtext += content_list[current] + ";" + "fail" + "\n"
        resulttext += content_list[current] + ";" + "fail" + "\n"
        print(str(current) + "/" + str(len(content_list)) + ";" + content_list[current] + ";" + "fail")
    if result:
        inn = result[0].get('data').get('inn')
        status = result[0].get('data').get('state').get('status')
        actuality_date = datetime.fromtimestamp(result[0].get('data').get('state').get('actuality_date')/1000).strftime('%Y.%m.%d')
        registration_date = datetime.fromtimestamp(result[0].get('data').get('state').get('registration_date')/1000).strftime('%Y.%m.%d')
        if result[0].get('data').get('state').get('liquidation_date') != None:
            liquidation_date = datetime.fromtimestamp(result[0].get('data').get('state').get('liquidation_date')/1000).strftime('%Y.%m.%d')
        if status != "ACTIVE":
            failtext += inn + ";" + status + ";" + actuality_date + ";" + registration_date + ";" + liquidation_date + "\n"
        resulttext += inn + ";" + status + ";" + actuality_date + ";" + registration_date + "\n"
        print(str(current) + "/" + str(len(content_list)) + ";" + inn + ";" + status + ";" + actuality_date + ";" + registration_date + ";" + liquidation_date)
    time.sleep(2)
failfile = open("fail.csv", "a")
failfile.write(failtext)
failfile.close()
resultfile = open("result.csv", "a")
resultfile.write(resulttext)
resultfile.close()
#docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python3-32bit "pyinstaller checkinn.py"
#docker run -v "$(pwd):/src/" -v "$(pwd)/entrypoint.sh:/entrypoint.sh" cdrx/pyinstaller-windows:python3-32bit
#pyinstaller --onefile --console --clean checkinn.py