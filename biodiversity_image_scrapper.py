from selenium import webdriver
from selenium.webdriver.common.keys import Keys

search_url = https://www.google.co.in/search?q="{search_query}"&source=lnms&tbm=isch 

driver = webdriver.Firefox()

image_search = fennec fox

driver.get( search_url.format( search_query = image_serach ))

assert "Google" in driver.title

elem = driver.find_element_by_name( "q" )
elem.clear()
elem.send_keys( "pycon" )
elem.send_keys( Keys.RETURN )

assert "No results found." not in driver.page_source


