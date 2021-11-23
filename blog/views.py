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

# This 'view' sets the like for a post and then redirects to the same page without rendering any new pages.
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
        
        # Search Logic activates on get request and filters the set of posts by the search input
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
    form_class = CommentForm # Added with FormMixin so users can comment on others posts

    # On successful comment post, the page is reloaded so users can see their comment.
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    # Checks form on post request
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    # Saves comment and sets other necessary fields for the comment model
    def form_valid(self, form):
        context = self.get_context_data()
        comment = form.save(commit=False)
        comment.post = context['post']
        comment.author = self.request.user
        comment.save()
        return super(PostDetailView, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form): 
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form): 
        form.instance.author = self.request.user
        return super().form_valid(form)

    #Ensures user is who they say they are in order to update a post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    success_url = '/' 

    #Ensures user is who they say they are in order to delete a post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})