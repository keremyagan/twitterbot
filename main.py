#Kerem YAGAN
#https://github.com/keremyagan
from selenium import webdriver
from selenium import common
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup


class TwitterBot:
    def __init__(self, email, password,proxy):
        self.email = email
        self.password = password
        self.proxy=proxy
        webdriver.DesiredCapabilities.CHROME['proxy']={
            "httpProxy":self.proxy,
            "ftpProxy":self.proxy,
            "sslProxy":self.proxy,  
            "proxyType":"MANUAL",    
        }
        options = Options()
        options.headless = True
        self.bot = webdriver.Chrome(options=options)
        self.is_logged_in = False

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(4)

        try:
            email = bot.find_element_by_name('session[username_or_email]')
            password = bot.find_element_by_name('session[password]')
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            email = bot.find_element_by_name('session[username_or_email]')
            password = bot.find_element_by_name('session[password]')
        
        email.clear()
        password.clear()
        email.send_keys(self.email)
        password.send_keys(self.password)
        password.send_keys(keys.Keys.RETURN)
        time.sleep(10)
        self.is_logged_in = True

    def logout(self):
        if not self.is_logged_in:
            return 

        bot = self.bot
        bot.get('https://twitter.com/home')
        time.sleep(4)

        try:
            bot.find_element_by_xpath("//div[@data-testid='SideNav_AccountSwitcher_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@data-testid='SideNav_AccountSwitcher_Button']").click()

        time.sleep(1)

        try:
            bot.find_element_by_xpath("//a[@data-testid='AccountSwitcher_Logout_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(2)
            bot.find_element_by_xpath("//a[@data-testid='AccountSwitcher_Logout_Button']").click()

        time.sleep(3)

        try:
            bot.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()

        time.sleep(3) 
        self.is_logged_in = False

    def hashtag_tweets_likes(self,hashtag,scroll_number):
        driver=self.bot
        driver.get(f'https://twitter.com/search?q=%23{hashtag}&src=typeahead_click')
        time.sleep(4)
        # to scroll through the twitter hashtag timeline
        for i in range(scroll_number):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)


        # Get the links of each tweets on the twitter profile account
        tweet_xpath = '//div[@data-testid="tweet"]'
        tweet_links_xpath = '//a[@href]' 
        tweet_link = driver.find_elements_by_xpath(tweet_links_xpath)
        elements = driver.find_elements_by_xpath(tweet_xpath)
        tweets = [tweet.get_attribute("href") for tweet in tweet_link]
        main_tweets = set(())
        for i in tweets:
            if '/status/' in i and '/photo/' not in i:
                main_tweets.add(i)
            else:
                pass

        print(main_tweets)

        # Like tweets

        for tweets in main_tweets:
            driver.get(tweets)
            driver.switch_to_active_element()
            time.sleep(3)
            like = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="like"]')))
            like.click()
            time.sleep(2)
   
    def post_tweets(self,tweetBody):
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        bot = self.bot  

        try:
            bot.find_element_by_xpath("//a[@data-testid='SideNav_NewTweet_Button']").click()
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//a[@data-testid='SideNav_NewTweet_Button']").click()

        time.sleep(4) 
        body = tweetBody

        try:
            bot.find_element_by_xpath("//div[@role='textbox']").send_keys(body)
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            bot.find_element_by_xpath("//div[@role='textbox']").send_keys(body)

        time.sleep(4)
        bot.find_element_by_class_name("notranslate").send_keys(keys.Keys.ENTER)
        bot.find_element_by_xpath("//div[@data-testid='tweetButton']").click()
        time.sleep(4) 

    def follow(self,username):
        try:
            url="https://twitter.com/"+username
            driver=self.bot
            driver.get(url)
            time.sleep(3)
            try:
                driver.refresh()
                time.sleep(3)
                driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div/div').click()
            except Exception as err:
                print("1")
                print(err)
        except Exception as err:
            print(err)
            
    def retweet(self,url):
        driver=self.bot
        driver.get(url)
        time.sleep(3)
        while True:
            try:
                driver.refresh()
                time.sleep(3)
                driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[5]/div[2]').click()
                time.sleep(2)
                try:
                    driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/a[1]/div/span').click()
                    time.sleep(2)
                except:
                    pass
                
                driver.find_element_by_xpath('//*[@id="layers"]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div/div[2]/div').click()
                time.sleep(2)     
                break
            except Exception as err:
                print(err) 

    def like_from_url(self,url):
        bot=self.bot
        bot.get(url)
        time.sleep(3)
        while True:
            try:
                bot.get(url)
                time.sleep(3)
                bot.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/section/div/div/div[1]/div/div/article/div/div/div/div[3]/div[5]/div[3]/div/div/div').click()
                break
            except Exception as err:
                print(err)
 

file=open("hesaplar.txt","r")
icerik=file.readlines()
file.close()

while True:
    islem_no=input("1-Hashtag ile Tweet Beğenme\n2-Tweet Paylaşma\n3-Takip Etme\n4-Retweets\n5-Like\n6-Çıkış\nSeçiminiz:")
    if islem_no=="1":
        hashtag=input("Hashtag Adını Giriniz:")
        proxy_number=0
        for i in icerik:
            username=i.split()[0]
            password=i.split()[1]
            proxy="185.204.187.111:1580"+str(proxy_number)+":15900:ZweQwb:ZweQwb"
            a=TwitterBot(username,password,proxy)
            a.login()
            a.hashtag_tweets_likes(hashtag,10)
            proxy_number=proxy_number+1
            a.logout()
    elif islem_no=="2":
        tweet=input("Tweet İçeriğini Giriniz:")
        proxy_number=0
        for i in icerik:
            username=i.split()[0]
            password=i.split()[1]
            proxy="185.204.187.111:1580"+str(proxy_number)+":15900:ZweQwb:ZweQwb"
            a=TwitterBot(username,password,proxy)
            a.login()
            a.post_tweets(tweet)
            proxy_number=proxy_number+1
            a.logout()    
    elif islem_no=="3":
        user=input("Takip Edilecek Kişinin Kullanıcı Adını Giriniz:")
        proxy_number=0
        for i in icerik:
            username=i.split()[0]
            password=i.split()[1]
            proxy="185.204.187.111:1580"+str(proxy_number)+":15900:ZweQwb:ZweQwb"
            a=TwitterBot(username,password,proxy)
            a.login()
            a.follow(user)
            proxy_number=proxy_number+1
            a.logout()     
    elif islem_no=="4":
        url=input("Retweet Yapılacak URLyi Giriniz:")
        proxy_number=0
        for i in icerik:
            username=i.split()[0]
            password=i.split()[1]
            proxy="185.204.187.111:1580"+str(proxy_number)+":15900:ZweQwb:ZweQwb"
            a=TwitterBot(username,password,proxy)
            a.login()
            a.retweet(url)
            proxy_number=proxy_number+1
            a.logout()    
    elif islem_no=="5":
        url=input("Beğeni Yapılacak URLyi Giriniz:")
        proxy_number=0
        for i in icerik:
            username=i.split()[0]
            password=i.split()[1]
            proxy="185.204.187.111:1580"+str(proxy_number)+":15900:ZweQwb:ZweQwb"
            a=TwitterBot(username,password,proxy)
            a.login()
            a.like_from_url(url)
            proxy_number=proxy_number+1
            a.logout()         
    elif islem_no=="6": 
        break
    

