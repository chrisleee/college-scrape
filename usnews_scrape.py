from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib2 import Request
from urllib2 import HTTPError
from csv import DictWriter
from csv import writer
import json
import urllib
import urllib2
#from time import sleep

def make_soup(url):
    html = ''
    request = ''
    try:
        request = Request(url, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
        html = urlopen(request).read()
    except HTTPError, e:
        print e
    return BeautifulSoup(html, "lxml")


def get_rankings(section_url, schools, rankings):
    """
    Takes a URL and scrapes for the university name and the ranking
    
    Input: section_url - URL being scraped
    
    Output: [schools, rankings] - list of schools (str) and rankings (int)
    """
    soup = make_soup(section_url)
    
    for item in soup.findAll('span', 'rankscore-bronze'):
        rank = item.text.encode('ascii', 'ignore')
        rank = int(rank.translate(None, '#'))
        rankings.append(rank)
    for item in soup.findAll('a', 'school-name'):
        school = item.text.encode('ascii', 'replace').replace('?', ' ')
        school = school.replace('\\u200b', ' ').replace('\\u2014', ' ')
        schools.append(school)
    return [schools, rankings]


def page_flipper(BASE_URL):
    """
    Takes a base URL and uses get_rankings to scrape schools and ranks
    It then moves on to next page and repeats
    
    Input: BASE_URL - URL to start scrape with
    
    Output: [schools, rankings] - list of schools (str) and rankings (int)
    """
    soup = make_soup(BASE_URL)
    
    schools = []
    rankings = []
    schoolRanks = []
    pageLimit = 4
    index = 1
    
    while index <= pageLimit:
        section_url = BASE_URL + str(index)
        schoolRanks = get_rankings(section_url, schools, rankings)
        index += 1
    
    return schoolRanks


def create_school_dict():
    SCHOOLS_URL = "http://grad-schools.usnews.rankingsandreviews.com/best-graduate-schools/top-science-schools/computer-science-rankings/page+"
    schoolRanks = page_flipper(SCHOOLS_URL)
    newRanks = []

    for i in range(len(schoolRanks[0])):
        newRanks.append({'name': schoolRanks[0][i], 'rank': schoolRanks[1][i]})
    
    return newRanks


def bing_search(schools, website):
    """
    Takes in dict of schools and a website to search for and creates a list of the first result links
    
    INPUT: schools - dict of schools
    INPUT: website - desired website links
    
    OUTPUT: web_links - list of web links obtained from first result of each google search
    """ 
    web_links = []
    
    for school in schools:
        NEW_URL =  school['name'] + ' site:' + website
        print NEW_URL
        web_links.append(bing_search2(NEW_URL, 'Web'))
    
    return web_links

def bing_search2(query, search_type):
    #search_type: Web, Image, News, Video
    key= ''  # removed key entry because githib project is public
    query = urllib.quote(query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=1&$format=json'
    request = urllib2.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    request_opener = urllib2.build_opener()
    response = request_opener.open(request) 
    response_data = response.read()
    json_result = json.loads(response_data)
    result_list = json_result['d']['results']
    return result_list[0][u'Url']

def usnews_ntnl_rank(schools):
    """
    Scrapes usnews for national rank and adds it to each school in schools dict
    """
    
    links = bing_search(schools, 'colleges.usnews.rankingsandreviews.com/')
    
    # iterate through each link and scrape for ntnl rank
    for i, link in enumerate(links):
        soup = make_soup(link)
    
        for item in soup.findAll('span', 'rankscore-bronze cluetip cluetip-stylized'):
            rank = item.text.encode('ascii', 'ignore').replace('Tie', '')
            rank = int(rank.translate(None, '#'))
        
        schools[i]['ntnl_rank'] = rank
    
    return schools


def college_transfer_scrape(schools):
    """
    Scrapes collegetransfer for stuff and adds it to each school in schools dict
    """
    
    #links =

    #for i, link in enumerate(links):
    #    soup = make_soup(link)
        
    #    for item in soup.findAll():
    #        stuff = ''
        
    #    schools[i]['item'] = stuff
    
    return schools
    
    
def college_data_scrape(schools, links):
    """
    Scrapes collegedata for stuff and adds it to each school in schools dict
    """
    
    #links =

    #for i, link in enumerate(links):
    #    soup = make_soup(link)
        
    #    for item in soup.findAll():
    #        stuff = ''
        
    #    schools[i]['item'] = stuff
    
    return schools
    


#schools = create_school_dict()
#schools = usnews_ntnl_rank(schools)

