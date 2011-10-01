import tweepy

auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)

u = User.objects.get(username='panchicore').social_auth.get()

auth.set_access_token(u.oauth_token, u.oauth_token_secret)

api = tweepy.API(auth)

t = api.update_status('hola mundo')


  