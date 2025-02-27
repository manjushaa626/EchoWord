from .models import UserProfile,Blogpost,Comment
from .forms import CustomUserCreationForm,SignInForm,AddBlogForm,ProfileEditForm,CommentForm
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages


def home(request):
    msg = request.GET.get('msg')
    data_value = Blogpost.objects.all()
    return render(request, 'home.html', {'Blogpost': data_value, 'msg': msg})


def blogs(request):
    query = request.GET.get('q')  
    data_value = Blogpost.objects.all() 
    if query:
        data_value = Blogpost.objects.filter(title__icontains=query)
    return render(request, 'blogs.html', {'Blogpost': data_value, 'query': query})


def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    blogs = profile.user.blogs.all() 
    return render(request, 'profile.html', {'profile': profile, 'blogs': blogs})



def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


def signup(request):
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            phone_number=form.cleaned_data['phone_number']
            user=form.save()
            UserProfile.objects.create(user=user,phone_number=phone_number)
            login(request,user)
            msg="SignUp Completed"
            return render(request,'home.html',{'msg':msg})
        else:
            msg="SignUp not successfull"
            form=CustomUserCreationForm()
            return render(request,'signup.html',{'form':form,'msg':msg})
    else:
        form=CustomUserCreationForm()
        msg="SignUp not successfull"
        return render(request,'signup.html',{'form':form})


def  signin(request):
    if request.method=='POST':
        form=SignInForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user= authenticate(request,username=username,password=password)
            request.session['username']=username
            if user is not None:
                login(request,user)
                return redirect(home)
        else:
            return render(request,'signin.html',{'form': form})
    else:
        form=SignInForm()
        return render(request,'signin.html',{'form': form})


def signout(request):
    if 'username' in request.session:
        del request.session['username']
    logout(request)
    return redirect(home)


def changepassword(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
        else:
            messages="Cannot change password"
            return render(request,'changepassword.html',{'form': form,'messages':messages})
    else:
        form=PasswordChangeForm(request.user)
        return render(request,'changepassword.html',{'form': form})
    
def addblog(request):
    form = AddBlogForm()
    return render(request, 'addblog.html', {'addblogform': form})

def blog_save(request):
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user       
            blog.save()                   
            messages.success(request, "Blog added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Failed to add blog. Please try again.")
    else:
        form = AddBlogForm()
    return render(request, 'addblog.html', {'addblogform': form})

    
def blog_edit(request, id):
    blog = get_object_or_404(Blogpost, id=id)
    if blog.user != request.user:
        messages.error(request, "You are not authorized to edit this blog.")
        return redirect('home')
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "Failed to update blog. Please try again.")
    else:
        form = AddBlogForm(instance=blog)
    return render(request, 'addblog.html', {'addblogform': form, 'instance': blog})



def blog_delete(request, id):
    blog = get_object_or_404(Blogpost, id=id)
    if blog.user != request.user:
        messages.error(request, "You are not authorized to delete this blog.")
        return redirect('home')
    blog.delete()
    messages.success(request, "Blog deleted successfully!")
    return redirect('home')

# def blog_detail(request, id):
#     blog = get_object_or_404(Blogpost, id=id) 
#     is_owner = blog.user == request.user
#     return render(request, 'blog_detail.html', {'blog': blog, 'is_owner': is_owner})

def blog_detail(request, id):
    blog = get_object_or_404(Blogpost, id=id)  
    is_owner = blog.user == request.user
    comments = blog.comments.all()  
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            return redirect('blog_detail', id=blog.id)
    context = {
        'blog': blog,
        'is_owner': is_owner,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog_detail.html', context)
def add_comment(request, blog_id):
    blog = get_object_or_404(Blogpost, id=blog_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        user_profile = UserProfile.objects.get(user=request.user)  # Fetch UserProfile
        Comment.objects.create(blog=blog, user=user_profile, content=content)
        return redirect('blog_detail', id=blog_id)

def blog_update(request, pk=None):
    if request.method == 'POST':
        if pk is not None:
            instance = get_object_or_404(Blogpost, pk=pk)
            form = AddBlogForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save() 
                data_value = Blogpost.objects.all()
                return render(request, 'home.html', {'Blogpost': data_value})
            else:
                return render(request, 'home.html', {'addblogform': form})
        else:
            return redirect('home')
    else:
        form = AddBlogForm()
        return render(request, 'home.html', {'addblogform': form})

def contact(request):
    return render(request,'contact.html')
