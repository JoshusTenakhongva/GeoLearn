import mysql.connector
from PIL import Image
from shapely.geometry import Polygon

def main():

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
	#mycursor.execute( "SELECT * FROM iucn 100" )
	#for animal in mycursor:
	#	mammal_list.append( get_animal_information( animal )
		
	# Get the shape files for each mammal 
	#mammal_locations = []
	mycursor.execute( "SELECT AsText(boundaries) FROM iucn LIMIT 7" )
	for animal in mycursor:
	#	mammal_locations.append( create_polygon( animal ) )
		print( create_shape( animal ) )
	
	# display the information of the animals that are within the boundaries
	#mycursor.execute( "SELECT * FROM iucn LIMIT 100" )
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

	# Separate our list of coordinates into the shell and the holes
	shapeList = currentShape.strip( "POLYGON((" ).split( ")" )
	print( len( shapeList )) 
	
	# Delete all of the empty elements in the list 
	listIndex = 0
	for	i in range( 0, len( shapeList ) ):
	
		print( listIndex )
		if len( shapeList[ listIndex ] ) == 0:
			shapeList.pop( listIndex )
			print( "deleted" )
		else:		
			listIndex += 1
			
	
			
	#print( len( shapeList ) )
		
	# shapeString = currentShape[ 0 ].strip( "POLYGON((" ).strip( "))" )
		
	# Split the values into x and y coordinate pairs
		#listOfPointTuples = shapeString.split( "," )
		
	#if( polygonPointCount <= 100 ):
			
	#	for x in listOfPointTuples:
	#		print( x.split( "," ) )
					
	#	print("\n======================\n" )
		
	# Loop through each pair and create a float tuple
	#for i in range( 0, len( listOfPointTuples ) ):
		
		# Convert our string coordinates to floats
	#	tempList = listOfPointTuples[ i ].split()
	#	xCoor = float( tempList[ 0 ] )
	#	yCoor = float( tempList[ 1 ] )
			
		# Put the floats into tuples
	#	listOfPointTuples[ i ] = ( xCoor, yCoor )
			
	return "	polygon"
	
def create_multi_polygon( currentShape ):
	
	# Get rid of the cruft from the database string 
	shapeString = currentShape.strip( "MULTIPOLYGON(" ).strip( ")" )
	sectionCount = len( shapeString.split( "))" ) )
	polygonPointCount = len( shapeString.split( "," ) )
	
	#if polygonPointCount <= 100:
	#listOfPolygons = shapeString.split( "))" )
	
		
	print()
	for i in shapeString.split( "))" ):
		print( i )
		print()
			
	print( sectionCount )
	
	return "	multi" 
	
	#if polygonPointCount <= 100:
	#	listOfPointTuples = shapeString.split( ")" )

def create_shape( currentShape ):
	if "MULTIPOLYGON" in currentShape[ 0 ]:
		return create_multi_polygon( currentShape[ 0 ] )
		
	elif "POLYGON" in currentShape[ 0 ]:
		return "Sure" #create_polygon( currentShape[ 0 ] )
		
	
main()

#
