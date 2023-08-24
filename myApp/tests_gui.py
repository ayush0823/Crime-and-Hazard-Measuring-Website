from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pymongo

# login GUI tests
class LoginGUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(LoginGUITest, self).setUpClass()
        self.client = pymongo.MongoClient("mongodb+srv://crimeandhazard:cnhuser@hostedprojectsdb.xggdbhg.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['swe_test_db']
        self.collection = self.db['users']
        new_user = {'UserName': 'testuser', 'Password': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2000-01-01', 'UpVoted': {}, 'DownVoted': {}}
        self.collection.insert_one(new_user)

    @classmethod
    def tearDownClass(self):
        super(LoginGUITest, self).tearDownClass()
        self.collection.delete_many({'UserName': 'testuser'})

    # test login success
    def test_login(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/login/')
        
        username = selenium.find_element(By.NAME, 'UserName')
        password = selenium.find_element(By.NAME, 'Password')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        password.send_keys('testpass')
        submit.send_keys(Keys.RETURN)

        assert 'myApp/' in selenium.current_url
        selenium.get('http://127.0.0.1:8000/myApp/logout/')
        selenium.quit()

    # test login failure
    def test_login_failure(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/login/')
        
        username = selenium.find_element(By.NAME, 'UserName')
        password = selenium.find_element(By.NAME, 'Password')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        password.send_keys('wrongpass')
        submit.send_keys(Keys.RETURN)

        assert 'Invalid username or password' in selenium.page_source
        selenium.quit()

# change password GUI tests
class ChangePasswordGUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(ChangePasswordGUITest, self).setUpClass()
        self.client = pymongo.MongoClient("mongodb+srv://crimeandhazard:cnhuser@hostedprojectsdb.xggdbhg.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['swe_test_db']
        self.collection = self.db['users']
        new_user = {'UserName': 'testuser', 'Password': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2000-01-01', 'UpVoted': {}, 'DownVoted': {}}
        self.collection.insert_one(new_user)

    @classmethod
    def tearDownClass(self):
        super(ChangePasswordGUITest, self).tearDownClass()
        self.collection.delete_many({'UserName': 'testuser'})

    # test change password success without login
    def test_change_password_without_login(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/changePassword/')
        
        username = selenium.find_element(By.NAME, 'UserName')
        dob = selenium.find_element(By.NAME, 'DOB')
        password = selenium.find_element(By.NAME, 'newPassword')
        confirm_password = selenium.find_element(By.NAME, 'confirmNewPassword')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        dob.send_keys('01-01-2000')
        password.send_keys('newpass')
        confirm_password.send_keys('newpass')
        submit.send_keys(Keys.RETURN)

        assert 'myApp/login/' in selenium.current_url
        selenium.quit()
        self.collection.update_many({'UserName': 'testuser'}, {'$set': {'Password': 'testpass'}})

    # test change password success with login
    def test_change_password_with_login(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/login/')

        username = selenium.find_element(By.NAME, 'UserName')
        password = selenium.find_element(By.NAME, 'Password')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        password.send_keys('testpass')
        submit.send_keys(Keys.RETURN)

        selenium.get('http://127.0.0.1:8000/myApp/changePassword/')

        username = selenium.find_element(By.NAME, 'UserName')
        dob = selenium.find_element(By.NAME, 'DOB')
        password = selenium.find_element(By.NAME, 'newPassword')
        confirm_password = selenium.find_element(By.NAME, 'confirmNewPassword')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        dob.send_keys('01-01-2000')
        password.send_keys('newpass')
        confirm_password.send_keys('newpass')
        submit.send_keys(Keys.RETURN)

        assert 'myApp/profile/' in selenium.current_url
        selenium.get('http://127.0.0.1:8000/myApp/logout/')
        selenium.quit()
        self.collection.update_many({'UserName': 'testuser'}, {'$set': {'Password': 'testpass'}})

    # test change password failure without login (wrong username)
    def test_change_password_without_login_wrong_username(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/changePassword/')
        
        username = selenium.find_element(By.NAME, 'UserName')
        dob = selenium.find_element(By.NAME, 'DOB')
        password = selenium.find_element(By.NAME, 'newPassword')
        confirm_password = selenium.find_element(By.NAME, 'confirmNewPassword')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('wronguser')
        dob.send_keys('01-01-2000')
        password.send_keys('newpass')
        confirm_password.send_keys('newpass')
        submit.send_keys(Keys.RETURN)

        assert 'User does not exist' in selenium.page_source
        assert 'myApp/changePassword/' in selenium.current_url
        selenium.quit()

    # test change password failure without login (wrong dob)
    def test_change_password_without_login_wrong_dob(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/changePassword/')
        
        username = selenium.find_element(By.NAME, 'UserName')
        dob = selenium.find_element(By.NAME, 'DOB')
        password = selenium.find_element(By.NAME, 'newPassword')
        confirm_password = selenium.find_element(By.NAME, 'confirmNewPassword')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        dob.send_keys('01-01-2001')
        password.send_keys('newpass')
        confirm_password.send_keys('newpass')
        submit.send_keys(Keys.RETURN)

        assert 'Incorrect Date of Birth' in selenium.page_source
        assert 'myApp/changePassword/' in selenium.current_url
        selenium.quit()

# edit details GUI tests
class EditDetailsGUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(EditDetailsGUITest, self).setUpClass()
        self.client = pymongo.MongoClient("mongodb+srv://crimeandhazard:cnhuser@hostedprojectsdb.xggdbhg.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['swe_test_db']
        self.collection = self.db['users']
        new_user = {'UserName': 'testuser', 'Password': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2000-01-01', 'UpVoted': {}, 'DownVoted': {}}
        self.collection.insert_one(new_user)

    @classmethod
    def tearDownClass(self):
        super(EditDetailsGUITest, self).tearDownClass()
        self.collection.delete_many({'UserName': 'testuser'})

    # test edit details success
    def test_edit_details_success(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/login/')
        
        username = selenium.find_element(By.NAME, 'UserName')
        password = selenium.find_element(By.NAME, 'Password')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        password.send_keys('testpass')
        submit.send_keys(Keys.RETURN)

        selenium.get('http://127.0.0.1:8000/myApp/editprofile/')

        username = selenium.find_element(By.NAME, 'UserName')
        email = selenium.find_element(By.NAME, 'Email')
        first_name = selenium.find_element(By.NAME, 'FirstName')
        last_name = selenium.find_element(By.NAME, 'LastName')
        dob = selenium.find_element(By.NAME, 'DOB')
        addressline1 = selenium.find_element(By.NAME, 'AddressLine1')
        addressline2 = selenium.find_element(By.NAME, 'AddressLine2')
        locality = selenium.find_element(By.NAME, 'Locality')
        pincode = selenium.find_element(By.NAME, 'Pincode')
        city = selenium.find_element(By.NAME, 'City')
        state = selenium.find_element(By.NAME, 'State')
        country = selenium.find_element(By.NAME, 'Country')
        latitude = selenium.find_element(By.NAME, 'Latitude')
        longitude = selenium.find_element(By.NAME, 'Longitude')
        mobile = selenium.find_element(By.NAME, 'Mobile')
        instagram = selenium.find_element(By.NAME, 'Instagram')
        twitter = selenium.find_element(By.NAME, 'Twitter')
        submit = selenium.find_element(By.NAME, 'submit')

        email.send_keys('newtest@gmail.com')
        first_name.send_keys('newtest')
        last_name.send_keys('newuser')
        dob.send_keys('01-01-2000')
        addressline1.send_keys('newaddress1')
        addressline2.send_keys('newaddress2')
        locality.send_keys('newlocality')
        pincode.send_keys('123456')
        city.send_keys('newcity')
        state.send_keys('newstate')
        country.send_keys('newcountry')
        latitude.send_keys('123')
        longitude.send_keys('456')
        mobile.send_keys('1234567890')
        instagram.send_keys('newinstagram')
        twitter.send_keys('newtwitter')
        submit.send_keys(Keys.RETURN)

        assert 'myApp/profile/' in selenium.current_url
        selenium.get('http://127.0.0.1:8000/myApp/logout/')
        selenium.quit()


# post property GUI tests
class PostPropertyGUITest(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super(PostPropertyGUITest, self).setUpClass()
        self.client = pymongo.MongoClient("mongodb+srv://crimeandhazard:cnhuser@hostedprojectsdb.xggdbhg.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['swe_test_db']
        self.collection = self.db['users']
        new_user = {'UserName': 'testuser', 'Password': 'testpass', 'Email': 'test@gmail.com', 'FirstName': 'test', 'LastName': 'user', 'DOB': '2000-01-01', 'UpVoted': {}, 'DownVoted': {}}
        self.collection.insert_one(new_user)

    @classmethod
    def tearDownClass(self):
        super(PostPropertyGUITest, self).tearDownClass()
        self.collection.delete_many({'UserName': 'testuser'})
        self.collection = self.db['properties']
        self.collection.delete_many({'title': 'testproperty'})

    # test post property success with login
    def test_post_property_success(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/login/')
        
        username = selenium.find_element(By.NAME, 'UserName')
        password = selenium.find_element(By.NAME, 'Password')
        submit = selenium.find_element(By.NAME, 'Submit')

        username.send_keys('testuser')
        password.send_keys('testpass')
        submit.send_keys(Keys.RETURN)

        selenium.get('http://127.0.0.1:8000/myApp/postProperty/')

        title = selenium.find_element(By.NAME, 'Title')
        description = selenium.find_element(By.NAME, 'Description')
        search_text = selenium.find_element(By.ID, 'search-input')
        search_button = selenium.find_element(By.ID, 'search-button')
        latitude = selenium.find_element(By.NAME, 'Latitude')
        longitude = selenium.find_element(By.NAME, 'Longitude')
        price = selenium.find_element(By.NAME, 'price')
        addressline1 = selenium.find_element(By.NAME, 'AddressLine1')
        addressline2 = selenium.find_element(By.NAME, 'AddressLine2')
        city = selenium.find_element(By.NAME, 'City')
        state = selenium.find_element(By.NAME, 'State')
        pincode = selenium.find_element(By.NAME, 'Pincode')
        submit_property = selenium.find_element(By.NAME, 'submit-property')

        title.send_keys('testproperty')
        description.send_keys('testdescription')
        search_text.send_keys('ahmedabad')
        search_button.send_keys(Keys.RETURN)
        # latitude.send_keys('123')
        # longitude.send_keys('456')
        price.send_keys('123456')
        addressline1.send_keys('testaddress1')
        addressline2.send_keys('testaddress2')
        city.send_keys('testcity')
        state.send_keys('teststate')
        pincode.send_keys('123456')
        submit_property.send_keys(Keys.RETURN)

        assert 'myApp/' in selenium.current_url
        selenium.get('http://127.0.0.1:8000/myApp/logout/')
        selenium.quit()

    # test post property failure without login
    def test_post_property_failure(self):
        selenium = webdriver.Edge()
        selenium.get('http://127.0.0.1:8000/myApp/postProperty/')
        
        assert 'myApp/login/' in selenium.current_url
        selenium.quit()