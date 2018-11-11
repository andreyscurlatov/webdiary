from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

# Create your views here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Blogger, Blog, Comment


def index(request):
    num_blogs = Blog.objects.all().count()
    num_bloggers = Blogger.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {

        'num_blogs': num_blogs,
        'num_bloggers': num_bloggers,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context)


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blog_list'
    queryset = Blog.objects.all()
    template_name = 'blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['comment_list'] = Comment.objects.filter(blog_id=self.kwargs['pk']).order_by('date_of_public')[::-1]
        return context


class BlogCreate(CreateView):
    model = Blog
    fields = ['title', 'text']
    success_url = '/blog/blog/all'
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.blogger = Blogger.objects.get(nik_name_id=self.request.user.id)
        return super(BlogCreate, self).form_valid(form)


class BloggerListView(ListView):
    model = Blogger
    context_object_name = 'blogger_list'
    queryset = Blogger.objects.all()
    template_name = 'blogger_list.html'


class BloggerDetailView(DetailView):
    model = Blogger
    context_object_name = 'blogger'
    template_name = 'blogger_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BloggerDetailView, self).get_context_data(**kwargs)
        context['blog_list'] = Blog.objects.filter(blogger_id=self.kwargs['pk']).order_by('date_of_public')[::-1]
        return context


class BloggerCreate(LoginRequiredMixin, CreateView):
    model = Blogger
    fields = ['first_name', 'last_name', 'date_of_birth', 'bio']
    success_url = '/blog/blogger/all'
    template_name = 'blogger_form.html'

    def form_valid(self, form):
        form.instance.nik_name = self.request.user
        return super(BloggerCreate, self).form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = 'comment_form.html'

    def form_valid(self, form):
        form.instance.blog = Blog.objects.get(id=self.kwargs['pk'])
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


def add_user_to_group_users(sender, user, **kwargs):
    group = Group.objects.get(name='users')
    group.user_set.add(user)


@receiver(post_save, sender=Blogger)
def add_blogger_to_group_bloggers(sender, instance, **kwargs):
    group = Group.objects.get(name='bloggers')
    group.user_set.add(instance.nik_name)
