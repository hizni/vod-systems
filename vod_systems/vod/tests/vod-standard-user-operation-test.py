from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth.models import User
from vod.models import Institution, Datatype, Transplant_Type, Alias_Identifier, User_Institution
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


class MySeleniumTests2(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        # self.selenium.implicitly_wait(3)

        # create user
        User.objects.create_user('user', 'user@mysite.com', 'userpassword')

        # create meta data
        # Institutions
        Institution.objects.create(code='*', description='default institution')
        Institution.objects.create(code='OUH', description='Oxford University Hospitals NHS FT')
        Institution.objects.create(code='IMP', description='Imperial University Hospitals NHS')

        # User-Institutions
        User_Institution.objects.create(fk_user_id_id='1', fk_institution_id_id='5')

        # Datatype
        Datatype.objects.create(code='clinical-symptoms', description='Time since first clinical symptoms of SOS/VOD', unit='days')
        Datatype.objects.create(code='weight-kilos', description='Measures the weight in kilos', unit='kg')
        Datatype.objects.create(code='painful-hepatomegaly', description='Patient has an enlarged liver that is painful', unit='boolean')

        # Transplant type
        Transplant_Type.objects.create(code='Autograft', description='Autograft')
        Transplant_Type.objects.create(code='Allograft', description='Allograft')

        #Alias Identifier
        Alias_Identifier.objects.create(code='nhs-number', description='NHS Number')
        Alias_Identifier.objects.create(code='local-mrn', description='Local Hospital ID')
        Alias_Identifier.objects.create(code='ris-id', description='Radiology System ID')

        super(MySeleniumTests2, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(MySeleniumTests2, self).tearDown()

    def test_user_failed_login_incorrect(self):
        selenium = self.selenium

        # Opening the link we want to test
        selenium.get('http://localhost:8081/vod/login/')

        assert "/vod/login/" in self.selenium.current_url

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('user')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('WRONG PASSWORD')

        submit = selenium.find_element_by_name("login")
        submit.send_keys(Keys.RETURN)

        # check the link of the response.
        assert '/vod/login' in selenium.current_url
        assert 'alert-warning' in selenium.page_source

    def test_user_failed_login_invalid(self):
        selenium = self.selenium

        # Opening the link we want to test
        selenium.get('http://localhost:8081/vod/login/')

        assert "/vod/login/" in self.selenium.current_url

        username_input = self.selenium.find_element_by_name("username")
        password_input = self.selenium.find_element_by_name("password")

        submit = selenium.find_element_by_name("login")
        submit.send_keys(Keys.RETURN)

        # check the link of the response.
        assert 'alert-info' in selenium.page_source

    def test_user_successful_login(self):
        selenium = self.selenium

        # Opening the link we want to test
        selenium.get('http://localhost:8081/vod/login/')

        assert "/vod/login/" in self.selenium.current_url

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('user')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('userpassword')

        submit = selenium.find_element_by_name("login")
        submit.send_keys(Keys.RETURN)

        # check the link of the response.
        assert '/vod/patient/list/' in selenium.current_url

    def test_add_user(self):

        selenium = self.selenium

        # Opening the link we want to test
        selenium.get('http://localhost:8081/vod/login/')

        assert "/vod/login/" in self.selenium.current_url

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('user')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('userpassword')

        submit = selenium.find_element_by_name("login")
        submit.send_keys(Keys.RETURN)

        addPt = selenium.find_element_by_id("btnAdd")
        addPt.send_keys(Keys.RETURN)

        # test if modal is displayed
        assert 'modal-content' in selenium.page_source

        addpx_firstname = self.selenium.find_element_by_id("first_name")
        addpx_firstname.send_keys('dummy')
        addpx_lastname = self.selenium.find_element_by_id("surname")
        addpx_lastname.send_keys('dummysurname')
        addpx_gender = self.selenium.find_element_by_id("gender")
        addpx_gender.send_keys(Keys.SPACE, 'm')
        addpx_dob = self.selenium.find_element_by_id("date_of_birth")
        addpx_dob.send_keys('2001-01-12')

        adduser_submit = self.selenium.find_element_by_id("submit-id-save_changes")
        adduser_submit.send_keys(Keys.SPACE)

        assert 'modal-content' in selenium.page_source
    def test_list_views(self):

        # testing what the ListView would display
        # Institutions
        matching_objects = Institution.objects.all()
        self.assertEqual(matching_objects.count(), 3)

        # Datatype
        matching_objects = Datatype.objects.all()
        self.assertEqual(matching_objects.count(), 3)

        # User
        matching_objects = User.objects.all()
        self.assertEqual(matching_objects.count(), 1)

        # Transplant
        matching_objects = Transplant_Type.objects.all()
        self.assertEqual(matching_objects.count(), 2)

        # Alias identifier
        matching_objects = Alias_Identifier.objects.all()
        self.assertEqual(matching_objects.count(), 3)
