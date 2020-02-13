# pip3 install selenium
# sudo apt-get install firefox-geckodriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def main():
    image_scraper( "fennec fox" )

def image_scraper( animal_search ):

    # Create our google image search url template 
    search_url = "https://www.google.co.in/search?q={search_query}&source=lnms&tbm=isch"

    # Connect our python script to our firefox browser
    driver = webdriver.Firefox()

    # Change any spaces in the search query into pluses
    image_search = correct_for_query_spaces( animal_search )

    # Have our webdriver connect to our crafted url
    # The url replaces the "search query" with our actual search query
    driver.get( search_url.format( search_query = image_search ))

    # Check that the connection to the website was successful 
    assert "Google" in driver.title
    assert "No results found." not in driver.page_source

    


def correct_for_query_spaces( search_query ):
    temp_query = search_query.split()
    return '+'.join( temp_query )

def retreive_image_urls( search_query ):
    

if __name__ == "__main__":
    main()
