# pip3 install selenium
# sudo apt-get install firefox-geckodriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# pip3 install Pillow
from PIL import Image

import io
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    while True:
        print( "type animal name: " )
        image_scraper( input() )

def image_scraper( animal_search ):

    ''' Connect to google images webpage ''' 
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

    ''' Retreive the URLs for the images we're searching for '''
    retrieve_image_urls( animal_search, driver )


def correct_for_query_spaces( search_query ):
    temp_query = search_query.split()
    return '+'.join( temp_query )

def retrieve_image_urls( search_query, webdriver ):

    # Variable that holds the number of images to fetch 
    number_of_images_to_fetch = 1
    index = 0
    image_urls = []

    scroll_down( webdriver )

    image_elements = webdriver.find_elements_by_class_name( 'rg_i' )

    if not os.path.exists( BASE_DIR + "/biodiversity/" + search_query ):
        os.mkdir( BASE_DIR + "/biodiversity/" + search_query )

    ''' 
    Loop through the image elements gathered and translate them to 
    URLs and then to actual images 
    '''

    temp = image_elements[ 0 ].get_attribute( 'data-iurl' )
    temp_file = io.BytesIO( requests.get( temp ).content )
    temp_image = Image.open( temp_file.convert( 'RGB' ) )
    print( "length " +  str( len( image_elements )) )
    
    for index in range( number_of_images_to_fetch ):
        print( "index" + str( index ) )
        image_url = image_elements[ index ].get_attribute( 'data-iurl' )
        image_file = io.BytesIO( requests.get( image_url ).content )
        image = Image.open( image_file.convert( 'RGB' ))

        image_name = '/image' + index + '.jpg'
        image_path = BASE_DIR + "/biodiversity/" + search_query + image_name
        image.save( image_path, 'JPEG', quality=85 )
        
    webdriver.close()


'''
Method that scrolls down the webpage to load more images
'''
def scroll_down( webdriver ):
    value = 0
    for i in range( 1 ):
        webdriver.execute_script( "scrollBy( 0, " + str(value) + ");" )
        value += 500
        time.sleep( 1 )

'''

'''
#def download_images( elements, index ):
    

#def upload_image_directory(): 


if __name__ == "__main__":
    main()
