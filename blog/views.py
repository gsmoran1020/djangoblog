from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import CommentForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context=context)


def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 7
    
    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date_posted')
        

        if self.request.method == 'GET':
            search_input = self.request.GET.get('search-area') or ''
            if search_input:
                queryset = queryset.filter(title__contains=search_input)

        return queryset

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(FormMixin, DetailView):
    model = Post
    context_object_name = 'post'
    form_class = CommentForm

    # On successful comment post, the page is reloaded so users can see their comment.
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        context = self.get_context_data()
        comment = form.save(commit=False)
        comment.post = context['post']
        comment.author = self.request.user
        comment.save()
        return super(PostDetailView, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):  # LoginRequiredMixin is how to make class-based views require login
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):  # overriding this function from then running the super() allows us to set the author
        form.instance.author = self.request.user
        return super().form_valid(form)


# LoginRequiredMixin is how to make class-based views require login
# UserPassesTestMixin checks if you are the same user as the creator of an element you are trying to access.
# See the test_func() function that is needed to utilize this Mixin.
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):  # overriding this function then running the super() allows us to set the author of the form
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/' 

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})