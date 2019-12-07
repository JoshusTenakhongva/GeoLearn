import mysql.connector
from PIL import Image
from shapely.geometry import Polygon

def main():

	ROWS_TO_ACCESS = 10

	mydb = mysql.connector.connect(
	
		host="ecolocation.c09lpapromur.us-east-2.rds.amazonaws.com",
		user="TeamEcolocation",
		password="EcolocationData",
		port=3306,
		database="ecolocation_data"
		)

	mycursor = mydb.cursor()
	
	# Grab the descriptors of the mammals information from the database
	descriptors = []
	mycursor.execute( "SHOW FIELDS FROM iucn" )
	for x in mycursor: 
		descriptors.append( x[ 0 ] )
		
	# Get all of the mammals from the database into a list 
	#mammal_list = []
	#mycursor.execute( "SELECT * FROM iucn %d" %( ROWS_TO_ACCESS ) )
	#for animal in mycursor:
	#	mammal_list.append( get_animal_information( animal )
		
	# Get the shape files for each mammal 
	#mammal_locations = []
	mycursor.execute( "SELECT AsText(boundaries) FROM iucn LIMIT %d" % ( ROWS_TO_ACCESS ) )
	index = 0
	for animal in mycursor:
		
		#mammal_locations.append( create_shape( animal ) )
		#index += 1
		#print( index, end=" " )
	
		print( create_shape( animal ) )
	
	#	print( "\n\n" )	
	
	# display the information of the animals that are within the boundaries
	#mycursor.execute( "SELECT * FROM iucn LIMIT %d" % ( ROWS_TO_ACCESS ) )
	#display_mammal_information( mycursor, polygons, descriptors )
# end main 	
	
	
def get_animal_information( animalList ):
	return true
	


def display_mammal_information( listOfMammals, polygons, descriptors ):

	polygonIndex = 0
	
	for x in listOfMammals: 
		for index in range( 0, len( x )):
			print( " - " + descriptors[ index ], end= ": " )
			if index != 17:	
				print( x[ index ] )
			else:
				print( polygons[ polygonIndex ].bounds )
		
		polygonIndex += 1
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
			
	print( "length of polygon sections", end= " " )
	print( len( shapeList )) 
			
	# Convert the list of coordinate pair strings into floats
	# Loop through each shape in the list 
	for shape in listOf_shapesPoints:
	
		# Loop thorugh the points in each shape
		for index in range( 0, len( shape ) ):
			
			# separate the x and y coordinates
			tempCoors = shape[ index ].split()
			
			# Convert the coordaintes to floats 
			xCoor = float( tempCoors[ 0 ] )
			yCoor = float( tempCoors[ 1 ] )
			
			# Save the now converted coordinates
			shape[ index ] = ( xCoor, yCoor )
	
	# Save the actual shape file, leaving the holes in the listOf_shapesPoints list
	linearRing = listOf_shapesPoints.pop( 0 )
			
	# Create our polygon 
	if len( listOf_shapesPoints ) == 0:
		polygon = Polygon( linearRing )
	else:
		polygon = Polygon( linearRing, listOf_shapesPoints )
			
	# return our polygon
	return polygon.bounds
	
def create_multi_polygon( currentShape ):
	
	# Get rid of the cruft from the database string 
	shapeString = currentShape.strip( "MULTIPOLYGON(" ).strip( ")" )
	listOfPolygons = shapeString.split( "))" )
		
	for index in range( 0, len( listOfPolygons) ):
		#print( listOfPolygons[ index ] )
		listOfPolygons = create_polygon( listOfPolygons[ index ] )
			
	#multi_polygon = MultiPolygon( listOfPolygons )
	print( "multipolygon polygon count" )
	print( len( listOfPolygons ) )
	
	return "		multi" 

def create_shape( currentShape ):
	if "MULTIPOLYGON" in currentShape[ 0 ]:
		print( "	multi" )
		#return( " " )
		return create_multi_polygon( currentShape[ 0 ] )
		
		
	elif "POLYGON" in currentShape[ 0 ]:
		
		print( " polygon" )
		#return( " " )
		return create_polygon( currentShape[ 0 ] )
		
	
main()

#
