from selenium import webdriver
import time
import pandas as pd

#the following options set Chrome to work in headless mode. If the output is not what desired, the headless mode could be disabled in order to verify what happens on the screen!
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

# at this site you can find info regarding 
# the installation of selenium drivers for your browser  https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
# here in the example it is used Chrome as browser
# in the path of windows the full path of the EXE file must be specified


chrome_driver_path = "/usr/bin/chromedriver" #default chromedriver as usually set in ubuntu
#add your windows path to chromedriver here as chrome_driver_path = "C:/temp/chromedriver.exe"



driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)
driver.get("https://www.investing.com/technical/technical-analysis")



try:
    privacy_accept=driver.find_element("xpath",'//*[@id="onetrust-accept-btn-handler"]');
    privacy_accept.click()
    print("Closed first Pop Up")
except: 
    print("Issues with the first popup")
try:
    NoThanks=driver.find_element("xpath", "/html/body/div[5]/header/div[1]/div/div[4]/div[2]/div[3]/div/div[3]/a[1]");
    NoThanks.click()
    print("Closed second Pop Up")
except: 
    print("Issues with the second popup")

element = driver.switch_to.active_element

#all of the following variables are meant to keep track of the closed pop-ups. Be aware that there might be many more!
check_login_closed=False
check_advice_closed=False
check_notification_closed=False

def check_login_popup():
    try:
        ClosePopUp=driver.find_element("xpath", '//*[@id="PromoteSignUpPopUp"]/div[2]/i');
        ClosePopUp.click()
        print("Closed Login Pop Up")
        check_login_closed=True
    except:
        print("Login pop up not found")    
    return 

def check_advice_popup():
    try:
        ClosePopUp=driver.find_element("xpath", 
        '/html/body/div[5]/aside/div[2]/div/div/div/div/div[2]/div/div[1]/div[1]/div[2]');
        ClosePopUp.click()
        print("Closed Advice Pop Up")
        check_advice_closed=True
    except:
        print("Advice pop up not found")    
    return 

def check_notification_popup():
    try:
        ClosePopUp=driver.find_element("xpath", 
        '/html/body/div[6]/div/button');
        ClosePopUp.click()
        print("Closed Notification Pop Up")
        check_notification_closed=True
    except:
        print("Notification pop up not found")    
    return 



check_login_popup()
check_advice_popup()
check_notification_popup()


# to find the xpath of an element, click "inspect" and then, selecting the html code, right-click and then "copy full xpath"
# this works with Firefox and Chrome 
#following, the base xpaths to find in selenium the pair and the time-period 

pair_xpath_base='//*[@id="pairSublinksLevel2"]' 
pair_table='//*[@id="curr_table"]'
daily_xpath='/html/body/div[5]/section/div[6]/ul/li[7]'

#initialization of the collection of the data for pair
dict_coll=[]

#the first item in the web page is not clickcable and this may cause errors. Therefore, the order of scraping the pairs is shifted
range_pair_order=[x for x in range (1,9)]
range_pair_order=range_pair_order[1:]+range_pair_order[:1]

for pair in range_pair_order:
    
        
    pair_xpath_li=f"{pair_xpath_base}/li[{pair}]/a"
            
    click=False
    while click==False:
                try:
                    if check_login_closed==False: #between pairs , we try to close the login pop up
                        check_login_popup()
                    if check_advice_closed==False: #between pairs , we try to close the advice pop up
                        check_advice_popup()
                    if check_notification_closed==False: #between pairs , we try to close the advice pop up
                        check_notification_popup()                    

                    pair_to_click=driver.find_element("xpath", pair_xpath_li)
                    pair_to_click.click()
                    click=True
                except Exception as error:
                    time.sleep(1)
                    print(f"Exception: {error} with pair n.{pair} - {data_period}")    
    
    data_periods=['3600','86400']

    for data_period in data_periods:
        
        if data_period=='86400':
            try:
                daily_tab=driver.find_element("xpath", daily_xpath)
                daily_tab.click()
                time.sleep(3)
            except Exception as error:    
                print(f"Exception: {error} in clicking on Daily")    

        classic=[]
        for x in range (2,9):
            try:
                a=driver.find_element("xpath", f"{pair_table}/tbody/tr[1]/td[{x}]").text
                classic.append(a)
            except Exception as error:   
                print(f"Exception: {error} in scraping classic pivot points")
            
        check_scraping=False
        while check_scraping==False:             
            try:
                pair_name=driver.find_element("xpath", '//*[@id="quoteLink"]').text.replace("/","_")
                update_time=driver.find_element("xpath",'//*[@id="updateTime"]').text
                last_actual=driver.find_element("xpath",'/html/body/div[5]/section/div[8]/div[1]/div[1]/div[1]').text
                maBuy=driver.find_element("xpath",'/html/body/div[5]/section/div[8]/div[1]/div[2]/div[2]/span[2]/i[2]').text
                maSell=driver.find_element("xpath",'/html/body/div[5]/section/div[8]/div[1]/div[2]/div[2]/span[3]/i[2]').text
                ti_Buy=driver.find_element("xpath",'/html/body/div[5]/section/div[8]/div[1]/div[2]/div[3]/span[2]/i[2]').text
                ti_Sell=driver.find_element("xpath",'/html/body/div[5]/section/div[8]/div[1]/div[2]/div[3]/span[3]/i[2]').text

                pair_dict=dict(pair_name=pair_name,
                    data_period=data_period,
                    update_time=update_time,
                    last_actual=last_actual,
                    Ma_Buy=maBuy,
                    Ma_Sell=maSell,
                    ti_Buy=ti_Buy,
                    ti_Sell=ti_Sell,
                    S3=classic[0],
                    S2=classic[1],
                    S1=classic[2],
                    Pivot=classic[3],
                    R1=classic[4],
                    R2=classic[5],
                    R3=classic[6]
                )
            except Exception as error:
                print(f"Exception: {error} in scraping parameters with pair {pair_name}")
            
            if pair_name == "":
                time.sleep(5)
            else:
                check_scraping=True    
            
            print(pair_dict)
            dict_coll.append(pair_dict)

df=pd.DataFrame(dict_coll)
df.to_excel("investing.xlsx")



