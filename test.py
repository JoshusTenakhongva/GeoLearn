import mysql.connector
from PIL import Image
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon

def main():

	ROWS_TO_ACCESS = 100
	getting_info = True

	mydb = mysql.connector.connect(
	
		host="ecolocation.c09lpapromur.us-east-2.rds.amazonaws.com",
		user="TeamEcolocation",
		password="EcolocationData",
		port=3306,
		database="ecolocation_data"
		)

	mycursor = mydb.cursor( buffered=True )
	
	# Grab the descriptors of the mammals information from the database
	descriptors = []
	mycursor.execute( "SHOW FIELDS FROM iucn" )
	for x in mycursor: 
		descriptors.append( x[ 0 ] )
		
	animal_boundaries = []
	animal_info = []
	
	mycursor.execute( "SELECT AsText(boundaries) FROM iucn" )
	print( "starting" )
	for animal in mycursor:
		animal_boundaries.append( animal )
	print( "done" )
	
	mycursor.execute( "SELECT * FROM iucn" )
	print( "starting" )
	for animal in mycursor:
		animal_info.append( animal )
	print( "done" )
	
	animals_within_boundaries = []
	
	while getting_info:
		response = input( "Enter longitude and latitude (comma separated) or \"exit\" to exit: " )
		if response.lower() == "exit":
			getting_info = False
		else:
			response = response.split( "," )
			latitude = float( response[ 0 ] )
			longitude = float( response[ 1 ] )
			
		for index in range( 0, len( animal_boundaries ) ):
			if checkCoordinates_in_animalInfo(latitude, longitude, animal_boundaries[ index ]):
				animals_within_boundaries.append( animal_info[ index ] )
				
		if len( animals_within_boundaries ) == 0:
			print( "There were no mammals in that area" )
		else:
			display_mammal_information( animals_within_boundaries, descriptors )
			#try:
			
			#except: 	
	
# end main 	
def checkCoordinates_in_animalInfo( latitude, longitude, animal_boundary ):
	
	# create a point object from the latitude and longitude
	point = Point( latitude, longitude )
	
	# return if it's within the animal polygon
	return point.within( animal_boundary )

def display_mammal_information( listOfMammals, descriptors ):

	for x in listOfMammals: 
		for index in range( 0, len( x )):
			if index != 17:	
				print( " - " + descriptors[ index ], end= ": " )
				print( x[ index ] )
		
		print( "\n====================\n" )
		
# end display_mammal_information
		
def create_polygon( currentShape ):

	listOf_shapesPoints = []
	# Separate our list of coordinates into the shell and the holes
	shapeList = currentShape.strip( "POLYGON((" ).split( ")" )
	
	# Delete all of the empty elements in the list 
	listIndex = 0
	for	i in range( 0, len( shapeList ) ):
	
		# If an element in the list is nothing, delete it
		if len( shapeList[ listIndex ] ) == 0:
			shapeList.pop( listIndex )
			
		# If the element is valid, separate it into a list of coordinate pairs
		else:		
			shapeList[ listIndex ] = shapeList[ listIndex ].strip( ",((" )
			listOf_shapesPoints.append( shapeList[ listIndex ].split( "," ) )
			listIndex += 1
			
	# Convert the list of coordinate pair strings into floats
	# Loop through each shape in the list 
	for shape in listOf_shapesPoints:
	
		# Loop thorugh the points in each shape
		for index in range( 0, len( shape ) ):
			
			# separate the x and y coordinates
			tempCoors = shape[ index ].split()
			
			# Convert the coordaintes to floats 
			latitude = float( tempCoors[ 0 ] )
			longitude = float( tempCoors[ 1 ] )
			
			# Save the now converted coordinates
			shape[ index ] = ( latitude, longitude )
	
	# Save the actual shape file, leaving the holes in the listOf_shapesPoints list
	linearRing = listOf_shapesPoints.pop( 0 )
	
	try:
	# Create our polygon 
		if len( listOf_shapesPoints ) == 0:
			polygon = Polygon( linearRing )
		else:
			polygon = Polygon( linearRing, listOf_shapesPoints )
				
		# return our polygon
		return polygon
		
	except ValueError:
		return Polygon( [(0,0), (0,0), (0,0 )] )
		
def create_multi_polygon( currentShape ):
	
	# Get rid of the cruft from the database string 
	shapeString = currentShape.strip( "MULTIPOLYGON(" ).strip( ")" )
	listOfPolygons = shapeString.split( "))" )
		
	for index in range( 0, len( listOfPolygons ) ):
		listOfPolygons[ index ] = create_polygon( listOfPolygons[ index ] )
			
	multi_polygon = MultiPolygon( listOfPolygons )
	
	return multi_polygon

def create_shape( currentShape ):
	if currentShape[ 0 ] is not None: 
		if "MULTIPOLYGON" in currentShape[ 0 ]:
			print( "	multi" )
			#return( " " )
			return create_multi_polygon( currentShape[ 0 ] ).bounds
			
			
		elif "POLYGON" in currentShape[ 0 ]:
			
			print( " polygon" )
			#return( " " )
			return create_polygon( currentShape[ 0 ] ).bounds
		
	
main()

#
