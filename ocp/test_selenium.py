'''
    Created By : Christian Merriman
    Date : 3/27/26
    Purpose : Run tests with selenium to make sure the website works correctly.
    Covers most of the site such as menu navigation. Logging in and out. User profiles. Upgrading user access_levels.
    Doesn't cover the following because lots of variables for these, with connecting to Ollama and ComfyUI. Can be tested manually for now. :
        -Chatting with ED-209   -Connection to Ollama
        -ED-209 Image Creation  -Connection to COMFYUI
        -Asset Page Commenting  -Will show the images assets from COMFYUI and can comment on them

    
'''
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import connections, transaction

from selenium import webdriver
#from selenium.webdriver.firefox.options import Options

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException





#from selenium.webdriver.firefox.service import Service
#from webdriver_manager.firefox import GeckoDriverManager

from typing import Any
import time
import unittest
import os


#used so i do not have to retest ones that work, when adding new tests
#SET TO
#  True to run everything 
#  False to only run new ones that do not have this : @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
RUN_SELENIUM_TESTS = True
HEADLESS = True

class NonMemberUITests(StaticLiveServerTestCase):
    
    '''
        Setup Selenium (firefox now)
    '''
    @classmethod
    def setUpClass(cls):
        try:
            super().setUpClass()

            options = Options()

            # Headless mode for CI
            if os.environ.get("GITHUB_ACTIONS") == "true" or HEADLESS:
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")

            # Required for GitHub Actions stability
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")

            # DO NOT set binary location unless needed
            # DO NOT use Service()
            # Let Selenium Manager handle everything

            cls.driver = webdriver.Chrome(options=options)

            cls.driver.implicitly_wait(10)

        except Exception as e:
            print("SETUPCLASS FAILED:", e)
            raise


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    '''
        Helper Functions
    '''

    #this will login the user by sending in a user name, password and access_level (has defaults)
    #will return the created user to use
    def login(self, CREATE_USER : bool = True, username : str = "testuser", password : str = "testpassword123", access_level : int = 1)->Any:
        
        #github will not work without this. it wont logout previous user quick enough.
        #resets the browser session state for the driver
        self.driver.delete_all_cookies()
        self.driver.get("about:blank")

        if CREATE_USER:
            #create a temporary user in the test database
            User = get_user_model()
            new_user = User.objects.create_user(
                                                username=username, 
                                                password=password,
                                                access_level=access_level
                                        )
            
        else:
            new_user = None

        #go to the index page
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        #now head to the login page
        wait.until(EC.element_to_be_clickable((By.ID, "signInDropDown"))).click()
        
        #find sign in page
        items = self.driver.find_elements(By.CLASS_NAME, "dropdown-item")
        for item in items:
            if "Sign In" in item.get_attribute("textContent"):
                self.driver.execute_script("arguments[0].click();", item)
                break

        #now fill out the information
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        
        #submit it
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Login']")))
        self.driver.execute_script("arguments[0].click();", login_button)
        
        #lets verify we logged on
        wait = WebDriverWait(self.driver, 10)

        #wait until dashboard loads so we know we are logged on
        wait.until(EC.url_contains('/dashboard'))

        return new_user
    
    # this will login the user by sending in a user name, password and access_level (has defaults)
    # will return the created user to use
    def logingpt(self, CREATE_USER: bool = True, username: str = "testuser", password: str = "testpassword123", access_level: int = 1) -> Any:
        
        if CREATE_USER:
            # create a temporary user in the test database
            User = get_user_model()
            new_user = User.objects.create_user(
                username=username,
                password=password,
                access_level=access_level
            )
        else:
            new_user = None

        # go to the index page
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        # open dropdown
        wait.until(EC.element_to_be_clickable((By.ID, "signInDropDown"))).click()
        
        # Wait for dropdown items to be visible
        items = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "dropdown-item")))

        for item in items:
            if "Sign In" in item.text:
                wait.until(EC.element_to_be_clickable(item))
                item.click()
                break

        # fill out form
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        
        # submit form
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Login']")))
        login_button.click()   # ✅ FIXED (no JS)

        # DEBUG INFO
        print("AFTER LOGIN CLICK URL:", self.driver.current_url)

        # wait for redirect (more reliable)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: "/dashboard" in driver.current_url)

        print("FINAL URL:", self.driver.current_url)

        return new_user

    #must run login before running this
    def logout(self):
        self.click_navigation(
                    start_at="dashboard",
                    dropdown="settingsDropdown",
                    contained="Log Out",
                    notwaitfor="dashboard"
        )

    #used for clicking navigations
    #sends in the user, if we need the user id
    #send in what page to start at (default index), the dropdown menu, what we are looking to click and what page we are waiting to load or the page you are waiting to change
    #can send in None for start_at, if you do not need it to start at a page
    def click_navigation(self, user : Any = None, start_at : str = "index", dropdown : str = None, contained : str = None, waitfor : str = None, notwaitfor : str = None):
        #make sure we want to start some place
        if start_at:
            #start at index
            self.driver.get(self.live_server_url + reverse(start_at))
        wait = WebDriverWait(self.driver, 10)

        #open the drop down for this element
        wait.until(EC.element_to_be_clickable((By.ID, dropdown))).click()

        #find the clickable item we are looking for
        items = self.driver.find_elements(By.CLASS_NAME, "dropdown-item")
        for item in items:
            if contained in item.get_attribute("textContent"):
                self.driver.execute_script("arguments[0].click();", item)
                break
        
        #verify by if we are waiting to contain or not contain a page
        if waitfor:
            if user and waitfor == 'user_profile':
                url = reverse('user_profile', args=[user.id])
                wait.until(EC.url_contains(url))
            else:
                wait.until(EC.url_contains(reverse(waitfor)))
        elif notwaitfor:
            wait.until_not(EC.url_contains(notwaitfor))

    #this will create a list of users needed
    #send in the max users to make, with their name, password and access level
    #will return the list of users made
    def create_users(self, max_users : int = 1, name : str = "user", pw : str = "123", access_level : int = 1)->list:
        the_users = []

        wait = WebDriverWait(self.driver, 10)

        for i in range(max_users):
            #pause before we begin
            #time.sleep(1)
            wait.until(lambda d: True)

            #setup our maxxed out user and create
            new_name = f"{name}{i}"

            #create our new user
            new_user = self.login(
                                    username=new_name,
                                    password=pw,
                                    access_level=access_level
                                )

            #sleep then logout
            #time.sleep(1)
            wait.until(EC.url_contains("/dashboard"))
            self.logout()
            wait.until(EC.url_contains("/"))

            #now add the user to our list
            the_users.append(new_user)

        return the_users
    
    def security_settings_name_search(self, FULL_NAME : bool = True):
        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        #setup our maxxed out user and create
        user_name = "max"
        user_pw = "max"
        user_access_level = 5 #may change to 3, 4 or 5
        
        max_user = self.login(
                            username=user_name,
                            password=user_pw,
                            access_level=user_access_level)


        #sleep then logout
        #time.sleep(1)
        wait.until(EC.url_contains("/dashboard"))
        self.logout()
        wait.until(EC.url_contains("/"))

        #users to be created, make sure its 2 under the access level
        #example: 5 - 2 = 3. We only need 3 users because they will all start at 1 and can only go to 2, 3 and 4. Never the same access level as the user, this case 5.
        #also make sure it never falls below 1
        user_num = 1

        #now create user_num of users to test and sleep
        the_users = self.create_users(max_users=user_num)
        #time.sleep(1)

        #login our level 5 user
        self.login(         
                            CREATE_USER=False,
                            username=user_name,
                            password=user_pw,
                            access_level=user_access_level
                    )
        
        #now goto our secutiry settings
        self.click_navigation(
                    user=max_user,
                    start_at=None,
                    dropdown="settingsDropdown",
                    contained="Security Settings",
                    waitfor="security_settings"
        )

        #find the search
        search_box = wait.until(EC.presence_of_element_located((By.ID, "personnelSearch")))

        #type in the name to search, check to see if we use full or partial name
        if FULL_NAME:
            target_name = the_users[0].username
            search_box.send_keys(target_name)
        else:
            target_name = the_users[0].username
            len_name = len(target_name)
            len_use = max(1,abs(len_name-2))
            search_box.send_keys(target_name[:len_use])

        #press enter
        search_box.send_keys(Keys.ENTER)

        #wait for load
        #time.sleep(1)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#personnelTable tbody"))
        )

        #now see if we can find it
        #self.assertIn(target_name.upper(), self.driver.page_source.upper())

        # Check that the name appears specifically inside the personnelTable <tbody>
        table_body = self.driver.find_element(By.CSS_SELECTOR, "#personnelTable tbody")
        self.assertIn(target_name.upper(), table_body.text.upper())
    
    '''
        Test Functions
    '''    

    #make sure we are on the index page
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_indexpage(self):
        
        self.driver.get(self.live_server_url + reverse('index'))

        #check to see if we are on index
        expected_url = self.live_server_url + reverse('index')
        self.assertEqual(self.driver.current_url, expected_url)

    #make sure our title is correct
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_homepage_load_and_title(self):
        #get the index
        self.driver.get(self.live_server_url + reverse('index'))
        
        #check browsers title
        self.assertIn("OCP", self.driver.title)

    '''
    Check navigation links below
    '''
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_navigation_to_comingsoon(self):
        self.click_navigation(
                    dropdown="servicesDropDown",
                    contained="Coming Soon",
                    waitfor="comingsoon"
        )  

        #now verify it on page
        self.assertIn("comingsoon", self.driver.current_url)

    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_navigation_to_products(self):
        self.click_navigation(
                    dropdown="servicesDropDown",
                    contained="Products",
                    waitfor="currentproducts"
        )  
        
        #verify
        self.assertIn("currentproducts", self.driver.current_url)

    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_navigation_to_employment(self):
        self.click_navigation(
                    dropdown="employmentDropDown",
                    contained="Join Us",
                    waitfor="employment"
        )

        #verify
        self.assertIn("employment", self.driver.current_url)

    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_navigation_to_aboutocp(self):
        self.click_navigation(
                    dropdown="aboutDropDown",
                    contained="About",
                    waitfor="about"
        )

        #verify
        self.assertIn("about", self.driver.current_url)

    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_navigation_to_mission_statement(self):
        self.click_navigation(
                    dropdown="aboutDropDown",
                    contained="Mission",
                    waitfor="mission"
        )

        #verify
        self.assertIn("mission", self.driver.current_url)

    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_navigation_to_signin(self):
        self.click_navigation(
                    dropdown="signInDropDown",
                    contained="Sign In",
                    waitfor="login"
        )

        #verify
        self.assertIn("login", self.driver.current_url)

    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_guest_navigation_to_register(self):
        self.click_navigation(
                    dropdown="signInDropDown",
                    contained="Register",
                    waitfor="register"
        )

        #verify
        self.assertIn("register", self.driver.current_url)

    #test the logo if it goes to index
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_brand_logo_returns_to_home(self):
        #start diff page
        self.driver.get(self.live_server_url + reverse('mission'))
        
        #find the logo and click
        logo = self.driver.find_element("class name", "nav-logo")
        logo.click()
        
        #make sure it worked
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('index'))

    #test the omni consumer products link if it goes to index
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_ocptextlink_returns_to_home(self):
        #start diff page
        self.driver.get(self.live_server_url + reverse('mission'))
        
        #find the logo and click
        ocptextlink = self.driver.find_element(By.ID, "ocp-text-id")
        ocptextlink.click()
        
        #make sure it worked
        self.assertEqual(self.driver.current_url, self.live_server_url + reverse('index'))


    #test user login
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_flow(self):
        self.login()
        
        #lets verify we logged on
        wait = WebDriverWait(self.driver, 10)
        
        #make sure we are on the dashboard
        self.assertIn("/dashboard", self.driver.current_url)

    #test user login
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_flow_username_password(self):
        self.login(
                    username="bubba",
                    password="gump"
                )
        
        #lets verify we logged on
        wait = WebDriverWait(self.driver, 10)
        
        #make sure we are on the dashboard
        self.assertIn("/dashboard", self.driver.current_url)

    #test user login error
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_flow_username_password_error(self):
        username ="bubba"
        password = ""

        #go to the index page
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        #now head to the login page
        wait.until(EC.element_to_be_clickable((By.ID, "signInDropDown"))).click()
        
        #find sign in page
        items = self.driver.find_elements(By.CLASS_NAME, "dropdown-item")
        for item in items:
            if "Sign In" in item.get_attribute("textContent"):
                self.driver.execute_script("arguments[0].click();", item)
                break

        #now fill out the information
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        
        #submit it
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Login']")))
        self.driver.execute_script("arguments[0].click();", login_button)

        #wait for it to appear so we know the page reloaded
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid username')]")))
        
        #make sure we are on the login still
        self.assertIn("/login", self.driver.current_url)

        #make sure we received an error
        self.assertIn("Invalid username and/or password.", self.driver.page_source)

    #this will test registering users
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_register_flow(self):
        #go to the index page
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        #navigate to register
        self.click_navigation(
                    start_at=None,
                    dropdown="signInDropDown",
                    contained="Register",
                    waitfor="register"
        )

        wait = WebDriverWait(self.driver, 10)

        username = "user1"
        email = "user1@user1.com"
        pw ="123"

        #get the boxes and then fill them in
        name_box = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        email_box = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        password_box = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        confirm_password_box = wait.until(EC.presence_of_element_located((By.NAME, "confirmation")))

        #now enter our values in the input fields
        name_box.send_keys(username)
        email_box.send_keys(email)
        password_box.send_keys(pw)
        confirm_password_box.send_keys(pw)

        #get current page
        old_page = self.driver.find_element(By.TAG_NAME, 'html')

        #get the input button to click and submit for register
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Register']"))).click()

        #wait until we leave this page
        wait.until(EC.staleness_of(old_page))

        #now check to make sure the new html as loaded
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-title")))

        #verify this is the dashboard html page
        self.assertIn("OCP DASHBOARD", self.driver.page_source)

    #this will test registering user errors
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_register_error_flow(self):
        #go to the index page
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        #navigate to register
        self.click_navigation(
                    start_at=None,
                    dropdown="signInDropDown",
                    contained="Register",
                    waitfor="register"
        )

        wait = WebDriverWait(self.driver, 10)

        #this will loop through 3 different empty conditions that will cause an error
        #dont need to do email, because email has to be valid for it to go through
        for i in range(3):
            
            #blank name
            if i == 0:
                username = "    "
                email = "user1@user1.com"
                pw ="123"
                pwconfirmation ="123"
            #blank pw
            elif i == 1:
                username = "joe"
                email = "user1@user1.com"
                pw ="    "
                pwconfirmation ="123"
            #blank pw confirmation
            else:
                username = "joe"
                email = "user1@user1.com"
                pw ="123"
                pwconfirmation ="    "

            #get the boxes and then fill them in
            name_box = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            email_box = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            password_box = wait.until(EC.presence_of_element_located((By.NAME, "password")))
            confirm_password_box = wait.until(EC.presence_of_element_located((By.NAME, "confirmation")))

            #now enter our values in the input fields
            name_box.send_keys(username)
            email_box.send_keys(email)
            password_box.send_keys(pw)
            confirm_password_box.send_keys(pwconfirmation)

            #get current page
            old_page = self.driver.find_element(By.TAG_NAME, 'html')

            #get the input button to click and submit for register
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Register']"))).click()

            #wait until we leave this page
            wait.until(EC.staleness_of(old_page))

            #now check to make sure the new html as loaded
            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Error"))

            #verify this is the dashboard html page
            self.assertIn("Error", self.driver.page_source)

            #sleep
            #time.sleep(1)

    #run login and then run logout
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_logout_flow(self):
        self.login()   

        #lets verify we logged on
        wait = WebDriverWait(self.driver, 10)

        self.logout()

        #lets verify we logged out
        wait = WebDriverWait(self.driver, 10)

        #check to see if we are on index
        expected_url = self.live_server_url + reverse('index')
        self.assertEqual(self.driver.current_url, expected_url)

    #test user menu dashboard
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_dashboard(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        self.login()

        self.click_navigation(
                    start_at=None,
                    dropdown="terminalDropdown",
                    contained="Dashboard",
                    waitfor="dashboard"
        )

        #verify
        self.assertIn("dashboard", self.driver.current_url)

    #test user menu assetfeed
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_assetfeed(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        self.login()

        self.click_navigation(
                    start_at=None,
                    dropdown="terminalDropdown",
                    contained="Asset Feed",
                    waitfor="assetfeed"
        )

        #verify
        self.assertIn("assetfeed", self.driver.current_url)

    #test user menu assetfeed
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_assetfeed_empty(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        self.login()

        self.click_navigation(
                    start_at=None,
                    dropdown="terminalDropdown",
                    contained="Asset Feed",
                    waitfor="assetfeed"
        )

        #verify on page
        self.assertIn("assetfeed", self.driver.current_url)

        #find the text for empty class and see if it has no assets
        text = self.driver.find_element(By.CLASS_NAME, "empty-state").text
        self.assertIn("NO ASSETS", text)

    #test user menu chat
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_chat(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        self.login()

        self.click_navigation(
                    start_at=None,
                    dropdown="directivesDropdown",
                    contained="Chat Interface",
                    waitfor="chat"
        )

        #verify
        self.assertIn("chat", self.driver.current_url)

    #test user menu image_creation
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_image_creation(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        self.login()

        self.click_navigation(
                    start_at=None,
                    dropdown="directivesDropdown",
                    contained="Vision Generator",
                    waitfor="image_creation"
        )

        #verify
        self.assertIn("image_creation", self.driver.current_url)

    #test user menu user profile
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_user_profile(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        user = self.login()

        self.click_navigation(
                    user=user,
                    start_at=None,
                    dropdown="settingsDropdown",
                    contained="Profile",
                    waitfor="user_profile"
        )

        #verify
        self.assertIn("user_profile", self.driver.current_url)

    #test user menu user profile
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_user_profile_access_levels(self):
        #go through and test all acesss levels 1 - 5
        max_acces_level = 5
        for i in range(1,max_acces_level+1):

            #start at index
            self.driver.get(self.live_server_url + reverse('index'))
            wait = WebDriverWait(self.driver, 10)

            #login and create our i user
            user = self.login(
                                username=f"testuser_{i}",
                                access_level=i)

            self.click_navigation(
                        user=user,
                        start_at=None,
                        dropdown="settingsDropdown",
                        contained="Profile",
                        waitfor="user_profile"
            )

            #verify
            self.assertIn("user_profile", self.driver.current_url)

            #check to see if we have the right access level
            self.assertIn(f"LEVEL {i}:", self.driver.page_source)

            #pause then logout
            #time.sleep(1)
            self.logout()

            #if we need to pause for next loop
            #if i < max_acces_level:
            #    time.sleep(1)

    #test user menu user profile
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_security_settings(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        user = self.login(access_level=5)

        self.click_navigation(
                    user=user,
                    start_at=None,
                    dropdown="settingsDropdown",
                    contained="Security Settings",
                    waitfor="security_settings"
        )

        #verify
        self.assertIn("security_settings", self.driver.current_url)

    #tests to see if our security settings search box works with a full name
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_security_settings_user_full_name_search(self):
        self.security_settings_name_search(FULL_NAME=True)

    #tests to see if our security settings search box works with a partial name
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_security_settings_user_partial_name_search(self):
        self.security_settings_name_search(FULL_NAME=False)

    #this will test to see if we can change the users access levels
    @unittest.skipUnless(RUN_SELENIUM_TESTS, "SELENIUM tests are currently disabled")
    def test_login_menu_security_settings_update_access_level(self):

        #start at index
        self.driver.get(self.live_server_url + reverse('index'))
        wait = WebDriverWait(self.driver, 10)

        #setup our maxxed out user and create
        user_name = "max"
        user_pw = "max"
        user_access_level = 5 #may change to 3, 4 or 5
        
        max_user = self.login(
                            username=user_name,
                            password=user_pw,
                            access_level=user_access_level)


        #sleep then logout
        #time.sleep(1)
        wait.until(EC.url_contains("/dashboard"))
        self.logout()
        wait.until(EC.url_contains("/"))

        #users to be created, make sure its 2 under the access level
        #example: 5 - 2 = 3. We only need 3 users because they will all start at 1 and can only go to 2, 3 and 4. Never the same access level as the user, this case 5.
        #also make sure it never falls below 1
        user_num = max(1,abs(max_user.access_level - 2))

        #now create user_num of users to test and sleep
        the_users = self.create_users(max_users=user_num)
        #time.sleep(1)

        #login our level 5 user
        self.login(         
                            CREATE_USER=False,
                            username=user_name,
                            password=user_pw,
                            access_level=user_access_level
                    )
        
        wait.until(EC.url_contains("/dashboard"))
        
        #now goto our secutiry settings
        self.click_navigation(
                    user=max_user,
                    start_at=None,
                    dropdown="settingsDropdown",
                    contained="Security Settings",
                    waitfor="security_settings"
        )

        #must be at least access level 3 to upgrade
        if max_user.access_level >= 3:

            # Loop through your 3 created users
            # We want to set them to levels 2, 3, and 4 respectively
            for index, target_user in enumerate(the_users):
                new_level = index + 2  # This will give us 2, 3, then 4
                
                # 1. Locate the specific row for this username
                # This XPath finds a <tr> that has a <td> containing the username
                row_xpath = f"//tr[td[contains(., '{target_user.username.upper()}')]]"
                row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

                # 2. Find the dropdown (select) and button within that row
                dropdown = Select(row.find_element(By.CLASS_NAME, "ocp-select"))
                submit_btn = row.find_element(By.CLASS_NAME, "update-btn")

                # 3. Select the level (using value string)
                dropdown.select_by_value(str(new_level))

                # 4. Click Submit
                submit_btn.click()

                # 5. HANDLE THE CONFIRMATION POPUP
                # Your HTML has an 'onsubmit' confirm dialog. We must accept it.
                wait.until(EC.alert_is_present())
                self.driver.switch_to.alert.accept()

                # 6. Verify the page reloaded and shows the new level badge
                # We wait for the specific badge text to appear on the page
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, f"level-{new_level}")))
                
                print(f"Successfully promoted {target_user.username} to Level {new_level}")

                #now test level max_user.access_level (3, 4 or 5)
                if new_level == max_user.access_level - 1 :
                    max_level = max_user.access_level
                    # 1. Locate the specific row for this username
                    # This XPath finds a <tr> that has a <td> containing the username
                    row_xpath = f"//tr[td[contains(., '{target_user.username.upper()}')]]"
                    row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

                    # 2. Find the dropdown (select) and button within that row
                    dropdown = Select(row.find_element(By.CLASS_NAME, "ocp-select"))
                    submit_btn = row.find_element(By.CLASS_NAME, "update-btn")

                    try:
                        row.find_element(By.XPATH, f".//option[@value='{max_level}']")
                        self.fail(f"Security Acess Level {max_level} should not be available!")
                    except NoSuchElementException:
                        print(f"Security Access Level {max_level} was successfully not found!")
                        continue
    