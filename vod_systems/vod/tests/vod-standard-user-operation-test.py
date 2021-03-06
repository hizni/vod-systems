from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.auth.models import User
from vod.models import Institution, Datatype, Transplant_Type, Alias_Identifier, User_Institution, Patient
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

    def test_add_patient(self):

        selenium = self.selenium

        # Opening the link we want to test
        selenium.get('http://localhost:8081/vod/login/')

        assert "/vod/login/" in self.selenium.current_url

        self.helper_login_user()

        selenium.get('http://localhost:8081/vod/patient/list/')

        # check the number of user objects in the database
        self.assertEqual(Patient.objects.all().count(), 0)

        addBtn = selenium.find_element_by_id("btnAdd")
        addBtn.send_keys(Keys.RETURN)

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

        # check the number of user objects in the database
        self.assertEqual(Patient.objects.all().count(), 1)

    def helper_login_user(self):
        selenium = self.selenium

        # Login a user
        selenium.get('http://localhost:8081/vod/login/')

        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('user')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('userpassword')

        submit = selenium.find_element_by_name("login")
        submit.send_keys(Keys.RETURN)

    def test_add_user(self):
        selenium = self.selenium

        self.helper_login_user()

        # assert that number of institutions added is same as in setup
        self.assertEqual(User.objects.all().count(), 1)

        selenium.get('http://localhost:8081/vod/user/list/')
        assert "/vod/user/list/" in self.selenium.current_url

        addInst = selenium.find_element_by_id("btnAdd")
        addInst.send_keys(Keys.RETURN)

        # test if modal is displayed
        assert 'modal-content' in selenium.page_source

        self.selenium.find_element_by_id("username").send_keys('dummy')

        self.selenium.find_element_by_id("password").send_keys('dummy')

        self.selenium.find_element_by_id("confirm_password").send_keys('dummy')

        self.selenium.find_element_by_id("is_staff").send_keys(Keys.SPACE)

        self.selenium.find_element_by_id("id_checkbox_select_multiple_1").send_keys(Keys.SPACE)

        self.selenium.find_element_by_id("submit-id-save_changes").send_keys(Keys.SPACE)

        # assert that number of institutions added is same as in setup
        self.assertEqual(User.objects.all().count(), 2)

    def test_add_institution(self):
        selenium = self.selenium

        self.helper_login_user()

        # assert that number of institutions added is same as in setup
        self.assertEqual(Institution.objects.all().count(), 3)

        selenium.get('http://localhost:8081/vod/institution/list/')
        assert "/vod/institution/list/" in self.selenium.current_url

        addInst = selenium.find_element_by_id("btnAdd")
        addInst.send_keys(Keys.RETURN)

        # test if modal is displayed
        assert 'modal-content' in selenium.page_source

        code = self.selenium.find_element_by_id("code")
        code.send_keys('dummy')

        desc = self.selenium.find_element_by_id("description")
        desc.send_keys('dummy')

        submit = self.selenium.find_element_by_id("submit-id-save_changes")
        submit.send_keys(Keys.SPACE)

        # assert that number of institutions added is same as in setup
        self.assertEqual(Institution.objects.all().count(), 4)

    def test_add_alias_identifier(self):
        selenium = self.selenium

        self.helper_login_user()

        # assert that number of institutions added is same as in setup
        self.assertEqual(Alias_Identifier.objects.all().count(), 3)

        selenium.get('http://localhost:8081/vod/aliasid/list/')
        assert "/vod/aliasid/list/" in self.selenium.current_url

        addAlias = selenium.find_element_by_id("btnAdd")
        addAlias.send_keys(Keys.RETURN)

        # test if modal is displayed
        assert 'modal-content' in selenium.page_source

        code = self.selenium.find_element_by_id("code")
        code.send_keys('dummy')

        desc = self.selenium.find_element_by_id("description")
        desc.send_keys('dummy')

        submit = self.selenium.find_element_by_id("submit-id-save_changes")
        submit.send_keys(Keys.SPACE)

        # assert that number of institutions added is same as in setup
        self.assertEqual(Alias_Identifier.objects.all().count(), 4)

    def test_add_datatype(self):
        selenium = self.selenium

        self.helper_login_user()

        # assert that number of institutions added is same as in setup
        self.assertEqual(Datatype.objects.all().count(), 3)

        selenium.get('http://localhost:8081/vod/datatype/list/')

        assert "/vod/datatype/list/" in self.selenium.current_url

        addDatatype = selenium.find_element_by_id("btnAdd")
        addDatatype.send_keys(Keys.RETURN)

        # test if modal is displayed
        assert 'modal-content' in selenium.page_source

        code = self.selenium.find_element_by_id("code")
        code.send_keys('dummy')

        desc = self.selenium.find_element_by_id("description")
        desc.send_keys('dummy')

        unit = self.selenium.find_element_by_id("unit")
        unit.send_keys('dummy')

        submit = self.selenium.find_element_by_id("submit-id-save_changes")
        submit.send_keys(Keys.SPACE)

        self.assertEqual(Datatype.objects.all().count(), 4)

    def test_add_transplant(self):
        selenium = self.selenium

        self.helper_login_user()

        self.assertEqual(Transplant_Type.objects.all().count(), 2)

        selenium.get('http://localhost:8081/vod/transplant/list/')

        assert "/vod/transplant/list/" in self.selenium.current_url

        addTransplant = selenium.find_element_by_id("btnAdd")
        addTransplant.send_keys(Keys.RETURN)

        # test if modal is displayed
        assert 'modal-content' in selenium.page_source

        code = self.selenium.find_element_by_id("code")
        code.send_keys('dummy')

        desc = self.selenium.find_element_by_id("description")
        desc.send_keys('dummy')

        submit = self.selenium.find_element_by_id("submit-id-save_changes")
        submit.send_keys(Keys.SPACE)

        self.assertEqual(Transplant_Type.objects.all().count(), 3)

    def test_list_views(self):

        # testing what the ListView would display
        # Institutions
        matching_objects = Institution.objects.all()
        self.assertEqual(matching_objects.count(), 3)

        # Data type
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
