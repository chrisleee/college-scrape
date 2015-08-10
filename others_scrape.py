__author__ = 'Christopher'
from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib2 import Request
from urllib2 import HTTPError
import csv
import bs4


def make_soup(url):
    html = ''
    request = ''
    try:
        request = Request(url, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
        html = urlopen(request).read()
    except HTTPError, e:
        print e
    return BeautifulSoup(html, "lxml")


def read_csv_links(file):
    """
    Takes in a csv file and returns a list of links
    """
    result_list = []

    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            result_list.append(row)

    return result_list[0][0].split(',')


def read_csv_dict(file):
    """
    Takes in a csv file and returns a list of dictionaries
    """
    result_dict = []

    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result_dict.append({'name': row['name'], 'rank': int(row['rank']), 'ntnl_rank': int(row['ntnl_rank'])})

    return result_dict


def college_transfer_scrape(schools):
    """
    Scrapes collegetransfer for stuff and adds it to each school in schools dict
    """

    links = read_csv_links('spreadsheettransfer.csv')

    for i, link in enumerate(links):
        print link
        soup = make_soup(link)

        deadlines = soup.find('section', attrs={'id': 'new-tp-appDeadlines'})

        try:
            fall_deadline = deadlines.find('tr', 'odd')
            fall_date = fall_deadline.find('td')
            print fall_date.text.encode('ascii', 'ignore')
            schools[i]['fall_date'] = fall_date.text.encode('ascii', 'ignore')
        except AttributeError:
            print 'N/A'
            schools[i]['fall_date'] = 'N/A'

        try:
            spring_deadline = deadlines.find('tr', 'even')
            spring_date = spring_deadline.find('td')
            print spring_date.text.encode('ascii', 'ignore')
            schools[i]['spring_date'] = spring_date.text.encode('ascii', 'ignore')
        except AttributeError:
            print 'N/A'
            schools[i]['spring_date'] = 'N/A'

        # finds tuition and adds to dict
        try:
            in_tuition = soup.find('th', text='In-State Tuition').parent
            in_tuition = in_tuition.find('td').text.encode('ascii', 'ignore').replace('$', '').replace(',', '')
            out_tuition = soup.find('th', text='Out-of-State Tuition').parent
            out_tuition = out_tuition.find('td').text.encode('ascii', 'ignore').replace('$', '').replace(',', '')
            print in_tuition, out_tuition
            schools[i]['in_tuition'] = int(in_tuition)
            schools[i]['out_tuition'] = int(out_tuition)
        except AttributeError:
            print 'N/A'
            schools[i]['in_tuition'] = 'N/A'
            schools[i]['out_tuition'] = 'N/A'

    return schools


def college_data_scrape(schools):
    """
    Scrapes collegedata for stuff and adds it to each school in schools dict
    """

    links = read_csv_links('spreadsheetdata.csv')

    for i, link in enumerate(links):
        try:
            print '-----------------'
            print link
            print schools[i]['name']
            soup = make_soup(link)

            # finds location of school and adds to dict
            location = soup.find('p', 'citystate')
            location = location.text.encode('ascii', 'ignore').strip()
            print location
            schools[i]['location'] = location

            # finds acceptance rate and adds to dict
            acceptance = soup.find('th', text='Overall Admission Rate').parent
            acceptance = acceptance.find('td').text.encode('ascii', 'ignore')
            print acceptance
            schools[i]['acceptance_rate'] = acceptance

            # finds entrance difficulty and adds to dict
            entrance_difficulty = soup.find('th', text='Entrance Difficulty').parent
            entrance_difficulty = entrance_difficulty.find('td').text.encode('ascii', 'ignore')
            if entrance_difficulty == '':
                entrance_difficulty = entrance_difficulty.replace('', 'N/A')
            print entrance_difficulty
            schools[i]['entrance_difficulty'] = entrance_difficulty

            # finds website and adds to dict
            website = soup.find('th', text='Web Site').parent
            website = website.find('a').text.encode('ascii', 'ignore')
            print website
            schools[i]['website'] = website

            # finds Institution type and adds to dict
            institution = soup.find('th', text='Institution Type').parent
            institution = institution.find('td').text.encode('ascii', 'ignore')
            print institution
            schools[i]['institution'] = institution

            # finds undergrad amount and adds to dict
            population = soup.find('th', text='Undergraduate Students').parent
            population = population.find('td').text.encode('ascii', 'ignore')
            print population
            schools[i]['undergrad_population'] = population

            # finds race enrollment and adds to dict
            race_list = []
            race = soup.find('th', text='Ethnicity of Students from U.S.').parent
            for srace in race.find('td'):
                if isinstance(srace,bs4.element.NavigableString):
                    if not []:
                        new_race = srace.encode('ascii', 'ignore')
                        race_list.append(new_race)
            print race_list
            schools[i]['race_diversity'] = race_list

            print '-----------------'
            print
        except AttributeError:
            schools[i]['location'] = 'N/A'
            schools[i]['acceptance_rate'] = 'N/A'
            schools[i]['entrance_difficulty'] = 'N/A'
            schools[i]['website'] = 'N/A'
            schools[i]['institution'] = 'N/A'
            schools[i]['undergrad_population'] = 'N/A'
            schools[i]['race_diversity'] = 'N/A'

    return schools


schools = read_csv_dict('spreadsheet.csv')

schools = college_transfer_scrape(schools)
schools = college_data_scrape(schools)

keys = ['name', 'rank', 'ntnl_rank', 'location', 'out_tuition', 'in_tuition', 'undergrad_population', 'acceptance_rate', 'fall_date', 'spring_date', 'entrance_difficulty', 'institution', 'race_diversity', 'website']

with open('spreadsheetDone.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(schools)