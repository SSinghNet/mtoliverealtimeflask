import requests
from bs4 import BeautifulSoup

USERNAME = "3450310391"
PASSWORD = "Realtime2021"
studentInfo = {}
classes = []
schedule = {}
currentDayCode = ""


session_requests = requests.session()
# cookies for login
payload = {
    "DISTRICTID": "MountOlive",
    "CFCLIENT_PARENTPORTALROOT": "districtid%3DMountOlive%23dbname%3DMountOlive%23loggedin%3Dfalse%23",
    "PARENTPORTALCODE": "",
}


def login(username, password):
    login_url = "https://www.fridaystudentportal.com/portal/security/validateStudent.cfm"
    # creates login session
    result = session_requests.post(
        login_url,
        cookies=payload,
        data={"username": username, "password": password}
    )
    print(result.url)
    if ("login.cfm" in result.url):
        return False
    return True


def getStudentInformation(username, password):
    url = "https://www.fridaystudentportal.com/portal/index.cfm?f=homepage.cfm"
    result = session_requests.post(
        url,
        cookies=payload,
        data={"username": username, "password": password}
    )

    pageSoup = BeautifulSoup(result.text, "html.parser")
    results = pageSoup.find(class_="header-bottom")
    results2 = pageSoup.find(class_="main-student-data")

    studentName = results.find("h6").text.split(
    )[0] + " " + results.find("h6").text.split()[1]
    studentId = results.find(class_="visible-sm").text.split()[2]
    studentGrade = results.find_all("h6")[2].text.split()[1]
    studentCohort = results.find_all("h6")[2].text.split(
    )[3] + " " + results.find_all("h6")[2].text.split()[4]
    studentCounselor = results2.find_all("h6")[0].text.split(
    )[1] + " " + results2.find_all("h6")[0].text.split()[2]
    studentHRTeacher = results2.find_all("h6")[1].text.split(
    )[2] + " " + results2.find_all("h6")[1].text.split()[3]
    studentImage = pageSoup.find(
        class_="student-picture-placeholder-wrapper").find("img")
    currentAttendance = results.find("span").text.replace("\n", "")

    studentInfo.update([("studentName", studentName), ("studentId", studentId), ("studentGrade", studentGrade), ("studentCohort", studentCohort), (
        "studentCounselor", studentCounselor), ("studentHRTeacher", studentHRTeacher), ("currentAttendance", currentAttendance), ("studentImage", studentImage["src"])])


def getGradebookOverview(username, password, mp):
    gradebook_url = "https://www.fridaystudentportal.com/portal/index.cfm?f=gradebook.cfm"
    result = session_requests.post(
        gradebook_url,
        cookies=payload,
        data={"username": username, "password": password, "selectMP": mp}
    )
    print(result.url)

    pageSoup = BeautifulSoup(result.text, "html.parser")
    results = pageSoup.find_all("td", class_="finedetail")
    # get length of results
    resultsLength = 0
    for i in results:
        resultsLength += 1

    i = 0
    while i < resultsLength:
        className = results[i].find("a").text
        classUrl = results[i].find("a").attrs["href"].replace(
            "§", "&sect").replace(" ", "")
        classSection = results[i].find("p").text.replace(" ", "")
        classAverage = results[i + 1].text.replace(" ", "").replace(
            "\n", "").replace("\t", "").replace("\r", "")
        classAverageLetter = "N/A"
        if(classAverage != ""):
            classAverage = int(classAverage)
            if(classAverage >= 98):
                classAverageLetter = "A+"
            elif(classAverage >= 93):
                classAverageLetter = "A"
            elif(classAverage >= 90):
                classAverageLetter = "A-"
            elif(classAverage >= 87):
                classAverageLetter = "B+"
            elif(classAverage >= 83):
                classAverageLetter = "B"
            elif(classAverage >= 80):
                classAverageLetter = "B-"
            elif(classAverage >= 77):
                classAverageLetter = "C+"
            elif(classAverage >= 73):
                classAverageLetter = "C"
            elif(classAverage >= 70):
                classAverageLetter = "C-"
            else:
                classAverageLetter = "F"
        else:
            classAverage = "N/A"

        classTeacher = results[i + 2].text.split()[0] + \
            " " + results[i + 2].text.split()[1]
        classTeacherEmail = results[i +
                                    2].find("a").attrs["href"].replace("mailto:", "").lower()
        newClass = True
        for j in classes:
            if(j["className"] == className):
                newClass = False
                j["mp" + mp] = {}
                j["mp" + mp]["classAverage"] = classAverage
                j["mp" + mp]["classAverageLetter"] = classAverageLetter
        if(newClass):
            classes.append(
                {"className": className, "classUrl": classUrl, "classSection": classSection, "classTeacher": classTeacher, "classTeacherEmail": classTeacherEmail,
                 "mp"+mp: {"classAverage": classAverage, "classAverageLetter": classAverageLetter, }}
            )
        i += 3


def getGrades(username, password):
    for m in range(4):
        mp = "1"
        if(m == 3):
            mp = "4"
        elif(m == 2):
            mp = "3"
        elif(m == 1):
            mp = "2"

        getGradebookOverview(username, password, mp)
        for k in classes:
            url = "https://www.fridaystudentportal.com" + k["classUrl"]
            result = session_requests.post(
                url,
                cookies=payload,
                data={"username": username, "password": password, "selectMP": mp}
            )
            pageSoup = BeautifulSoup(result.text, "html.parser")
            resultsCounter = pageSoup.find_all("tr")
            resultsAssignment = pageSoup.find_all(
                "td", {"class": "finedetail"})  # 6 each

            count = 0
            for l in resultsCounter:
                count += 1

            j = 0
            currentCategory = ""
            currentCategoryPercent = 0
            # k["mp" + mp] = {}
            try:
                k["mp" + mp]["assignments"] = {}
            except:
                k["mp" + mp] = {}
                k["mp" + mp]["assignments"] = {}
            for i in range(count):
                if resultsCounter[i].has_attr("class") and "table-row-subheader" in resultsCounter[i].get("class"):
                    currentCategory = (resultsCounter[i].text.replace(
                        "\n", "").replace("\t", "").replace("\r", ""))
                    currentCategoryPercent = currentCategory[currentCategory.index(
                        "-") + 2:currentCategory.index("%")]
                    currentCategory = currentCategory[0: currentCategory.index(
                        "-") - 1]

                    k["mp" + mp]["assignments"][currentCategory] = {}
                    k["mp" + mp]["assignments"][currentCategory]["assignments"] = []
                    k["mp" + mp]["assignments"][currentCategory]["categoryPercentage"] = currentCategoryPercent
                    continue
                if resultsCounter[i].has_attr("class") and "collapse" in resultsCounter[i].get("class"):
                    assDate = resultsAssignment[j + 1].text.replace(
                        "\n", "").replace("\t", "").replace("\r", "")
                    assName = resultsCounter[i - 1].text.replace(
                        "\n", "").replace("\t", "").replace("\r", "")
                    assPoints = resultsAssignment[j + 2].text.replace("\n", "").replace(
                        "\t", "").replace("\r", "").replace("\\xa0", "")
                    assTotalPoints = resultsAssignment[j + 3].text.replace(
                        "\n", "").replace("\t", "").replace("\r", "")
                    assDesc = resultsCounter[i].text.replace(
                        "\n", "").replace("\t", "").replace("\r", "")
                    assDesc = assDesc[12:len(assDesc)]

                    wholeAss = {"name": assName, "assDate": assDate, "assPoints": assPoints,
                                "assTotalPoints": assTotalPoints, "assDesc": assDesc}
                    k["mp" +
                        mp]["assignments"][currentCategory]["assignments"].append(wholeAss)
                    j += 6
    # with open("data.json", "w") as f:
    #     json.dump(classes, f)


def getSchedule(username, password, mp):
    schedule_url = "https://www.fridaystudentportal.com/portal/index.cfm?f=schedule.cfm"
    result = session_requests.post(
        schedule_url,
        cookies=payload,
        data={"username": username, "password": password, "selectMP": mp}
    )
    print(result.url)
    pageSoup = BeautifulSoup(result.text, "html.parser")
    results = pageSoup.find_all("td")

    schedule["A"] = []
    schedule["B"] = []
    schedule["C"] = []
    schedule["D"] = []

    i = 4
    while i < len(results) - 4:
        classNum = results[i].text.replace("\n", "").replace(
            "\t", "").replace("\r", "").replace(" ", "")
        classNames = [
            results[i+1].text.replace("\n", "").replace("\t",
                                                        "").replace("\r", ""),
            results[i+2].text.replace("\n", "").replace("\t",
                                                        "").replace("\r", ""),
            results[i+3].text.replace("\n", "").replace("\t",
                                                        "").replace("\r", ""),
            results[i+4].text.replace("\n", "").replace("\t",
                                                        "").replace("\r", ""),
        ]

        if(classNum == "LNCH"):
            for j in classNames:
                j = "Lunch"

        jj = 0
        for j in classNames:
            k = j.split()
            if(classNum == "LNCH"):
                className = "Lunch"
                classRoom = ""
                classTeacher = ""
                classSection = ""
            else:
                try:
                    classRoom = k[len(k)-1]
                    classTeacher = k[len(k) - 3][k[len(k) - 3].index(".") -
                                                 1: k[len(k) - 3].index(".")] + ". " + k[len(k) - 2]
                    classSection = k[len(
                        k) - 3][k[len(k) - 3].rindex("H"): k[len(k) - 3].index(".") - 1]
                    className = j[0:j.rindex("H", 0, j.index("."))]
                except:
                    classRoom = ""
                    classTeacher = ""
                    classSection = ""
                    className = ""
            thisList = {"classNum": classNum, "className": className,
                        "classTeacher": classTeacher, "classSection": classSection, "classRoom": classRoom}
            if(className != ""):
                if(jj == 0):
                    schedule["A"].append(thisList)
                elif(jj == 1):
                    schedule["B"].append(thisList)
                elif(jj == 2):
                    schedule["C"].append(thisList)
                elif(jj == 3):
                    schedule["D"].append(thisList)
            jj += 1
        i += 5
   # print(schedule)

def getDay(username, password):
    login(username, password)
    schedule_url = "https://www.fridaystudentportal.com/portal/index.cfm?f=myStudent.cfm"
    result = session_requests.post(
        schedule_url,
        cookies=payload,
        data={"username": username, "password": password}
    )
    print(result.url)
    pageSoup = BeautifulSoup(result.text, "html.parser")
    results = pageSoup.find_all("td")
    
    currentDayCode = results[9].text.replace("\n", "").replace("\t", "").replace("\r", "")[3:]
    return currentDayCode


def getClasses(username, password):
    login(username, password)
    getGrades(username, password)
    return classes


def getStudentInfo(username, password):
    login(username, password)
    getStudentInformation(username, password)
    return studentInfo


def getSched(username, password, mp):
    login(username, password)
    getSchedule(username, password, mp)
    return schedule


def main():
    login(USERNAME, PASSWORD)
    getDay(USERNAME, PASSWORD)
    print(currentDayCode)
    # getStudentInformation(USERNAME, PASSWORD)
    # getGrades(USERNAME, PASSWORD)
    # print(studentInfo)
    # print(classes)


if __name__ == "__main__":
    main()
