from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Category
from .forms import PostForm, PostSearchForm, CategoryForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
  param = {}
  form = PostSearchForm()
  if request.GET.get('title') != '' and request.GET.get('title') != None:
    search = request.GET.get('title')
    posts = Post.objects.filter(published_date__lte=timezone.now(),title__contains=search).order_by('-published_date')
    param['info_msg'] = "Search post contain \"" + search + "\""
  else:
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
  param['cats'] = get_cat()
  page = request.GET.get('page', 1)
  paginator = Paginator(posts, 5)
  try:
    posts_pag = paginator.page(page)
  except PageNotAnInteger:
    posts_pag = paginator.page(1)
  except EmptyPage:
    posts_pag = paginator.page(paginator.num_pages)
  param['posts'] = posts_pag
  param['page_title'] = "All Published Post"
  return render(request, 'blog/post_list.html', param)




def post_category(request, pk):
  cat = get_object_or_404(Category, pk=pk)
  param = {}
  form = PostSearchForm()
  if request.GET.get('title') != '' and request.GET.get('title') != None:
    search = request.GET.get('title')
    posts = Post.objects.filter(published_date__lte=timezone.now(),category=cat,title__contains=search).order_by('-published_date')
    param['info_msg'] = "Search post contain \"" + search + "\""
  else:
    posts = Post.objects.filter(published_date__lte=timezone.now(),category=cat).order_by('-published_date')
  param['cats'] = get_cat()
  page = request.GET.get('page', 1)
  paginator = Paginator(posts, 5)
  try:
    posts_pag = paginator.page(page)
  except PageNotAnInteger:
    posts_pag = paginator.page(1)
  except EmptyPage:
    posts_pag = paginator.page(paginator.num_pages)
  param['posts'] = posts_pag
  param['page_title'] = "Post with Category: " + str(cat)
  return render(request, 'blog/post_list.html', param)



def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  form = CommentForm()
  return render(request, 'blog/post_detail.html', {'cats' : get_cat(), 'post': post, 'form': form})



@login_required
def post_new(request):
  if request.method == "POST":
    form = PostForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm()
  page_title = "New Post"
  return render(request, 'blog/post_edit.html', {'cats' : get_cat(), 'form': form, 'page_title': page_title})



@login_required
def post_edit(request, pk):
  post = get_object_or_404(Post, pk=pk)
  if request.method == "POST":
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = request.user
      post.save()
      return redirect('post_detail', pk=post.pk)
  else:
    form = PostForm(instance=post)
  page_title = "Edit Post"
  return render(request, 'blog/post_edit.html', {'cats' : get_cat(), 'form': form, 'page_title': page_title})



@login_required
def post_draft_list(request):
  param = {}
  form = PostSearchForm()
  if request.GET.get('title') != '' and request.GET.get('title') != None:
    search = request.GET.get('title')
    posts = Post.objects.filter(published_date__isnull=True,title__contains=search).order_by('-created_date')
    param['info_msg'] = "Search post contain \"" + search + "\""
  else:
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
  page = request.GET.get('page', 1)
  paginator = Paginator(posts, 5)
  try:
    posts_pag = paginator.page(page)
  except PageNotAnInteger:
    posts_pag = paginator.page(1)
  except EmptyPage:
    posts_pag = paginator.page(paginator.num_pages)
  param['posts'] = posts_pag
  return render(request, 'blog/post_draft_list.html', param)



@login_required
def post_publish(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.publish()
  return redirect('post_detail', pk=pk)



@login_required
def post_pull(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.pull()
  return redirect('post_detail', pk=pk)



@login_required
def post_remove(request, pk):
  post = get_object_or_404(Post, pk=pk)
  post.delete()
  return redirect('post_list')



@login_required
def mng_category(request):
  param = {}
  if request.method == "POST":
    form = CategoryForm(request.POST)
    if form.is_valid():
      cat = form.save(commit=False)
      cat.save()
      form = CategoryForm()
      suc_msg = "New category added"
      param['suc_msg'] = suc_msg
  else:
    form = CategoryForm()
  page = request.GET.get('page', 1)
  param['cats_pag'] = get_cat_pag(page)
  param['cats'] = get_cat()
  param['form'] = form
  return render(request, 'blog/category_manage.html', param)



@login_required
def cat_remove(request, pk):
  cat = get_object_or_404(Category, pk=pk)
  cat.delete()
  form = CategoryForm()
  suc_msg = "Category deleted"
  page = request.GET.get('page', 1)
  return render(request, 'blog/category_manage.html', {'cats_pag': get_cat_pag(page), 'cats' : get_cat(), 'form': form, 'suc_msg': suc_msg})



def get_cat():
  return Category.objects.order_by('title')



def get_cat_pag(page):
  cats_list = get_cat()
  paginator = Paginator(cats_list, 5)
  try:
    cats = paginator.page(page)
  except PageNotAnInteger:
    cats = paginator.page(1)
  except EmptyPage:
    cats = paginator.page(paginator.num_pages)
  return cats



def add_comment_to_post(request, pk):
  param = {}
  post = get_object_or_404(Post, pk=pk)
  form = CommentForm(request.POST)
  if form.is_valid():
    comment = form.save(commit=False)
    comment.post = post
    comment.save()
    suc_msg = "Comment sent, waiting to approve"
    param['suc_msg'] = suc_msg
  param['cats'] = get_cat()
  param['post'] = post
  param['form'] = form
  return render(request, 'blog/post_detail.html', param)



@login_required
def comment_approve(request, pk):
  comment = get_object_or_404(Comment, pk=pk)
  comment.approve()
  return redirect('post_detail', pk=comment.post.pk)



@login_required
def comment_remove(request, pk):
  comment = get_object_or_404(Comment, pk=pk)
  comment.delete()
  return redirect('post_detail', pk=comment.post.pk)