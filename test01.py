from csv import DictWriter
from operator import itemgetter

schools = [{'name': 'Carnegie Mellon University', 'rank': 1, 'ntnlRank': 25},
    {'name': 'Massachusetts Institute of Technology', 'rank': 1, 'ntnlRank': 7},
    {'name': 'Stanford University', 'rank': 1, 'ntnlRank': 4},
    {'name': 'Cornell University', 'rank': 6, 'ntnlRank': 15},
    {'name': 'University of Texas-Austin', 'rank': 9, 'ntnlRank': 53}]


def orderSchools():
    schoolsOrderedByRank = sorted(schools, key=itemgetter('rank', 'name'))[:]
    schoolsOrderedByName = sorted(schools, key=itemgetter('name', 'rank'))[:]
    schoolsOrderedByNtnlRank = sorted(schools, key=itemgetter('ntnlRank', 'name'))[:]
    
    return [schoolsOrderedByName, schoolsOrderedByRank, schoolsOrderedByNtnlRank]


orderedSchools = orderSchools()

with open('spreadsheettest.csv', 'w') as outfile:
    writer = DictWriter(outfile, ('name', 'rank', 'ntnlRank'))
    writer.writeheader()
    writer.writerows(schools)