###按年份爬取每一年所有比赛的比赛结果
###Column: Team1, Team2, Home/Away, Result, Team1Score, Team2Score

from bs4 import BeautifulSoup
import requests
import time

import re
import pickle


urlnamelist = ['abilene-christian', 'air-force', 'akron', 'alabama-am', 'alabama', 'alabama-state', 'alabama-birmingham', 'albany-ny', 'alcorn-state', 'american', 'appalachian-state', 'arizona-state', 'arizona', 'arkansas', 'arkansas-state', 'arkansas-little-rock', 'arkansas-pine-bluff', 'army', 'auburn', 'austin-peay', 'ball-state', 'baylor', 'belmont', 'bethune-cookman', 'binghamton', 'boise-state', 'boston-college', 'boston-university', 'bowling-green-state', 'bradley', 'brigham-young', 'brown', 'bryant', 'bucknell', 'buffalo', 'butler', 'cal-poly', 'cal-state-bakersfield', 'cal-state-fullerton', 'cal-state-northridge', 'campbell', 'canisius', 'central-arkansas', 'central-connecticut-state', 'central-florida', 'central-michigan', 'charleston-southern', 'charlotte', 'chattanooga', 'chicago-state', 'cincinnati', 'citadel', 'clemson', 'cleveland-state', 'coastal-carolina', 'colgate', 'college-of-charleston', 'colorado', 'colorado-state', 'columbia', 'connecticut', 'coppin-state', 'cornell', 'creighton', 'dartmouth', 'davidson', 'dayton', 'delaware', 'delaware-state', 'denver', 'depaul', 'detroit-mercy', 'drake', 'drexel', 'duke', 'duquesne', 'east-carolina', 'east-tennessee-state', 'eastern-illinois', 'eastern-kentucky', 'eastern-michigan', 'eastern-washington', 'elon', 'evansville', 'fairfield', 'fairleigh-dickinson', 'florida-am', 'florida-atlantic', 'florida', 'florida-gulf-coast', 'florida-international', 'florida-state', 'fordham', 'fresno-state', 'furman', 'gardner-webb', 'george-mason', 'george-washington', 'georgetown', 'georgia', 'georgia-southern', 'georgia-state', 'georgia-tech', 'gonzaga', 'grambling', 'grand-canyon', 'green-bay', 'hampton', 'hartford', 'harvard', 'hawaii', 'high-point', 'hofstra', 'holy-cross', 'houston-baptist', 'houston', 'howard', 'idaho-state', 'idaho', 'illinois', 'illinois-state', 'illinois-chicago', 'incarnate-word', 'indiana', 'indiana-state', 'iona', 'iowa', 'iowa-state', 'ipfw', 'iupui', 'jackson-state', 'jacksonville', 'jacksonville-state', 'james-madison', 'kansas', 'kansas-state', 'kennesaw-state', 'kent-state', 'kentucky', 'la-salle', 'lafayette', 'lamar', 'lehigh', 'liberty', 'lipscomb', 'long-beach-state', 'long-island-university', 'longwood', 'louisiana-state', 'louisiana-tech', 'louisiana-lafayette', 'louisiana-monroe', 'louisville', 'loyola-il', 'loyola-md', 'loyola-marymount', 'maine', 'manhattan', 'marist', 'marquette', 'marshall', 'maryland', 'maryland-baltimore-county', 'maryland-eastern-shore', 'massachusetts', 'massachusetts-lowell', 'mcneese-state', 'memphis', 'mercer', 'miami-fl', 'miami-oh', 'michigan-state', 'michigan', 'middle-tennessee', 'milwaukee', 'minnesota', 'mississippi', 'mississippi-state', 'mississippi-valley-state', 'missouri-state', 'missouri', 'missouri-kansas-city', 'monmouth', 'montana', 'montana-state', 'morehead-state', 'morgan-state', 'mount-st-marys', 'murray-state', 'navy', 'nebraska', 'nebraska-omaha', 'nevada', 'nevada-las-vegas', 'new-hampshire', 'new-mexico', 'new-mexico-state', 'new-orleans', 'niagara', 'nicholls-state', 'njit', 'norfolk-state', 'north-carolina-at', 'north-carolina-central', 'north-carolina-state', 'north-carolina', 'north-carolina-asheville', 'north-carolina-greensboro', 'north-carolina-wilmington', 'north-dakota-state', 'north-dakota', 'north-florida', 'north-texas', 'northeastern', 'northern-arizona', 'northern-colorado', 'northern-illinois', 'northern-iowa', 'northern-kentucky', 'northwestern-state', 'northwestern', 'notre-dame', 'oakland', 'ohio', 'ohio-state', 'oklahoma', 'oklahoma-state', 'old-dominion', 'oral-roberts', 'oregon', 'oregon-state', 'pacific', 'penn-state', 'pennsylvania', 'pepperdine', 'pittsburgh', 'portland', 'portland-state', 'prairie-view', 'presbyterian', 'princeton', 'providence', 'purdue', 'quinnipiac', 'radford', 'rhode-island', 'rice', 'richmond', 'rider', 'robert-morris', 'rutgers', 'sacramento-state', 'sacred-heart', 'saint-francis-pa', 'saint-josephs', 'saint-louis', 'saint-marys-ca', 'saint-peters', 'sam-houston-state', 'samford', 'san-diego-state', 'san-diego', 'san-francisco', 'san-jose-state', 'santa-clara', 'savannah-state', 'seattle', 'seton-hall', 'siena', 'south-alabama', 'south-carolina', 'south-carolina-state', 'south-carolina-upstate', 'south-dakota', 'south-dakota-state', 'south-florida', 'southeast-missouri-state', 'southeastern-louisiana', 'southern-california', 'southern-illinois', 'southern-illinois-edwardsville', 'southern', 'southern-methodist', 'southern-mississippi', 'southern-utah', 'st-bonaventure', 'st-francis-ny', 'st-johns-ny', 'stanford', 'stephen-f-austin', 'stetson', 'stony-brook', 'syracuse', 'temple', 'tennessee-state', 'tennessee-tech', 'tennessee', 'tennessee-martin', 'texas-am', 'texas-am-corpus-christi', 'texas-christian', 'texas', 'texas-southern', 'texas-state', 'texas-tech', 'texas-arlington', 'texas-el-paso', 'texas-pan-american', 'texas-san-antonio', 'toledo', 'towson', 'troy', 'tulane', 'tulsa', 'california-davis', 'california-irvine', 'california-riverside', 'california-santa-barbara', 'ucla', 'california', 'utah-state', 'utah', 'utah-valley', 'valparaiso', 'vanderbilt', 'vermont', 'villanova', 'virginia', 'virginia-commonwealth', 'virginia-military-institute', 'virginia-tech', 'wagner', 'wake-forest', 'washington', 'washington-state', 'weber-state', 'west-virginia', 'western-carolina', 'western-illinois', 'western-kentucky', 'western-michigan', 'wichita-state', 'william-mary', 'winthrop', 'wisconsin', 'wofford', 'wright-state', 'wyoming', 'xavier', 'yale', 'youngstown-state']
# schoolnamelist = ['Abilene Christian Wildcats', 'Air Force Falcons', 'Akron Zips', 'Alabama A&M Bulldogs', 'Alabama Crimson Tide', 'Alabama State Hornets', 'Alabama-Birmingham Blazers', 'Albany (NY) Great Danes', 'Alcorn State Braves', 'American Eagles', 'Appalachian State Mountaineers', 'Arizona State Sun Devils', 'Arizona Wildcats', 'Arkansas Razorbacks', 'Arkansas State Red Wolves', 'Arkansas-Little Rock Trojans', 'Arkansas-Pine Bluff Golden Lions', 'Army Black Knights', 'Auburn Tigers', 'Austin Peay Governors', 'Ball State Cardinals', 'Baylor Bears', 'Belmont Bruins', 'Bethune-Cookman Wildcats', 'Binghamton Bearcats', 'Boise State Broncos', 'Boston College Eagles', 'Boston University Terriers', 'Bowling Green State Falcons', 'Bradley Braves', 'Brigham Young Cougars', 'Brown Bears', 'Bryant Bulldogs', 'Bucknell Bison', 'Buffalo Bulls', 'Butler Bulldogs', 'Cal Poly Mustangs', 'Cal State Bakersfield Roadrunners', 'Cal State Fullerton Titans', 'Cal State Northridge Matadors', 'Campbell Fighting Camels', 'Canisius Golden Griffins', 'Central Arkansas Bears', 'Central Connecticut State Blue Devils', 'Central Florida Knights', 'Central Michigan Chippewas', 'Charleston Southern Buccaneers', 'Charlotte 49ers', 'Chattanooga Mocs', 'Chicago State Cougars', 'Cincinnati Bearcats', 'Citadel Bulldogs', 'Clemson Tigers', 'Cleveland State Vikings', 'Coastal Carolina Chanticleers', 'Colgate Raiders', 'College of Charleston Cougars', 'Colorado Buffaloes', 'Colorado State Rams', 'Columbia Lions', 'Connecticut Huskies', 'Coppin State Eagles', 'Cornell Big Red', 'Creighton Bluejays', 'Dartmouth Big Green', 'Davidson Wildcats', 'Dayton Flyers', "Delaware Fightin' Blue Hens", 'Delaware State Hornets', 'Denver Pioneers', 'DePaul Blue Demons', 'Detroit Mercy Titans', 'Drake Bulldogs', 'Drexel Dragons', 'Duke Blue Devils', 'Duquesne Dukes', 'East Carolina Pirates', 'East Tennessee State Buccaneers', 'Eastern Illinois Panthers', 'Eastern Kentucky Colonels', 'Eastern Michigan Eagles', 'Eastern Washington Eagles', 'Elon Phoenix', 'Evansville Purple Aces', 'Fairfield Stags', 'Fairleigh Dickinson Knights', 'Florida A&M Rattlers', 'Florida Atlantic Owls', 'Florida Gators', 'Florida Gulf Coast Eagles', 'Florida International Panthers', 'Florida State Seminoles', 'Fordham Rams', 'Fresno State Bulldogs', 'Furman Paladins', "Gardner-Webb Runnin' Bulldogs", 'George Mason Patriots', 'George Washington Colonials', 'Georgetown Hoyas', 'Georgia Bulldogs', 'Georgia Southern Eagles', 'Georgia State Panthers', 'Georgia Tech Yellow Jackets', 'Gonzaga Bulldogs', 'Grambling Tigers', 'Grand Canyon Antelopes', 'Green Bay Phoenix', 'Hampton Pirates', 'Hartford Hawks', 'Harvard Crimson', 'Hawaii Warriors', 'High Point Panthers', 'Hofstra Pride', 'Holy Cross Crusaders', 'Houston Baptist Huskies', 'Houston Cougars', 'Howard Bison', 'Idaho State Bengals', 'Idaho Vandals', 'Illinois Fighting Illini', 'Illinois State Redbirds', 'Illinois-Chicago Flames', 'Incarnate Word Cardinals', 'Indiana Hoosiers', 'Indiana State Sycamores', 'Iona Gaels', 'Iowa Hawkeyes', 'Iowa State Cyclones', 'IPFW Mastodons', 'IUPUI Jaguars', 'Jackson State Tigers', 'Jacksonville Dolphins', 'Jacksonville State Gamecocks', 'James Madison Dukes', 'Kansas Jayhawks', 'Kansas State Wildcats', 'Kennesaw State Owls', 'Kent State Golden Flashes', 'Kentucky Wildcats', 'La Salle Explorers', 'Lafayette Leopards', 'Lamar Cardinals', 'Lehigh Mountain Hawks', 'Liberty Flames', 'Lipscomb Bisons', 'Long Beach State 49ers', 'Long Island University Blackbirds', 'Longwood Lancers', 'Louisiana State Fighting Tigers', 'Louisiana Tech Bulldogs', "Louisiana-Lafayette Ragin' Cajuns", 'Louisiana-Monroe Warhawks', 'Louisville Cardinals', 'Loyola (IL) Ramblers', 'Loyola (MD) Greyhounds', 'Loyola Marymount Lions', 'Maine Black Bears', 'Manhattan Jaspers', 'Marist Red Foxes', 'Marquette Golden Eagles', 'Marshall Thundering Herd', 'Maryland Terrapins', 'Maryland-Baltimore County Retrievers', 'Maryland-Eastern Shore Hawks', 'Massachusetts Minutemen', 'Massachusetts-Lowell River Hawks', 'McNeese State Cowboys', 'Memphis Tigers', 'Mercer Bears', 'Miami (FL) Hurricanes', 'Miami (OH) RedHawks', 'Michigan State Spartans', 'Michigan Wolverines', 'Middle Tennessee Blue Raiders', 'Milwaukee Panthers', 'Minnesota Golden Gophers', 'Mississippi Rebels', 'Mississippi State Bulldogs', 'Mississippi Valley State Delta Devils', 'Missouri State Bears', 'Missouri Tigers', 'Missouri-Kansas City Kangaroos', 'Monmouth Hawks', 'Montana Grizzlies', 'Montana State Bobcats', 'Morehead State Eagles', 'Morgan State Bears', "Mount St. Mary's Mountaineers", 'Murray State Racers', 'Navy Midshipmen', 'Nebraska Cornhuskers', 'Nebraska-Omaha Mavericks', 'Nevada Wolf Pack', 'Nevada-Las Vegas Rebels', 'New Hampshire Wildcats', 'New Mexico Lobos', 'New Mexico State Aggies', 'New Orleans Privateers', 'Niagara Purple Eagles', 'Nicholls State Colonels', 'NJIT Highlanders', 'Norfolk State Spartans', 'North Carolina A&T Aggies', 'North Carolina Central Eagles', 'North Carolina State Wolfpack', 'North Carolina Tar Heels', 'North Carolina-Asheville Bulldogs', 'North Carolina-Greensboro Spartans', 'North Carolina-Wilmington Seahawks', 'North Dakota State Bison', 'North Dakota UND', 'North Florida Ospreys', 'North Texas Mean Green', 'Northeastern Huskies', 'Northern Arizona Lumberjacks', 'Northern Colorado Bears', 'Northern Illinois Huskies', 'Northern Iowa Panthers', 'Northern Kentucky Norse', 'Northwestern State Demons', 'Northwestern Wildcats', 'Notre Dame Fighting Irish', 'Oakland Golden Grizzlies', 'Ohio Bobcats', 'Ohio State Buckeyes', 'Oklahoma Sooners', 'Oklahoma State Cowboys', 'Old Dominion Monarchs', 'Oral Roberts Golden Eagles', 'Oregon Ducks', 'Oregon State Beavers', 'Pacific Tigers', 'Penn State Nittany Lions', 'Pennsylvania Quakers', 'Pepperdine Waves', 'Pittsburgh Panthers', 'Portland Pilots', 'Portland State Vikings', 'Prairie View Panthers', 'Presbyterian Blue Hose', 'Princeton Tigers', 'Providence Friars', 'Purdue Boilermakers', 'Quinnipiac Bobcats', 'Radford Highlanders', 'Rhode Island Rams', 'Rice Owls', 'Richmond Spiders', 'Rider Broncs', 'Robert Morris Colonials', 'Rutgers Scarlet Knights', 'Sacramento State Hornets', 'Sacred Heart Pioneers', 'Saint Francis (PA) Red Flash', "Saint Joseph's Hawks", 'Saint Louis Billikens', "Saint Mary's (CA) Gaels", "Saint Peter's Peacocks", 'Sam Houston State Bearkats', 'Samford Bulldogs', 'San Diego State Aztecs', 'San Diego Toreros', 'San Francisco Dons', 'San Jose State Spartans', 'Santa Clara Broncos', 'Savannah State Tigers', 'Seattle Redhawks', 'Seton Hall Pirates', 'Siena Saints', 'South Alabama Jaguars', 'South Carolina Gamecocks', 'South Carolina State Bulldogs', 'South Carolina Upstate Spartans', 'South Dakota Coyotes', 'South Dakota State Jackrabbits', 'South Florida Bulls', 'Southeast Missouri State Redhawks', 'Southeastern Louisiana Lions', 'Southern California Trojans', 'Southern Illinois Salukis', 'Southern Illinois-Edwardsville Cougars', 'Southern Jaguars', 'Southern Methodist Mustangs', 'Southern Mississippi Golden Eagles', 'Southern Utah Thunderbirds', 'St. Bonaventure Bonnies', 'St. Francis (NY) Terriers', "St. John's (NY) Red Storm", 'Stanford Cardinal', 'Stephen F. Austin Lumberjacks', 'Stetson Hatters', 'Stony Brook Seawolves', 'Syracuse Orange', 'Temple Owls', 'Tennessee State Tigers', 'Tennessee Tech Golden Eagles', 'Tennessee Volunteers', 'Tennessee-Martin Skyhawks', 'Texas A&M Aggies', 'Texas A&M-Corpus Christi Islanders', 'Texas Christian Horned Frogs', 'Texas Longhorns', 'Texas Southern Tigers', 'Texas State Bobcats', 'Texas Tech Red Raiders', 'Texas-Arlington Mavericks', 'Texas-El Paso Miners', 'Texas-Rio Grande Valley Vaqueros', 'Texas-San Antonio Roadrunners', 'Toledo Rockets', 'Towson Tigers', 'Troy Trojans', 'Tulane Green Wave', 'Tulsa Golden Hurricane', 'UC-Davis Aggies', 'UC-Irvine Anteaters', 'UC-Riverside Highlanders', 'UC-Santa Barbara Gauchos', 'UCLA Bruins', 'University of California Golden Bears', 'Utah State Aggies', 'Utah Utes', 'Utah Valley Wolverines', 'Valparaiso Crusaders', 'Vanderbilt Commodores', 'Vermont Catamounts', 'Villanova Wildcats', 'Virginia Cavaliers', 'Virginia Commonwealth Rams', 'Virginia Military Institute Keydets', 'Virginia Tech Hokies', 'Wagner Seahawks', 'Wake Forest Demon Deacons', 'Washington Huskies', 'Washington State Cougars', 'Weber State Wildcats', 'West Virginia Mountaineers', 'Western Carolina Catamounts', 'Western Illinois Leathernecks', 'Western Kentucky Hilltoppers', 'Western Michigan Broncos', 'Wichita State Shockers', 'William & Mary Tribe', 'Winthrop Eagles', 'Wisconsin Badgers', 'Wofford Terriers', 'Wright State Raiders', 'Wyoming Cowboys', 'Xavier Musketeers', 'Yale Bulldogs', 'Youngstown State Penguins']
schoolnamelist = ['Abilene Christian', 'Air Force', 'Akron', 'Alabama A&M', 'Alabama-Birmingham', 'Alabama State', 'Alabama', 'Albany (NY)', 'Alcorn State', 'American', 'Appalachian State', 'Arizona State', 'Arizona', 'Arkansas-Little Rock', 'Arkansas-Pine Bluff', 'Arkansas State', 'Arkansas', 'Army', 'Auburn', 'Austin Peay', 'Ball State', 'Baylor', 'Belmont', 'Bethune-Cookman', 'Binghamton', 'Boise State', 'Boston College', 'Boston University', 'Bowling Green State', 'Bradley', 'Brigham Young', 'Brown', 'Bryant', 'Bucknell', 'Buffalo', 'Butler', 'Cal Poly', 'Cal State Bakersfield', 'Cal State Fullerton', 'Cal State Northridge', 'UC-Davis', 'UC-Irvine', 'UC-Riverside', 'UC-Santa Barbara', 'University of California', 'Campbell', 'Canisius', 'Central Arkansas', 'Central Connecticut State', 'Central Florida', 'Central Michigan', 'Charleston Southern', 'Charlotte', 'Chattanooga', 'Chicago State', 'Cincinnati', 'Citadel', 'Clemson', 'Cleveland State', 'Coastal Carolina', 'Colgate', 'College of Charleston', 'Colorado State', 'Colorado', 'Columbia', 'Connecticut', 'Coppin State', 'Cornell', 'Creighton', 'Dartmouth', 'Davidson', 'Dayton', 'Delaware State', 'Delaware', 'Denver', 'DePaul', 'Detroit Mercy', 'Drake', 'Drexel', 'Duke', 'Duquesne', 'East Carolina', 'East Tennessee State', 'Eastern Illinois', 'Eastern Kentucky', 'Eastern Michigan', 'Eastern Washington', 'Elon', 'Evansville', 'Fairfield', 'Fairleigh Dickinson', 'Florida A&M', 'Florida Atlantic', 'Florida Gulf Coast', 'Florida International', 'Florida State', 'Florida', 'Fordham', 'Fresno State', 'Furman', 'Gardner-Webb', 'George Mason', 'George Washington', 'Georgetown', 'Georgia Southern', 'Georgia State', 'Georgia Tech', 'Georgia', 'Gonzaga', 'Grambling', 'Grand Canyon', 'Green Bay', 'Hampton', 'Hartford', 'Harvard', 'Hawaii', 'High Point', 'Hofstra', 'Holy Cross', 'Houston Baptist', 'Houston', 'Howard', 'Idaho State', 'Idaho', 'Illinois-Chicago', 'Illinois State', 'Illinois', 'Incarnate Word', 'Indiana State', 'Indiana', 'Iona', 'Iowa State', 'Iowa', 'IPFW', 'IUPUI', 'Jackson State', 'Jacksonville State', 'Jacksonville', 'James Madison', 'Kansas State', 'Kansas', 'Kennesaw State', 'Kent State', 'Kentucky', 'La Salle', 'Lafayette', 'Lamar', 'Lehigh', 'Liberty', 'Lipscomb', 'Long Beach State', 'Long Island University', 'Longwood', 'Louisiana-Lafayette', 'Louisiana-Monroe', 'Louisiana State', 'Louisiana Tech', 'Louisville', 'Loyola (IL)', 'Loyola Marymount', 'Loyola (MD)', 'Maine', 'Manhattan', 'Marist', 'Marquette', 'Marshall', 'Maryland-Baltimore County', 'Maryland-Eastern Shore', 'Maryland', 'Massachusetts-Lowell', 'Massachusetts', 'McNeese State', 'Memphis', 'Mercer', 'Miami (FL)', 'Miami (OH)', 'Michigan State', 'Michigan', 'Middle Tennessee', 'Milwaukee', 'Minnesota', 'Mississippi State', 'Mississippi Valley State', 'Mississippi', 'Missouri-Kansas City', 'Missouri State', 'Missouri', 'Monmouth', 'Montana State', 'Montana', 'Morehead State', 'Morgan State', "Mount St. Mary's", 'Murray State', 'Navy', 'Nebraska-Omaha', 'Nebraska', 'Nevada-Las Vegas', 'Nevada', 'New Hampshire', 'New Mexico State', 'New Mexico', 'New Orleans', 'Niagara', 'Nicholls State', 'NJIT', 'Norfolk State', 'North Carolina-Asheville', 'North Carolina A&T', 'North Carolina Central', 'North Carolina-Greensboro', 'North Carolina State', 'North Carolina-Wilmington', 'North Carolina', 'North Dakota State', 'North Dakota', 'North Florida', 'North Texas', 'Northeastern', 'Northern Arizona', 'Northern Colorado', 'Northern Illinois', 'Northern Iowa', 'Northern Kentucky', 'Northwestern State', 'Northwestern', 'Notre Dame', 'Oakland', 'Ohio State', 'Ohio', 'Oklahoma State', 'Oklahoma', 'Old Dominion', 'Oral Roberts', 'Oregon State', 'Oregon', 'Pacific', 'Penn State', 'Pennsylvania', 'Pepperdine', 'Pittsburgh', 'Portland State', 'Portland', 'Prairie View', 'Presbyterian', 'Princeton', 'Providence', 'Purdue', 'Quinnipiac', 'Radford', 'Rhode Island', 'Rice', 'Richmond', 'Rider', 'Robert Morris', 'Rutgers', 'Sacramento State', 'Sacred Heart', 'Saint Francis (PA)', "Saint Joseph's", 'Saint Louis', "Saint Mary's (CA)", "Saint Peter's", 'Sam Houston State', 'Samford', 'San Diego State', 'San Diego', 'San Francisco', 'San Jose State', 'Santa Clara', 'Savannah State', 'Seattle', 'Seton Hall', 'Siena', 'South Alabama', 'South Carolina State', 'South Carolina Upstate', 'South Carolina', 'South Dakota State', 'South Dakota', 'South Florida', 'Southeast Missouri State', 'Southeastern Louisiana', 'Southern California', 'SIU Edwardsville', 'Southern Illinois', 'Southern Methodist', 'Southern Mississippi', 'Southern Utah', 'Southern', 'St. Bonaventure', 'St. Francis (NY)', "St. John's (NY)", 'Stanford', 'Stephen F. Austin', 'Stetson', 'Stony Brook', 'Syracuse', 'Temple', 'Tennessee-Martin', 'Tennessee State', 'Tennessee Tech', 'Tennessee', 'Texas A&M-Corpus Christi', 'Texas A&M', 'Texas-Arlington', 'Texas Christian', 'Texas-El Paso', 'Texas-Rio Grande Valley', 'Texas-San Antonio', 'Texas Southern', 'Texas State', 'Texas Tech', 'Texas', 'Toledo', 'Towson', 'Troy', 'Tulane', 'Tulsa', 'UCLA', 'Utah State', 'Utah Valley', 'Utah', 'Valparaiso', 'Vanderbilt', 'Vermont', 'Villanova', 'Virginia Commonwealth', 'VMI', 'Virginia Tech', 'Virginia', 'Wagner', 'Wake Forest', 'Washington State', 'Washington', 'Weber State', 'West Virginia', 'Western Carolina', 'Western Illinois', 'Western Kentucky', 'Western Michigan', 'Wichita State', 'William & Mary', 'Winthrop', 'Wisconsin', 'Wofford', 'Wright State', 'Wyoming', 'Xavier', 'Yale', 'Youngstown State']
# yearlist = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']
yearlist = ['2015', '2016']


for year in yearlist:
    print(year)
    ###在下一行输入文件的保存路径，格式csv
    with open(str(year + 'GameResult.csv'), 'w') as f:
        for i in range(0, len(urlnamelist)):
            url = "www.sports-reference.com/cbb/schools/" + str(urlnamelist[i]) + "/" + year + "-schedule.html"
            r = requests.get("http://" + url)
            if str(r) != '<Response [404]>':
                print(i)
                data = r.text
                soup = BeautifulSoup(data, "html.parser")
                # print(soup.get_text)
                for a in soup.find_all('tr'):
                    b = a.find_all('td')
                    # print(b)
                    if b:
                        # print(b[5])
                        # b[4]主客场，b[5]对手, b[7]输赢，b[8]一队得分，b[9]二队得分
                        # print(b[5].contents[0])
                        # 2015-2017 format
                        if int(year) >= 2015:
                            if 'href' in str(b[5].contents[0]):
                                #For home, H = home for t1, A = away for t1, N = Netrual Place
                                if b[4].contents:
                                    if b[4].contents[0] == '@':
                                        home = 'A'
                                    else:
                                        home = 'N'
                                else:
                                    home = 'H'
                                oppo = b[5].contents[0].contents[0]
                                result = b[7].contents[0]
                                t1score = b[8].contents[0]
                                t2score = b[9].contents[0]
                                f.write(schoolnamelist[i] + ',' + oppo + ',' + home + ',' + result + ',' + t1score + ',' + t2score + '\n')
                        # 2010-2014 format
                        else:
                            # b[2]主客场，b[3]对手, b[5]输赢，b[6]一队得分，b[7]二队得分
                            if 'href' in str(b[3].contents[0]):
                                if b[2].contents:
                                    if b[2].contents[0] == '@':
                                        home = 'A'
                                    else:
                                        home = 'N'
                                else:
                                    home = 'H'
                                oppo = b[3].contents[0].contents[0]
                                result = b[5].contents[0]
                                t1score = b[6].contents[0]
                                t2score = b[7].contents[0]
                                f.write(schoolnamelist[i] + ',' + oppo + ',' + home + ',' + result + ',' + t1score + ',' + t2score + '\n')
        f.close()
    # time.sleep(60)