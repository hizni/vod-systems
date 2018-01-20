from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, FormView
from parsley.decorators import parsleyfy

from models import User_Institution, Institution
from user_forms import UserCreateForm, UserDetailUpdateForm, UserRetireForm, LoginForm




def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None

    request.session.flush()
    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

    return redirect('index')


class LoginView(FormView):
    form_class = LoginForm
    # success_url = redirect('user-list')
    template_name = './vod/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            # raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
            messages.warning(self.request, "Sorry, that login was invalid. Please try again.")
            return redirect('vod-login')
        else:
            auth_login(self.request, user)
            if user.is_superuser:
                self.success_url = reverse('user-list')
            else:
                self.success_url = reverse('patient-list')

            return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, "Please make sure to correctly fill the form")

        return super(LoginView, self).form_invalid(form)


"""
User model Class Based Views
    UserListView    - list all the users
    
    UserCreateView  - create a new user
    UserUpdateView  - update a select user
    UserRetireView  - activate/deactivate the selected user 
"""


class UserListView(ListView):
    model = User
    template_name = './vod/admin/user-list.html'

    def get_queryset(self):
        return User.objects.all()


class UserCreateView(CreateView):
    form_class = parsleyfy(UserCreateForm)
    # template_name = '../templates/common/modal-template.html'
    # template_name = '../templates/common/user-form-template.html'
    template_name = '../templates/vod/admin/user-modal-template.html'
    view_title = 'Create new user'

    def form_valid(self, form):

        user = form.save()
        user.set_password(user.password)
        user.save()

        for i in form.cleaned_data['checkbox_select_multiple']:
            user_inst = User_Institution()
            user_inst.fk_user_id = user
            user_inst.fk_institution_id = Institution.objects.get(code=i)

            user_inst.save()

        if user.is_superuser:
            return redirect('user-list')
        else:
            return redirect('user-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,))


class UserUpdateView(UpdateView):

    form_class = parsleyfy(UserDetailUpdateForm)
    model = User
    # template_name = '../templates/common/form-template.html'
    # template_name = '../templates/common/user-form-template.html'
    template_name = '../templates/vod/admin/user-modal-template.html'

    view_title = 'Update existing user'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(UserUpdateView, self).get_form(form_class)
        form.helper.form_action = reverse('user-update', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return User.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        user = form.save()

        # todo Add some auditing to user institution management
        # currently all previous entries for institutions attributed to this user are deleted
        # no audit trail is setup
        user_chosen_inst = User_Institution.objects.filter(fk_user_id=self.kwargs['id'])
        user_chosen_inst.delete()

        # adding user - institution relationship
        for i in form.cleaned_data['checkbox_select_multiple']:
            user_inst = User_Institution()
            user_inst.fk_user_id = user
            user_inst.fk_institution_id = Institution.objects.get(id=i)

            user_inst.save()

        return redirect('user-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


class UserRetireView(UpdateView):
    form_class = parsleyfy(UserRetireForm)
    model = User
    # template_name = '../templates/common/form-template.html'
    # template_name = '../templates/common/user-form-template.html'
    template_name = '../templates/common/modal-template.html'
    view_title = 'User active status'
    selected_pk = 0

    def get_form(self, form_class=None):
        form = super(UserRetireView, self).get_form(form_class)
        form.helper.form_action = reverse('user-retire', kwargs={'id': self.selected_pk})
        return form

    def get_object(self, queryset=None):
        self.selected_pk = self.kwargs['id']
        return User.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        form.save()
        return redirect('user-list')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, ))


