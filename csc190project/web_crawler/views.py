from django.shortcuts import render
import requests
import praw
import pandas as pd
import datetime as dt
import sys
import re
import string
import requests
import dateutil.parser
import schedule
import pytz
import time, threading
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from web_crawler.models import *
#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import connection
from django.core.mail import send_mail
#from background_task import background
from pytz import timezone, utc
import pytz
from django.utils.html import strip_tags

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            print('Doing something imporant in the background')
            time.sleep(self.interval)


def index(request):
    return render(request, 'web_crawler/index.html')


def get_reddit_api(keywords):
    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password',
            'username': "projectHaven190", 'password': "haven190"}
    auth = requests.auth.HTTPBasicAuth(APP-ID, APP-SECRET)
    r = requests.post(base_url + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': 'APP-NAME by projectHaven190'},
                      auth=auth)
    d = r.json()
    token = 'bearer ' + d['access_token']
    base_url = 'https://oauth.reddit.com'
    headers = {'Authorization': token,
               'User-Agent': 'APP-NAME by projectHaven190'}
    payload = {'query': keywords, "include_over_18": False}
    response = requests.get(
        base_url + '/api/subreddit_autocomplete', headers=headers, params=payload)
    print(response)
    return response


@csrf_exempt
def suggest_subreddit(request):
    if request.method == "POST":
        subreddit = request.POST['subreddit']
        response = get_reddit_api(subreddit)
        return JsonResponse({"subreddit": subreddit_list})


@csrf_exempt
def regular_output(request):
    if request.method == "POST":
        search_word = request.POST['search_word']
        subreddit = request.POST['subreddit']
        py_obj, newest, new_result = craw_reddit(search_word, subreddit, "all", 10)
        # save search keyword into DB
        search_word_save = SearchHistory.objects.create(keyword=search_word, subreddit=subreddit, user=request.user, latest_search=dateutil.parser.parse(newest.astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y, %H:%M:%S")))
        #print(search_word_save.timestamp)
        print(search_word_save.latest_search)
        if py_obj == "":
            py_obj = "Your search yields no results. Please try again with different keywords."
        return JsonResponse({'output': py_obj, 'search_id': search_word_save.id})
        #return render(request, 'web_crawler/output.html', {'output': py_obj, 'search_id': search_word_save.id})


@csrf_exempt
def demo_output(request):
    if request.method == "POST":
        search_word = request.POST['search_word']
        subreddit = request.POST['subreddit']
        py_obj, newest, new_result = craw_reddit(search_word, subreddit, "all", 10)
        if py_obj == "":
            py_obj = "Your search yields no results. Please try again with different keywords."
        return JsonResponse({'output': py_obj})


@csrf_exempt
def search_subscribe(request):
    time_convert = {"10 minutes": 600, "1 hour": 3600, "1 day": 86400, "1 week": 604800, "1 month": 2592000}
    if request.method == "POST":
        search = SearchHistory.objects.get(id = request.POST['search_id'])
        search.subscribed = True
        search.subscribed_frequency = time_convert[request.POST['subscribed_frequency']]
        search.email = request.POST['email']
        search.save();
        return JsonResponse({"search_id": search.id, "search_word": search.keyword})


@csrf_exempt
def advanced_search_subscribe(request):
    time_convert = {"10 minutes": 600, "1 hour": 3600, "1 day": 86400, "1 week": 604800, "1 month": 2592000}
    if request.method == "POST":
        search = AdvancedSearchHistory.objects.get(id = request.POST['search_id'])
        search.subscribed = True
        search.subscribed_frequency = time_convert[request.POST['subscribed_frequency']]
        search.email = request.POST['email']
        search.save();
        return JsonResponse({"search_id": search.id})


@csrf_exempt
def search_unsubscribe(request):
    if request.method == "POST":
        search = SearchHistory.objects.get(id = request.POST['search_id'])
        #print(request.POST)
        #print(request.POST['search_id'])
        search.subscribed = False
        search.save();
        return JsonResponse({"search_id": search.id, "search_word": search.keyword})


@csrf_exempt
def advanced_search_unsubscribe(request):
    if request.method == "POST":
        search = AdvancedSearchHistory.objects.get(id = request.POST['search_id'])
        #print(request.POST)
        #print(request.POST['search_id'])
        search.subscribed = False
        search.save();
        return JsonResponse({"search_id": search.id})


@csrf_exempt
def advanced_output(request):
    if request.method == "POST":
        subreddit = request.POST['subreddit']
        word_in_title = request.POST['word_in_title']
        word_not_in_title = request.POST['word_not_in_title']
        word_in_comment = request.POST['word_in_comment']
        word_not_in_comment = request.POST['word_not_in_comment']
        search_within = request.POST['search_within']
        search_limit = request.POST['search_limit']

        search_save = AdvancedSearchHistory.objects.create(subreddit=subreddit,
                                                        word_in_title=word_in_title,
                                                        word_not_in_title=word_not_in_title,
                                                        word_in_comment=word_in_comment,
                                                        word_not_in_comment=word_not_in_comment,
                                                        search_within=search_within,
                                                        search_limit=search_limit,
                                                        user=request.user,
                                                    )
        search_query = ""
        if word_in_title != "":
            word_list = word_in_title.split(" ")
            word_in_title_list = ["title:" + each for each in word_list]
            word_in_title = " ".join(each for each in word_in_title_list)
            search_query += word_in_title

        if word_not_in_title != "":
            word_list = word_not_in_title.split(" ")
            word_not_in_title_list = [
                " NOT title:" + each for each in word_list]
            word_not_in_title = " ".join(
                each for each in word_not_in_title_list)
            search_query += word_not_in_title

        if word_in_comment != "":
            search_query += " " + word_in_comment

        if word_not_in_comment != "":
            word_list = word_not_in_comment.split(" ")
            word_not_in_comment_list = [" NOT " + each for each in word_list]
            word_not_in_comment = "".join(
                each for each in word_not_in_comment_list)
            search_query += word_not_in_comment

        print("5:" + search_query)
        # save advanced search into DB
        search_within_dict = {"All the time": "all", "One day": "day", "One month": "month", "One week": "week", "One year": "year"}
        py_obj, newest, new_result = craw_reddit(search_query, subreddit, search_within_dict[search_within], int(search_limit))

        search_save.latest_search = dateutil.parser.parse(newest.astimezone(pytz.timezone('America/Los_Angeles')).strftime("%m/%d/%Y, %H:%M:%S"))
        search_save.save()
        if py_obj == "":
            py_obj = "Your search yields no results. Please try again with different keywords."
        return JsonResponse({'output': py_obj, 'search_id': search_save.id})


def show_history(request):
    if request.method == "GET":
        search_list = SearchHistory.objects.filter(
            user=request.user).order_by('-timestamp')[:9]
        data = list(search_list.values())
        for each in data:
            each["timestamp"] = each["timestamp"].astimezone(pytz.timezone('America/Los_Angeles')).strftime("%b. %d, %Y, %I:%M %p")
        #return render(request, 'web_crawler/search_history.html', {"data": data})
        return JsonResponse(data, safe=False)


def show_advanced_history(request):
    if request.method == "GET":
        search_list = AdvancedSearchHistory.objects.filter(
            user=request.user).order_by('-timestamp')[:9]
        data = list(search_list.values())
        for each in data:
            each["timestamp"] = each["timestamp"].astimezone(pytz.timezone('America/Los_Angeles')).strftime("%b. %d, %Y, %I:%M %p")
        #return render(request, 'web_crawler/search_history.html', {"data": data})
        return JsonResponse(data, safe=False)


def craw_reddit(keywords, subreddit, search_within, search_limit, latest_search=None):
    reddit = praw.Reddit(client_id='UjzWJ5pYqzPMlg',
                         client_secret='k3S1WonqGzigZCw4LWhnR4FFAZM',
                         username='projectHaven190',
                         password='haven190',
                         user_agent='crawl')

    # subreddit that the user wants to crawl
    subreddit = reddit.subreddit(subreddit)

    # how many posts you want to scrub through. I have it to search through the 'hot' section of reddit.
    # if you look in the documentation subreddit could method call to .hot,.top,.new
    # limit is how many posts you want to look through, the max is 100 usually is defaulted at 15
    #hot_topics = subreddit.hot(limit=100)
    hot_topics = subreddit.search(keywords, time_filter=search_within, limit=search_limit, sort='new')
    
    result = ""
    keywordList = keywords.casefold().split()
    keywordList = [each.replace("title:", "") for each in keywordList]
    if "not" in keywordList:
        keywordList.remove("not")
    newest = dt.datetime(2000, 1, 1)
    new_result = ""
    for submission in hot_topics:
        if dt.datetime.fromtimestamp(submission.created_utc) > newest:            
            newest = dt.datetime.fromtimestamp(submission.created_utc)
        if latest_search and submission.created_utc == latest_search.timestamp():            
            new_result = result
        #Title of Post
        titles = '<h3>' + submission.title
        for word in titles.split():
            highlighted = highlight(word, keywordList)
            result += highlighted + ' '
        result = result + '</h3>'

        #URL to Post##
        redURL = submission.url
        for urls in redURL.split():
            result += '<a href=' + "'" + urls + "'" + 'target="_blank"' + '><p>' + \
                'Click this to see on Reddit' + '</a></p>' + " "

        #Body of Post#
        body = submission.selftext
        for word in body.split():
            highlighted = highlight(word, keywordList)
            result += highlighted + ' '
        result += "<br><br>"
    return result, newest, new_result


def highlight(text, keywords):
    def replacement(match): return re.sub(
        r'([^\s]+)', r'<mark>\1</mark>', match.group())
    text = re.sub("|".join(map(re.escape, keywords)),
                  replacement, text, flags=re.I)
    return (text)


def topFiveUsers(request):
    cursor = connection.cursor()
    cursor.execute('SELECT auth_user.username, count(web_crawler_searchhistory.timestamp) FROM auth_user, web_crawler_searchhistory WHERE auth_user.id = web_crawler_searchhistory.user_id GROUP BY auth_user.username ORDER BY count(web_crawler_searchhistory.timestamp) DESC LIMIT 5')
    topFive = cursor.fetchall()
    labels = [username[0] for username in topFive]
    data = [numOfSearch[1] for numOfSearch in topFive]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def topFiveKeyword(request):
    queryset = SearchHistory.objects.values('keyword').annotate(
        total=Count('keyword')).order_by('-total')[:5]
    labels = []
    data = []

    for value in queryset:
        labels.append(value['keyword'])
        data.append(value['total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def crawl_demo(request):
    return render(request, 'web_crawler/crawl_demo.html')

def topFiveUsers(request):
    cursor = connection.cursor()
    cursor.execute('SELECT auth_user.username, count(web_crawler_searchhistory.timestamp) FROM auth_user, web_crawler_searchhistory WHERE auth_user.id = web_crawler_searchhistory.user_id GROUP BY auth_user.username ORDER BY count(web_crawler_searchhistory.timestamp) DESC LIMIT 5')
    topFive = cursor.fetchall()
    labels = [username[0] for username in topFive]
    data = [numOfSearch[1] for numOfSearch in topFive]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def topFiveKeyword(request):
    queryset = SearchHistory.objects.values('keyword').annotate(
        total=Count('keyword')).order_by('-total')[:5]
    labels = []
    data = []

    for value in queryset:
        labels.append(value['keyword'])
        data.append(value['total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    # return render(request, 'web_crawler/top5keywords.html')
    
def topFiveUsers(request):
    cursor = connection.cursor()
    cursor.execute('SELECT auth_user.username, count(web_crawler_searchhistory.timestamp) FROM auth_user, web_crawler_searchhistory WHERE auth_user.id = web_crawler_searchhistory.user_id GROUP BY auth_user.username ORDER BY count(web_crawler_searchhistory.timestamp) DESC LIMIT 5')
    topFive = cursor.fetchall()
    labels = [username[0] for username in topFive]
    data = [numOfSearch[1] for numOfSearch in topFive]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
    
def top5users(request):
    return render(request, 'web_crawler/top5users.html')

def top5keywords(request):
    return render(request, 'web_crawler/top5keywords.html')

@login_required
def advanced_search(request):
    search_list = AdvancedSearchHistory.objects.filter(
        user=request.user).order_by('-timestamp')[:9]
    data = list(search_list.values())
    for each in data:
        each["timestamp"] = each["timestamp"].astimezone(pytz.timezone('America/Los_Angeles')).strftime("%b. %d, %Y, %I:%M %p")
    return render(request, 'web_crawler/advanced_search.html', {"data": data})



def regular_search(request):
    search_list = SearchHistory.objects.filter(
        user=request.user).order_by('-timestamp')[:9]
    data = list(search_list.values())
    for each in data:
        each["timestamp"] = each["timestamp"].astimezone(pytz.timezone('America/Los_Angeles')).strftime("%b. %d, %Y, %I:%M %p")

    return render(request, 'web_crawler/regular_search.html', {"data": data})




@login_required
def admin_console(request):
    return render(request, 'web_crawler/advanced_search.html')


def search_subscription(request):
    time_convert = {600: "10 minutes", 3600: "1 hour", 86400: "1 day", 604800: "1 week", 2592000: "1 month"}
    regular_search_subscription = SearchHistory.objects.filter(
        user=request.user, subscribed=True).order_by('-timestamp')
    advanced_search_subscription = AdvancedSearchHistory.objects.filter(
        user=request.user, subscribed=True).order_by('-timestamp')
    regular_search_data = list(regular_search_subscription.values())
    advanced_search_data = list(advanced_search_subscription.values())
    for each in regular_search_data:
        each["timestamp"] = each["timestamp"].astimezone(pytz.timezone('America/Los_Angeles')).strftime("%b. %d, %Y, %I:%M %p")
        each["subscribed_frequency"] = time_convert[each["subscribed_frequency"]]
    for each in advanced_search_data:
        each["timestamp"] = each["timestamp"].astimezone(pytz.timezone('America/Los_Angeles')).strftime("%b. %d, %Y, %I:%M %p")
        each["subscribed_frequency"] = time_convert[each["subscribed_frequency"]]
    return render(request, 'web_crawler/search_subscription.html', {"regular_search_subscription": regular_search_data, "advanced_search_subscription": advanced_search_data})


#@background()
def regular_crawl_background(regular_search):
    keyword = regular_search["keyword"]
    subreddit = regular_search["subreddit"]
    latest_search = regular_search["latest_search"]
    email = regular_search["email"]
    py_obj, newest, new_result = craw_reddit(keyword, subreddit, "all", 10, latest_search)
    #print("in regular_crawl: ", keyword, subreddit, new_result, newest, latest_search)
    temp = SearchHistory.objects.get(id=regular_search["id"])
    temp.latest_search = newest
    temp.save()
    if new_result != "":
        send_mail(
            "New search results from Crawl",
            strip_tags("<p>Hello, these are the new search results from your last visit: </p>" + new_result),
            "C R A W L Haven <crawler.haven@gmail.com>",
            [email],
            html_message=("<p>Hello, these are the new search results from your last visit: </p>" + new_result),
        )


def advanced_crawl_background(advanced_search):
    subreddit = advanced_search['subreddit']
    word_in_title = advanced_search['word_in_title']
    word_not_in_title = advanced_search['word_not_in_title']
    word_in_comment = advanced_search['word_in_comment']
    word_not_in_comment = advanced_search['word_not_in_comment']
    search_within = advanced_search['search_within']
    search_limit = advanced_search['search_limit']
    latest_search = advanced_search["latest_search"]
    email = advanced_search["email"]

    search_query = ""
    if word_in_title != "":
        word_list = word_in_title.split(" ")
        word_in_title_list = ["title:" + each for each in word_list]
        word_in_title = " ".join(each for each in word_in_title_list)
        search_query += word_in_title
    
    if word_not_in_title != "":
        word_list = word_not_in_title.split(" ")
        word_not_in_title_list = [" NOT title:" + each for each in word_list]
        word_not_in_title = " ".join(each for each in word_not_in_title_list)
        search_query += word_not_in_title

    if word_in_comment != "":
        search_query += " " + word_in_comment

    if word_not_in_comment != "":
        word_list = word_not_in_comment.split(" ")
        word_not_in_comment_list = [" NOT " + each for each in word_list]
        word_not_in_comment = "".join(each for each in word_not_in_comment_list)
        search_query += word_not_in_comment

    print("5:" + search_query)
    # save advanced search into DB
    search_within_dict = {"All the time": "all", "One day": "day", "One month": "month", "One week": "week", "One year": "year"}
    py_obj, newest, new_result = craw_reddit(search_query, subreddit, search_within_dict[search_within], int(search_limit), latest_search)
    temp = AdvancedSearchHistory.objects.get(id=advanced_search["id"])
    temp.latest_search = newest
    temp.save()
    #print("after saved")
    if new_result != "":
        send_mail(
            "New search results from Crawl",
            strip_tags("<p>Hello, these are the new search results from your last visit: </p>" + new_result),
            "C R A W L Haven <crawler.haven@gmail.com>",
            [email],
            html_message=("<p>Hello, these are the new search results from your last visit: </p>" + new_result),
        )
    return HttpResponse('')

#@background()
def subscription_background(repeat, frequency_array):
    original = [600, 3600, 86400, 604800, 2592000]
    while True:
        print("running....")
        regular_subcribed = [[] for i in range(5)]
        regular_search_subscription = SearchHistory.objects.filter(subscribed=True).order_by('-timestamp')
        regular_search_result = list(regular_search_subscription.values())
        for i in range(len(original)):
            for j in range(len(regular_search_result)):
                #print(result[j]["subscribed_frequency"])
                if regular_search_result[j]["subscribed_frequency"] == original[i]:
                    regular_subcribed[i].append(regular_search_result[j])
        print(regular_subcribed)
        advanced_subcribed = [[] for i in range(5)]
        advanced_search_subscription = AdvancedSearchHistory.objects.filter(subscribed=True).order_by('-timestamp')
        advanced_search_result = list(advanced_search_subscription.values())
        for i in range(len(original)):
            for j in range(len(advanced_search_result)):
                #print(result[j]["subscribed_frequency"])
                if advanced_search_result[j]["subscribed_frequency"] == original[i]:
                    advanced_subcribed[i].append(advanced_search_result[j])
        print(advanced_subcribed)
        #print(subcribed)
        for i in range(len(original)):
            if frequency_array[i] == 0:
                for each in regular_subcribed[i]:
                    regular_crawl_background(each)

                for each in advanced_subcribed[i]:
                    advanced_crawl_background(each)
                frequency_array[i] = original[i]
        for i in range(len(original)):
            frequency_array[i] -= repeat
        time.sleep(repeat)


def pass_forgot(request):
    return render(request, 'web_crawler/forgot_password.html')


def pass_change(request):
    return render(request, 'web_crawler/password_change.html')


def pass_change_success(request):
    return render(request, 'web_crawler/password_change_success.html')


def pass_found(request):
    return render(request, 'web_crawler/password_found.html')


def index1(request):
    return render(request, 'web_crawler/index1.html')


def dashboard(request):
    return render(request, 'web_crawler/dashboard.html')
def show_users(request):
    return render(request,'web_crawler/show_users.html')

def user_chart(request):
    #from research
    cursor = connection.cursor()
    query = '''SELECT COUNT (DISTINCT auth_user.username), FROM auth_user GROUP_BY auth_user.date_joined'''
    cursor.execute(query)
        #'''SELECT auth_user.username,FROM auth_user ORDER_BY auth_user.date_joined'''
    userdata = cursor.fetchall()
    data = [[0] for date in userdata]
    
    return JsonResponse(data={ 
        "data": data,
    })
def test(request):
    frequency_array = [0, 3600, 86400, 604800, 2592000]
    thread = threading.Thread(target=subscription_background(600, frequency_array), args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                  # Start the execution
    return render(request, 'web_crawler/index.html')
