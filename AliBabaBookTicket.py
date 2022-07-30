import time
from BookTicket import BookTicket
from CompleteForms import CompleteForms
from selenium.webdriver.common.by import By


class AliBabaBookTicket(BookTicket, CompleteForms):
    __URL: str = "https://www.alibaba.ir/"

    __cities: dict = {
        "90016": "آب نيل",
        "670": "آب نيل",
        "337": "آباده",
        "7": "آبيك",
        "4": "آبگرم",
        "9": "آتش بغ",
        "224": "آزادور",
        "290": "آنكارا",
        "14": "اراك",
        "261": "اردكان",
        "510": "ارسنجان",
        "448": "اروميه",
        "18": "ازنا",
        "20": "اسفراين",
        "301": "اسلامشهر",
        "21": "اصفهان",
        "387": "اقليد",
        "51": "الوند",
        "22": "امروان",
        "24": "انديمشك",
        "25": "اهواز",
        "450": "اينچه برون",
        "28": "بادرود",
        "30": "بافق",
        "383": "بجستان",
        "76": "بستان آباد",
        "34": "بكران",
        "299": "بم",
        "36": "بندرتركمن",
        "37": "بندرعباس",
        "226": "بهاباد",
        "43": "بيابانك",
        "44": "بيشه",
        "54": "تاكستان",
        "55": "تبريز",
        "449": "تجرك",
        "251": "تربت حيدريه",
        "912": "تربيت معلم",
        "59": "تنگ هفت",
        "1": "تهران",
        "56": "تپه سفيد",
        "287": "جاجرم ",
        "61": "جاجرم",
        "221": "جلفا",
        "351": "جمكران",
        "62": "جوين",
        "69": "خراسانك",
        "71": "خرم دره",
        "70": "خرم پي",
        "72": "خرمشهر",
        "369": "خواف",
        "75": "دامغان",
        "78": "دورود",
        "285": "رازي",
        "344": "رباط كريم",
        "451": "رشت",
        "373": "زادمحمود",
        "259": "زاهدان",
        "92": "زرند",
        "96": "زرين دشت",
        "97": "زنجان",
        "239": "زواره",
        "100": "ساري",
        "65": "ساوه",
        "105": "سبزوار",
        "48": "سراوان",
        "83": "سربندر",
        "234": "سرخس",
        "257": "سعادت شهر",
        "115": "سلماس",
        "116": "سمنان",
        "120": "سنخواست",
        "123": "سهند",
        "121": "سوادكوه",
        "125": "سيرجان",
        "128": "سيمين دشت",
        "106": "سپيددشت",
        "129": "شازند",
        "130": "شاهرود",
        "133": "شرفخانه",
        "511": "شلمچه",
        "264": "شهرضا",
        "600": "شهركرد",
        "512": "شهيد سليمي",
        "135": "شوش",
        "134": "شوشتر",
        "255": "شيراز",
        "144": "شيرگاه",
        "90031": "صفا شهر",
        "258": "صفاشهر",
        "311": "طبس",
        "148": "عجب شير",
        "509": "فهرج",
        "40": "فيروزان",
        "154": "فيروزكوه",
        "156": "قائمشهر",
        "160": "قزوين",
        "161": "قم",
        "403": "كارون",
        "162": "كاشان",
        "508": "كربلا",
        "165": "كرج",
        "167": "كرمان",
        "195": "كرمانشاه",
        "302": "ماهشهر",
        "249": "محمديه",
        "189": "مراغه",
        "256": "مرودشت",
        "191": "مشهد",
        "15": "ملاير",
        "194": "مهاباد",
        "86": "مهران",
        "250": "مياندوآب",
        "197": "ميانه",
        "198": "ميبد",
        "202": "نقاب",
        "262": "نقده",
        "203": "نكا",
        "206": "نيشابور",
        "213": "هرند",
        "215": "هشتگرد",
        "216": "هفت تپه",
        "117": "همدان",
        "295": "وان",
        "209": "ورامين",
        "211": "ورزنه",
        "212": "ورسك",
        "219": "يزد",
        "401": "پرند",
        "50": "پل سفيد",
        "53": "پيشوا",
        "66": "چمسنگر",
        "176": "گرمسار",
        "175": "گرگان",
    }

    def __init__(self):
        CompleteForms.__init__(self, self.__URL)

    def __del__(self):
        self.driver.close()

    # Login
    def login(self, data):
        self.__goToLoginForm()
        self.completeInputForm(data['username'], "/html/body/div/div[2]/div/div/form/div[1]/span/input",
                               By.XPATH)
        self.completeInputForm(data['password'], "/html/body/div/div[2]/div/div/form/div[2]/span/input",
                               By.XPATH)
        self.clickBtn("/html/body/div/div[2]/div/div/form/div[3]/button", By.XPATH)

    def __goToLoginForm(self):
        self.clickBtn("//header/div[1]/div/div/div/button", By.XPATH)
        self.clickBtn("/html/body/div/div[2]/div/div/form/div[2]/button[2]", By.XPATH)

    # Search
    def search(self, data):
        self.__goToSearchPage()
        self.__completeFormSearch(data)
        find: bool = False
        while not find:
            self.__btnSearch()
            try:
                self.__getTrains()
                if data['groupWay'] == 1:
                    self.__getTrains()
                find = True
            except:
                self.clickBtn("/html/body/div/div[1]/header/div[2]/div/div/div/div/div/button",
                              By.XPATH)

    def __getTrains(self):
        self.__minTrain()
        self.clickBtn("//section/div[2]/div[1]/div[2]/button",
                      By.XPATH)

    def __minTrain(self):
        t = self.wait_and_return("//section/div[1]/ul/li[3]/a",
                                 By.XPATH)
        time.sleep(2)
        t.click()
        self.completeCheckBox(
            "//aside/div/div/div[5]/div/details/div/div/label", By.XPATH)

    def __btnSearch(self):
        self.clickBtn(
            "//form/div[2]/div[4]/button", By.XPATH)

    def __goToSearchPage(self):
        time.sleep(2)
        self.clickBtn('//a[@href="/train-ticket"]', By.XPATH)

    def __completeFormSearch(self, data):
        self.__groupWay(data['groupWay'])
        self.__wagon(data['wagon'])
        self.__sex(data['sex'])
        self.__from(data['from'])
        self.__to(data['to'])
        self.__fromD(data['fromd'])
        if data['groupWay'] == 1:
            self.__toD(data['tod'])
        self.__setDate()
        self.__traveler(data['adult'], data['child'], data['infant'])

    def __traveler(self, adult, child, infant):
        self.clickBtn(
            "//form/div[2]/div[3]/div/div[1]", By.XPATH)
        for i in range(1, int(adult)):
            self.clickBtn(
                "//form/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/button[1]",
                By.XPATH)
        for i in range(0, int(child)):
            self.clickBtn(
                "//form/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/button[1]",
                By.XPATH)
        for i in range(0, int(infant)):
            self.clickBtn(
                "//form/div[2]/div[3]/div/div[2]/div/div[3]/div[2]/button[1]",
                By.XPATH)

    def __setDate(self):
        self.clickBtn(
            "//form/div[2]/div[2]/div/div[2]/div/div[3]/button",
            By.XPATH)

    def __toD(self, data: str):
        date = data.split('/')
        self.clickBtn(
            "//form/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/span[" +
            str(int(date[2]) + 7) + "]",
            By.XPATH)

    def __fromD(self, data):
        date = data.split('/')
        self.clickBtn(
            "//form/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/span[" +
            str(int(date[2]) + 7) + "]",
            By.XPATH)

    def __to(self, data):
        city = self.__getCity(data)
        self.completeInputForm(city,
                               "//form/div[2]/div[1]/div/div[1]/div[2]/span/input",
                               By.XPATH)
        self.clickBtn(
            "//form/div[2]/div[1]/div/div[2]/div/ul/li[1]/a",
            By.XPATH)

    def __from(self, data):
        city = self.__getCity(data)
        self.completeInputForm(city,
                               "//form/div[2]/div[1]/div/div[1]/div[1]/span[1]/input",
                               By.XPATH)
        self.clickBtn(
            "//form/div[2]/div[1]/div/div[2]/div/ul/li[1]/a",
            By.XPATH)

    def __getCity(self, date) -> str:
        return self.__cities[date]

    def __sex(self, data):
        self.clickBtn(
            "//form/div[1]/span[3]/button", By.XPATH)
        if data == "1":
            self.clickBtn(
                "//form/div[1]/span[3]/div/div/ul/li[3]/a",
                By.XPATH)
        elif data == "2":
            self.clickBtn(
                "//form/div[1]/span[3]/div/div/ul/li[2]/a",
                By.XPATH)
        elif data == "3":
            self.clickBtn(
                "//form/div[1]/span[3]/div/div/ul/li[1]/a",
                By.XPATH)

    def __wagon(self, data):
        self.clickBtn(
            "//form/div[1]/span[2]/button", By.XPATH)
        if data == "0":
            self.clickBtn(
                "//form/div[1]/span[2]/div/div/ul/li[2]/a",
                By.XPATH)
        elif data == "1":
            self.clickBtn(
                "//form/div[1]/span[2]/div/div/ul/li[1]/a",
                By.XPATH)

    def __groupWay(self, data):
        self.clickBtn(
            "//form/div[1]/span[1]/button", By.XPATH)
        if data == 0:
            self.clickBtn(
                "//form/div[1]/span[1]/div/div/ul/li[1]/a",
                By.XPATH)
        elif data == 1:
            self.clickBtn(
                "//form/div[1]/span[1]/div/div/ul/li[2]/a",
                By.XPATH)

    # set users
    def setUsers(self, dataUsers):
        for i in range(1, len(dataUsers) + 1):
            self.__setUser(i, dataUsers[i - 1])
        self.__setUsersBtn()

    def __setUsersBtn(self):
        self.clickBtn('//main/div/div/div/div/div[3]/button', By.XPATH)

    def __setUser(self, i, data):
        self.__setFName(i, data['FName'])
        self.__setLName(i, data['LName'])
        self.__setSex(i, data['sex'])
        self.__setId(i, data['id'])
        self.__setBirthday(i, data['birthday'])

    def __setBirthday(self, i, data):
        self.__setDay(i, data['day'])
        self.__setMonth(i, data['month'])
        self.__setYear(i, data['year'])

    def __setYear(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[3]",
                      By.XPATH)
        self.clickBtn(
            "//form/div[2]/div/div[1]/div[2]/div/div[5]/div/div[3]/div[2]/div/ul/li[@data-value=\"13" + data + "\"]/a",
            By.XPATH)

    def __setMonth(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[2]",
                      By.XPATH)
        if data[0] == 0:
            data = data[1:]
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[2]/div[2]/div/ul/li["
                      + data +
                      "]/a", By.XPATH)

    def __setDay(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[1]",
                      By.XPATH)
        if data[0] == 0:
            data = data[1:]
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[5]/div/div[1]/div[2]/div/ul/li["
                      + data +
                      "]/a",
                      By.XPATH)

    def __setId(self, i, data):
        self.completeInputForm(data,
                               "//form/div[2]/div/div["
                               + str(i) +
                               "]/div[2]/div/div[4]/div/span/input",
                               By.XPATH)

    def __setSex(self, i, data):
        self.clickBtn("//form/div[2]/div/div["
                      + str(i) +
                      "]/div[2]/div/div[3]/div",
                      By.XPATH)
        if data == "1":
            self.clickBtn(
                "//form/div[2]/div/div["
                + str(i) +
                "]/div[2]/div/div[3]/div/div[2]/div/ul/li[2]/a",
                By.XPATH)
        elif data == "2":
            self.clickBtn(
                "//form/div[2]/div/div["
                + str(i) +
                "]/div[2]/div/div[3]/div/div[2]/div/ul/li[1]/a",
                By.XPATH)

    def __setLName(self, i, data):
        self.completeInputForm(data,
                               "//main/form/div[2]/div/div["
                               + str(i) +
                               "]/div[2]/div/div[2]/div/span/input",
                               By.XPATH)

    def __setFName(self, i, data):
        self.completeInputForm(data,
                               "//main/form/div[2]/div/div["
                               + str(i) +
                               "]/div[2]/div/div[1]/div/span/input",
                               By.XPATH)

    # buy
    def buy(self):
        self.clickBtn("/html/body/div/div[1]/main/div/div[5]/div/div[1]/div[1]/div[1]/label", By.XPATH)
        self.clickBtn("/html/body/div/div[1]/main/div/div[5]/div/div[2]/button[2]", By.XPATH)
        time.sleep(60)
