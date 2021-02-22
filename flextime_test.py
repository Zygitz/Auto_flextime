from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
google_username, google_password = open("info/info.txt").read().split()
activities = {
}

class flextime(object):
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.browser = webdriver.Chrome(executable_path='C:\\Users\MRGra\Documents\Python Projects\Flextime\driver\chromedriver.exe')
        self.browser_commands(user, passwd, self.browser)

        self.var = self.beautiful_soup()
        self.plt = {"A": "250", "B": "251", "C": "252"}
        # self.month, self.start_day, self.end_day, self.favorites = [], [], [], []
        # self.day_flextime(16, self.plt["B"])
        self.prompt_user()
    def prompt_user(self):
        '''Prompts user for info'''
        month = str(input("Enter the month: \n>>> "))
        start_day = int(input("Enter the start day you would like to schedule PLTs for: \n>>> "))
        end_day = int(input("Enter the end day you would like to schedule PLTs for: \n>>> "))
        # self.favorites = bool(input("Would you like to use your favorite classes? (Type True/False) \n>>> "))
        with open("info/data_output.json") as infile:
            teacher_list = json.load(infile)
        for days in range(start_day, end_day + 1):
            for plt_ABC in self.plt:
                self.day_flextime(month, days, self.plt[plt_ABC])
                avail_PLTs_list = self.beautiful_soup()
                #class capacity
                for input_class in teacher_list:
                    for avail_class in avail_PLTs_list:
                        #determines if class is full
                        capacity = avail_class["class_capacity"].split("/")
                        # print(int(capacity[0]), int(capacity[1]))
                        # determine_full = int(capacity[0])/int(capacity[1])
#                       #if inner loop breaks, outer loop will break
                        if avail_class["class_teacher"] == input_class and int(capacity[0])/int(capacity[1]) < 1:
                            self.browser_input(class_id=avail_class["class_id"],class_desc=avail_class["class_info"], month=month, day=days)
                            break
                    else:
                        continue
                    break
    def browser_commands(self, google_username, google_password, browser):
        '''initial setup for the browser'''
        browser.get("https://www.flextimemanager.com/gpluslogin/oauth2callback/google")
        print("entering username...")
        browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys(google_username)
        browser.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()
        time.sleep(1)
        print("entering password...")
        browser.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(google_password)
        browser.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()
        time.sleep(1)
    def day_flextime(self, month, day, plt):
        '''Connects to URL given: day, PLT, month'''
        print(f"Connecting to flextime {month}/{day}, PLT - {plt}")
        self.browser.get(f"https://www.flextimemanager.com/student/mftm_get_day_activities/2021-{month}-{day}/{plt}/agendaFiveDay#")
        time.sleep(0.5)
    def testing(self):
        '''Scrapes all the html'''
        var_count = 25
        testing_return = []
        for i in range(2):
            self.day_flextime(var_count, self.plt["A"], 11)
            pltA_day = self.beautiful_soup()
            # self.browser_input("276218", self.browser, var_count)
            self.day_flextime(var_count, self.plt["B"], 11)
            pltB_day = self.beautiful_soup()
            # self.browser_input("276218", self.browser, var_count)
            self.day_flextime(var_count, self.plt["C"], 11)
            pltC_day = self.beautiful_soup()
            # self.browser_input("276218", self.browser, var_count)
            plt_overall = {
                "date": var_count,
                "PLT_A": pltA_day,
                "PLT_B": pltB_day,
                "PLT_C": pltC_day
            }
            testing_return.append(plt_overall)
            var_count += 1
        return testing_return
    def browser_input(self, class_id, month, day, class_desc):
        '''Input for the browser (Schedules flextime)'''
        # time.sleep(0.5)
        # if int(month) < 10:
        #     month = str(0) + str(month)
        # print(class_id, month, day)
        try:
            self.browser.execute_script(f'jQuery("#{class_id}").trigger("click");')
        except:
            return
        # time.sleep(0.5)
        try:
            self.browser.execute_script('jQuery("#addActivity").trigger("click")')
            print(f"activity '{class_desc}' has been scheduled")
            time.sleep(0.5)
        except:
            pass
    def beautiful_soup(self):
        '''Parses HTML for class info, teacher, capacity'''
        print("getting PLT info")
        html = self.browser.page_source

        soup = BeautifulSoup(html, features="lxml")
        data = soup.find_all('tr',attrs={'class':'backtd'})
        teacher_list = []
        for teacher_html in data:
            class_info = teacher_html.contents[2].text
            class_teacher = teacher_html.contents[4].text
            class_capacity = teacher_html.contents[6].text
            class_id = teacher_html.contents[1].contents[1].attrs["for"]
            teacher_dict = {
                "class_info": class_info,
                "class_teacher": class_teacher,
                "class_capacity": class_capacity,
                "class_id": class_id
            }
            teacher_list.append(teacher_dict)
        time.sleep(0.5)
        return teacher_list

new = flextime(google_username, google_password)
# var = new.testing()
# var = new.beautiful_soup()