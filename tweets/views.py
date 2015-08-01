from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .twitterAPI import get_tweet
from .models import Tweet, Author


@csrf_exempt
@require_POST
def fetch(request):
    tweet_id = request.POST['tweet_id']
    return JsonResponse(get_tweet(tweet_id))


@csrf_exempt
@require_POST
def create(request):
    tweet_data = request.POST['tweet_data']
    author_data = tweet_data['author']

    try:
        tweet = Tweet.objects.get(pk=tweet_data['id'])
    except Tweet.DoesNotExist:
        tweet = Tweet(
            id=tweet_data['id'],
            created_at=tweet_data['created_at'],
            favorite_count=tweet_data['favorite_count'],
            text=tweet_data['text']
        )

        try:
            author = Author.objects.get(pk=author_data['screen_name'])
        except Author.DoesNotExist:
            author = Author.objects.create(
                screen_name=author_data['screen_name'],
                name=author_data['name'],
                profile_image_url=author_data['profile_image_url']
            )

        tweet.author = author
        tweet.save()

        for rt_author_data in tweet_data['retweeted_by']:
            try:
                rt_author = Author.objects.get(pk=rt_author_data['screen_name'])
            except Author.DoesNotExist:
                rt_author = Author.objects.create(
                    screen_name=rt_author_data['screen_name'],
                    name=rt_author_data['name'],
                    profile_image_url=rt_author_data['profile_image_url']
                )

            tweet.retweet_authors.add(rt_author)
            tweet.save()

    if 'retweet_data' in request.POST.keys():
        retweet_data = request.POST['retweet_data']

        try:
            retweet = Tweet.objects.get(pk=retweet_data['id'])
        except Tweet.DoesNotExist:
            retweet = Tweet.objects.create(
                id=retweet_data['id'],
            )


    return JsonResponse({'status': 'OK'})
