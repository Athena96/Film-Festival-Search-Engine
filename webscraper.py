import requests
import sys
import string
from bs4 import BeautifulSoup
from read_write import ReadWrite

class FilmFestivalWikiWebScraper:

    def good_quality(self,word_vector):

        for word in word_vector:
            if word == "" or word == " ":
                return False
        return True

    def scrape_screened_wiki(self, festival, year, link):
        # place to store scraped data
        scraped_screened_films = []

        # init BeautifulSoup
        response = requests.get(link, headers={
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko)'})
        soup = BeautifulSoup(response.text, 'lxml')

        # pointer to the wiki table, containing films
        table = soup.find('table', {"class" :"wikitable"}) # TODO

        # iterate over each row in table
        for row in table.findAll("tr"):

            # break down into cells
            cells = row.findAll("td")

            # correct num cells
            if len(cells) >= 3: # TODO

                # extract film title
                title = cells[0].find(text=True)
                if title == None:
                    continue
                title = str(title.encode('ascii', 'ignore').decode('ascii'))

                dir_id = 0
                country_id = 0
                # if cell is of type len = 4
                if len(cells) == 3:
                    dir_id = 1
                    country_id = 2
                # if cell is of type len = 5
                elif len(cells) == 4:
                    dir_id = 2
                    country_id = 3

                director = cells[dir_id].find(text=True)
                director = str(director.encode('ascii', 'ignore').decode('ascii'))

                country = cells[country_id].find(text=True)
                country = str(country.encode('ascii', 'ignore').decode('ascii'))

                # check title OK
                title_parts = title.split(" ")
                title_parts_lc = [t.lower() for t in title_parts]
                title_parts_lc_noPunc = [t.translate(None, string.punctuation) for t in title_parts_lc]

                if self.good_quality(title_parts_lc_noPunc) == False:
                    continue


                # check title OK
                director_parts = director.split(" ")
                director_parts_lc = [d.lower() for d in director_parts]
                director_parts_lc_noPunc = [d.translate(None, string.punctuation) for d in director_parts_lc]



                if self.good_quality(director_parts_lc_noPunc) == False:
                    continue


                scraped_screened_films.append((year,title,director,country,festival, "_"))

        return scraped_screened_films

    def scrape_awards_wiki(self, festival, link):
        # place to store scraped data
        scraped_award_films = []

        # init BeautifulSoup
        response = requests.get(link, headers={
                'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko)'})
        soup = BeautifulSoup(response.text, 'lxml')

        # pointer to the wiki table, containing films
        table = soup.find("table", {"class" : "wikitable sortable"})

        # iterate over each row in table
        for row in table.findAll("tr"):

            # break down into cells
            cells = row.findAll("td")

            # correct num cells
            if len(cells) >= 4:

                # extract film year and cinvert to int
                year = cells[0].find(text=True)
                year = str(year.encode('ascii', 'ignore').decode('ascii'))

                try:
                    filmYearInt = int(year)
                    if filmYearInt < 1949:
                        continue
                except ValueError:
                    continue

                title = cells[1].find(text=True)
                title = str(title.encode('ascii', 'ignore').decode('ascii'))

                dir_id = 0
                country_id = 0
                # if cell is of type len = 4
                if len(cells) == 4:
                    dir_id = 2
                    country_id = 3
                # if cell is of type len = 5
                elif len(cells) == 5:
                    dir_id = 3
                    country_id = 4

                director = cells[dir_id].find(text=True)
                director = str(director.encode('ascii', 'ignore').decode('ascii'))

                country = cells[country_id].find(text=True)
                country = str(country.encode('ascii', 'ignore').decode('ascii'))

                # check title OK
                title_parts = title.split(" ")
                title_parts_lc = [t.lower() for t in title_parts]
                title_parts_lc_noPunc = [t.translate(None, string.punctuation) for t in title_parts_lc]

                if any(len(x) <= 1 for x in title_parts_lc_noPunc):
                    continue


                # check title OK
                director_parts = director.split(" ")
                director_parts_lc = [d.lower() for d in director_parts]
                director_parts_lc_noPunc = [d.translate(None, string.punctuation) for d in director_parts_lc]


                if any(len(x) <= 2 for x in director_parts_lc_noPunc):
                    continue
                scraped_award_films.append( (year, title, director, country, festival, "Award") )

        return scraped_award_films

    def merge_award_and_screened_data(self,award_films, screened_films):
        local_scraped_awards_page_data = award_films
        local_scraped_screening_data = screened_films

        merged_data = []

        for aId,award_film in enumerate(local_scraped_awards_page_data):

            for sId,screened_film in enumerate(local_scraped_screening_data):

                if award_film[1] == screened_film[1]:

                    del local_scraped_screening_data[sId]

        for award_film in local_scraped_awards_page_data:
            merged_data.append(award_film)
        for screened_film in local_scraped_screening_data:
            merged_data.append(screened_film)

        return merged_data



# Main
# python webscraper.py
if len(sys.argv) == 1:

    festivals = ["Cannes", "Berlin", "Venice"]

    links = [ ( "https://en.wikipedia.org/wiki/Palme_d%27Or",[
                ("2009","https://en.wikipedia.org/wiki/2009_Cannes_Film_Festival"),
                ("2010","https://en.wikipedia.org/wiki/2010_Cannes_Film_Festival"),
                ("2011","https://en.wikipedia.org/wiki/2011_Cannes_Film_Festival"),
                ("2012","https://en.wikipedia.org/wiki/2012_Cannes_Film_Festival"),
                ("2013","https://en.wikipedia.org/wiki/2013_Cannes_Film_Festival"),
                ("2014","https://en.wikipedia.org/wiki/2014_Cannes_Film_Festival"),
                ("2015","https://en.wikipedia.org/wiki/2015_Cannes_Film_Festival"),
                ("2016","https://en.wikipedia.org/wiki/2016_Cannes_Film_Festival"),
                ("2017","https://en.wikipedia.org/wiki/2017_Cannes_Film_Festival") ] ),

            ( "https://en.wikipedia.org/wiki/Golden_Bear",[
                ("2017","https://en.wikipedia.org/wiki/67th_Berlin_International_Film_Festival"),
                ("2016","https://en.wikipedia.org/wiki/66th_Berlin_International_Film_Festival"),
                ("2015","https://en.wikipedia.org/wiki/65th_Berlin_International_Film_Festival"),
                ("2014","https://en.wikipedia.org/wiki/64th_Berlin_International_Film_Festival"),
                ("2013","https://en.wikipedia.org/wiki/63rd_Berlin_International_Film_Festival"),
                ("2012","https://en.wikipedia.org/wiki/62nd_Berlin_International_Film_Festival"),
                ("2011","https://en.wikipedia.org/wiki/61st_Berlin_International_Film_Festival"),
                ("2010","https://en.wikipedia.org/wiki/60th_Berlin_International_Film_Festival"),
                ("2009","https://en.wikipedia.org/wiki/59th_Berlin_International_Film_Festival"),
                ("2008","https://en.wikipedia.org/wiki/58th_Berlin_International_Film_Festival"),
                ("2007","https://en.wikipedia.org/wiki/57th_Berlin_International_Film_Festival"),
                ("2006","https://en.wikipedia.org/wiki/56th_Berlin_International_Film_Festival"),
                ("2005","https://en.wikipedia.org/wiki/55th_Berlin_International_Film_Festival"),
                ("2004","https://en.wikipedia.org/wiki/54th_Berlin_International_Film_Festival"),
                ("2003","https://en.wikipedia.org/wiki/53rd_Berlin_International_Film_Festival"),
                ("2002","https://en.wikipedia.org/wiki/52nd_Berlin_International_Film_Festival"),
                ("2001","https://en.wikipedia.org/wiki/51st_Berlin_International_Film_Festival"),
                ("2000","https://en.wikipedia.org/wiki/50th_Berlin_International_Film_Festival"),
                ("1999","https://en.wikipedia.org/wiki/49th_Berlin_International_Film_Festival"),
                ("1998","https://en.wikipedia.org/wiki/48th_Berlin_International_Film_Festival") ] ),

            ( "https://en.wikipedia.org/wiki/Golden_Lion",[
("2017", "https://en.wikipedia.org/wiki/74th_Venice_International_Film_Festival"),
("2016", "https://en.wikipedia.org/wiki/73rd_Venice_International_Film_Festival"),
("2015", "https://en.wikipedia.org/wiki/72nd_Venice_International_Film_Festival"),
("2014", "https://en.wikipedia.org/wiki/71st_Venice_International_Film_Festival"),
("2013", "https://en.wikipedia.org/wiki/70th_Venice_International_Film_Festival"),
("2012", "https://en.wikipedia.org/wiki/69th_Venice_International_Film_Festival"),
("2011", "https://en.wikipedia.org/wiki/68th_Venice_International_Film_Festival"),
("2010", "https://en.wikipedia.org/wiki/67th_Venice_International_Film_Festival"),
("2009", "https://en.wikipedia.org/wiki/66th_Venice_International_Film_Festival"),
("2008", "https://en.wikipedia.org/wiki/65th_Venice_International_Film_Festival"),
("2007", "https://en.wikipedia.org/wiki/64th_Venice_International_Film_Festival"),
("2006", "https://en.wikipedia.org/wiki/63rd_Venice_International_Film_Festival"),
("2005", "https://en.wikipedia.org/wiki/62nd_Venice_International_Film_Festival"),
("2004", "https://en.wikipedia.org/wiki/61st_Venice_International_Film_Festival"),
("2003", "https://en.wikipedia.org/wiki/60th_Venice_International_Film_Festival"),
("2002", "https://en.wikipedia.org/wiki/59th_Venice_International_Film_Festival"),
("2001", "https://en.wikipedia.org/wiki/58th_Venice_International_Film_Festival"),
("2000", "https://en.wikipedia.org/wiki/57th_Venice_International_Film_Festival"),
("1999", "https://en.wikipedia.org/wiki/56th_Venice_International_Film_Festival"),
("1998", "https://en.wikipedia.org/wiki/55th_Venice_International_Film_Festival"),
("1997", "https://en.wikipedia.org/wiki/54th_Venice_International_Film_Festival"),
("1996", "https://en.wikipedia.org/wiki/53rd_Venice_International_Film_Festival"),
("1995", "https://en.wikipedia.org/wiki/52nd_Venice_International_Film_Festival"),
("1994", "https://en.wikipedia.org/wiki/51st_Venice_International_Film_Festival"),
("1993", "https://en.wikipedia.org/wiki/50th_Venice_International_Film_Festival"),
("1992", "https://en.wikipedia.org/wiki/49th_Venice_International_Film_Festival"),
("1991", "https://en.wikipedia.org/wiki/48th_Venice_International_Film_Festival"),
("1990", "https://en.wikipedia.org/wiki/47th_Venice_International_Film_Festival"),
("1989", "https://en.wikipedia.org/wiki/46th_Venice_International_Film_Festival"),
("1988", "https://en.wikipedia.org/wiki/45th_Venice_International_Film_Festival"),
("1987", "https://en.wikipedia.org/wiki/44th_Venice_International_Film_Festival"),
("1986", "https://en.wikipedia.org/wiki/43rd_Venice_International_Film_Festival"),
("1985", "https://en.wikipedia.org/wiki/42nd_Venice_International_Film_Festival"),
("1984", "https://en.wikipedia.org/wiki/41st_Venice_International_Film_Festival"),
("1983", "https://en.wikipedia.org/wiki/40th_Venice_International_Film_Festival"),
("1982", "https://en.wikipedia.org/wiki/39th_Venice_International_Film_Festival"),
("1981", "https://en.wikipedia.org/wiki/38th_Venice_International_Film_Festival"),
("1980", "https://en.wikipedia.org/wiki/37th_Venice_International_Film_Festival"),
("1968", "https://en.wikipedia.org/wiki/29th_Venice_International_Film_Festival"),
("1967", "https://en.wikipedia.org/wiki/28th_Venice_International_Film_Festival"),
("1966", "https://en.wikipedia.org/wiki/27th_Venice_International_Film_Festival"),
("1965", "https://en.wikipedia.org/wiki/26th_Venice_International_Film_Festival"),
("1964", "https://en.wikipedia.org/wiki/25th_Venice_International_Film_Festival"),
("1963", "https://en.wikipedia.org/wiki/24th_Venice_International_Film_Festival"),
("1962", "https://en.wikipedia.org/wiki/23rd_Venice_International_Film_Festival"),
("1961", "https://en.wikipedia.org/wiki/22nd_Venice_International_Film_Festival"),
("1960", "https://en.wikipedia.org/wiki/21st_Venice_International_Film_Festival"),
("1959", "https://en.wikipedia.org/wiki/20th_Venice_International_Film_Festival"),
("1958", "https://en.wikipedia.org/wiki/19th_Venice_International_Film_Festival"),
("1957", "https://en.wikipedia.org/wiki/18th_Venice_International_Film_Festival"),
("1956", "https://en.wikipedia.org/wiki/17th_Venice_International_Film_Festival"),
("1955", "https://en.wikipedia.org/wiki/16th_Venice_International_Film_Festival"),
("1954", "https://en.wikipedia.org/wiki/15th_Venice_International_Film_Festival"),
("1953", "https://en.wikipedia.org/wiki/14th_Venice_International_Film_Festival"),
("1952", "https://en.wikipedia.org/wiki/13th_Venice_International_Film_Festival"),
("1951", "https://en.wikipedia.org/wiki/12th_Venice_International_Film_Festival"),
("1950", "https://en.wikipedia.org/wiki/11th_Venice_International_Film_Festival"),
("1949", "https://en.wikipedia.org/wiki/10th_Venice_International_Film_Festival"),
("1948", "https://en.wikipedia.org/wiki/9th_Venice_International_Film_Festival"),
("1947", "https://en.wikipedia.org/wiki/8th_Venice_International_Film_Festival")] )

            ]

    films = []

    scraper = FilmFestivalWikiWebScraper()

    for idx,link_set in enumerate(links):
        print("")
        print("Scraping Data from the {0} Film Festival...".format(festivals[idx]))
        print("\t{0}".format(link_set[0]))

        scraped_awards_page_data = scraper.scrape_awards_wiki( festivals[idx], link_set[0] )

        # scraping the screening data
        scraped_screening_page_data = []
        for year_link in link_set[1]:
            print("\t{0}".format(year_link))
            scraped_screening_page_data.extend( scraper.scrape_screened_wiki( festivals[idx], year_link[0], year_link[1]) )

        # merge the data
        merged_data = scraper.merge_award_and_screened_data( scraped_awards_page_data,  scraped_screening_page_data)


        # save it
        films.extend( merged_data )


    # write the scraped data to file
    print("")
    print("Web-scraping Complete.")
    print("")
    print("Writing data to file: film_data.txt")
    print("")
    io = ReadWrite()
    io.write_film_data( "film_data.txt", films )


else:
    print("")
    print("Usage Error")
    print("")
