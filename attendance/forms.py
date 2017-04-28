import lxml.html
import requests
from django import forms
from models import Student
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Field, Div
from crispy_forms.bootstrap import StrictButton, InlineCheckboxes


class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-signin'
        self.helper.label_class = 'sr-only'
        # self.helper.field_class = 'form-control'
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            HTML('<h2 class ="form-signin-heading" > Register </h2><br/><br/>'),
            Div(
                'user_name',
                'lms_id',
                'password',
                HTML("<p>Profile Picture</p><img id='profile-pic' class='img-circle col-lg-12' src='#' alt='Profile pic not uploaded!'>"),
                'profile_picture',
            ),
            StrictButton('Register', css_class='btn btn-lg btn-primary btn-block', type='submit')
        )

    user_name = forms.CharField(label="User Name", max_length=50, widget=forms.TextInput(attrs={'placeholder': "User Name", 'class': 'form-control'}))
    lms_id = forms.CharField(label="LMS ID", max_length=50, widget=forms.TextInput(attrs={'placeholder': "LMS ID", 'class': 'form-control', 'id':'lmsid'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'form-control'}))
    profile_picture = forms.ImageField()

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        user_name = cleaned_data.get("user_name")
        lms_id = cleaned_data.get("lms_id")
        password = cleaned_data.get("password")
        profile_picture = cleaned_data.get("profile_picture")

        if lms_id and user_name and password:
            print "Cleaned LMS ID : ", lms_id
            print "Cleaned Password : ", password
            print "Profile Picture : ", profile_picture
            print
            try:
                Student.objects.get(lmsId=lms_id)
                flag = True
            except Student.DoesNotExist:
                flag = False

            if flag:
                print "Student already exits"
                raise forms.ValidationError(
                    "Student exits"
                )
            else:
                s = requests.session()
                login_url = 'http://lms.bml.edu.in/login/index.php'
                dash_url = 'http://lms.bml.edu.in/local/dashboard/index.php'

                login = s.get(login_url)
                login_html = lxml.html.fromstring(login.content)
                hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
                form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
                form['username'] = lms_id
                form['password'] = password
                response = s.post(login_url, data=form)

                if response.url == dash_url:
                    flag2 = False
                    print "Valid LMS details"
                else:
                    flag2 = True
                if flag2:
                    raise forms.ValidationError(
                        "Invalid LMS Details"
                    )


class EditProfile(forms.Form):
    profilePic = forms.ImageField(label="Profile Picture")
    scholarship = forms.BooleanField(label='Scholarship')