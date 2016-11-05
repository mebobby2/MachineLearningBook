import random
from random import randint
from sets import Set

sites = [
  {
    'href': 'http://thc.segfault.net/root/phun/unmaintain.html',
    'title': 'How To Write Unmaintainable Code',
    'tags': ['programming', 'devops']
  },
  {
    'href': 'http://www.albahari.com/threading/',
    'title': 'Threading in C#',
    'tags': ['programming', 'C#']
  },
  {
    'href': 'http://www.gamespot.com',
    'title': 'Gaming Always',
    'tags': ['Gaming', 'Games']
  },
  {
    'href': 'http://www.stackoverflow.com',
    'title': 'Programming Paradise',
    'tags': ['Programming']
  },
  {
    'href': 'http://facebook.com',
    'title': 'Social Media',
    'tags': ['Social']

  },{
    'href': 'http://twitter.com',
    'title': 'Socila Media with Tweets',
    'tags': ['Social']
  },
  {
    'href': 'http://hulucat.com',
    'title': 'Bubble Tea',
    'tags': ['Drinks', 'Entertainment', 'Food']
  },
  {
    'href': 'http://goldenvillage.sg',
    'title': 'Movies Galore',
    'tags': ['Movies', 'Entertainment', 'Films']
  },
  {
    'href': 'http://propertyguru.com',
    'title': 'Looking for your next home?',
    'tags': ['Home', 'Living', 'Rent']
  },
  {
    'href': 'http://taobao.cn',
    'title': 'Buy Cheap!',
    'tags': ['Cheap', 'Lifestyle', 'Shopping']
  },
  {
    'href': 'http://cleanmyhouse.sg',
    'title': 'Rent a Cleaner',
    'tags': ['Home', 'Lifestyle']
  },
  {
    'href': 'http://www.funevents.com',
    'title': 'Fun Events Near You :)',
    'tags': ['Events', 'Social']
  },
  {
    'href': 'http://rapgenius.com',
    'title': 'Rap Genius',
    'tags': ['Rap', 'Entertainment', 'Hip Hop']
  }
]

users = [
  {
    'user': 'dorsia'
  },
  {
    'user': 'mmihale'
  },
  {
    'user': 'smellycat'
  },
  {
    'user': 'sunrise_kelly'
  },
  {
    'user': 'leapriKon'
  },
  {
    'user': 'nerd_with_g'
  },
  {
    'user': 'blaster'
  },
  {
    'user': 'stevendoe'
  },
  {
    'user': 'luda'
  },
  {
    'user': 'pops'
  }
]

def get_popular(tag = None):
  tagged_sites = []
  for site in sites:
    if tag in site['tags']:
      tagged_sites.append(site)
  return tagged_sites;

def get_urlposts(site_href):
  return random.choice(users)

def get_userposts(user):
  num_posts = randint(1,4)
  user_posts = Set([])
  while len(user_posts) < num_posts:
    site = random.choice(sites)
    user_posts.add(site['href'])
  extracter = lambda site: {'href': site}
  return map(extracter, user_posts)
