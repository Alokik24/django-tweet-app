from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    return render(request, 'inapp/home.html')

def tweet_list(request):
    sort_by = request.GET.get('sort', 'created_at')
    order = request.GET.get('order', 'desc')

    if order == 'desc':
        sort_field = f'-{sort_by}'
    else:
        sort_field = sort_by

    tweets = Tweet.objects.all().order_by(sort_field)
    return render(request, 'inapp/tweet_list.html',{
        'tweets': tweets,
        'user': request.user,
        'current_sort:' :sort_by,
        'order': order,
    })

@login_required()
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')

    else:
        form = TweetForm()
    return render(request, 'inapp/tweet_form.html', {'form': form})

def tweet_search(request):
    query = request.GET.get('q', '')
    results = Tweet.objects.filter(text__icontains=query) if query else []
    return render(request, 'inapp/search_results.html', {'results': results, 'query': query})

@login_required()
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'inapp/tweet_form.html', {'form': form})

@login_required()
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'inapp/tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
@staff_member_required
def admin_dashboard(request):
    tweets = Tweet.objects.all().order_by('-created_at')

    # Filters from GET params
    query = request.GET.get('q', '').strip()
    user_filter = request.GET.get('user', '').strip()
    edited_only = request.GET.get('edited_only') == 'on'
    flagged_only = request.GET.get('flagged_only') == 'on'
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    if query:
        tweets = tweets.filter(Q(text__icontains=query) | Q(user__username__icontains=query))
    if user_filter:
        tweets = tweets.filter(user__username__iexact=user_filter)
    if edited_only:
        tweets = tweets.filter(edited_at__isnull=False)
    if flagged_only:
        tweets = tweets.filter(is_flagged=True)
    if start_date:
        tweets = tweets.filter(created_at__date__gte=start_date)
    if end_date:
        tweets = tweets.filter(created_at__date__lte=end_date)

    # Pass all users for the user filter dropdown
    all_users = User.objects.all().order_by('username')

    context = {
        'tweets': tweets,
        'query': query,
        'user_filter': user_filter,
        'edited_only': edited_only,
        'flagged_only': flagged_only,
        'start_date': start_date,
        'end_date': end_date,
        'all_users': all_users,
    }
    return render(request, 'inapp/admin_dashboard.html', context)

@staff_member_required()
def tweet_detail_admin(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    return render(request, 'inapp/tweet_detail_admin.html', {'tweet': tweet})

@staff_member_required()
def tweet_delete_admin(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    tweet.delete()
    return redirect('admin_dashboard')

@staff_member_required
def tweet_bulk_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        tweet_ids = request.POST.getlist('tweet_id')

        if not tweet_ids:
            messages.warning(request, "No tweets selected.")
            return redirect('admin_dashboard')

        tweets = Tweet.objects.filter(id__in=tweet_ids)

        if action == 'flag':
            tweets.update(is_flagged=True)
            messages.success(request, "Selected tweets flagged.")
        elif action == 'delete':
            tweets.delete()
            messages.success(request, "Selected tweets deleted.")
        else:
            messages.error(request, "Invalid action selected.")

    return redirect('admin_dashboard')

@staff_member_required
def tweet_toggle_flag(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    tweet.is_flagged = not tweet.is_flagged
    tweet.save()
    status = "flagged" if tweet.is_flagged else "unflagged"
    messages.success(request, f"Tweet has been {status}.")
    return redirect('admin_dashboard')

@staff_member_required
def tweet_admin(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, "Tweet updated successfully.")
            return redirect('admin_dashboard')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'inapp/tweet_edit_admin.html', {'form': form, 'tweet': tweet})
