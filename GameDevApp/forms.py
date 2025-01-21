from allauth.account.forms import LoginForm, SignupForm
from captcha.fields import ReCaptchaField

class CustomLoginForm(LoginForm):
    captcha = ReCaptchaField()

class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField()
