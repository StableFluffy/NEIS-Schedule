
import requests
from icalendar import Calendar, Event
from datetime import datetime
cal = Calendar()

API_KEY = 여기에 API 키 입력

school_codes = [0]
locale_code = [0]
r = input("출력을 원하는 학교 이름을 입력 해주세요.\n")

res_search = requests.get(f"https://open.neis.go.kr/hub/schoolInfo?SCHUL_NM={r}&Type=json&pIndex=1&pSize=100&KEY={API_KEY}")


for x in res_search.json()["schoolInfo"][1]["row"]:

    print(x["SCHUL_NM"], x["ORG_RDNDA"])
    school_codes.append(int(x["SD_SCHUL_CODE"]))
    locale_code.append(x["ATPT_OFCDC_SC_CODE"])

r = int(input("몇 번째 학교인가요?"))

r_2 = (input("몇 년도 자료를 검색 할까요?"))

res_cal = requests.get(f"https://open.neis.go.kr/hub/SchoolSchedule?ATPT_OFCDC_SC_CODE={locale_code[r]}&SD_SCHUL_CODE={school_codes[r]}&AA_FROM_YMD={r_2}0101&AA_TO_YMD={r_2}1231&pSize=500&Type=json&KEY={API_KEY}")
got_same_in_prev = False
for index, x in enumerate(res_cal.json()["SchoolSchedule"][1]["row"]):
        print(index+1, "번째 처리중.")
        event = Event()
        event.add('summary', x["EVENT_NM"])
        event.add('description', x["SBTR_DD_SC_NM"])
        event.add('dtstart', datetime.strptime(x["AA_YMD"], '%Y%m%d'))
        event.add('dtstamp', datetime.now())
        cal.add_component(event)
print("완료")
print(f"https://open.neis.go.kr/hub/SchoolSchedule?ATPT_OFCDC_SC_CODE={locale_code[r]}&SD_SCHUL_CODE={school_codes[r]}&AA_FROM_YMD={r_2}0101&AA_TO_YMD={r_2}1231&pSize=500&Type=json&KEY={API_KEY}")
        

sc_name = x["SCHUL_NM"]
f = open(f"{sc_name}.ics", 'wb')
f.write(cal.to_ical())
f.close()
