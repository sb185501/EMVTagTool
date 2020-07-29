# Program to read Simple Tag data from a text file. 

# Structure (dict) to hold the constructed data of a Simple Tag.
simpleTags = {}

class SimpleTag():
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def writeTagData(self, tag, name, desc):
        simpleTags[tag] = SimpleTag( name, desc )

file1 = open("SimpleTags.txt","r+") 

# Read all the lines in the file and fillup the structure simpleTags to use it for decoding the tags.
lines = file1.readlines()
for line in lines:
    if ( ( line.isspace() == False ) and ( line.find('*') == -1 ) and ( line.find('#') == -1 ) and ( line.find('/') == -1 )) :
        lineList = line.split(':')

        tagID = lineList[0].strip('\n\t ')
        tagName = lineList[1].strip('\n\t ')
        tagDesc = ''
        if len( lineList ) > 2:
            tagDesc = lineList[2].strip('\n\t ')

        st = SimpleTag('','')
        st.writeTagData(tagID, tagName, tagDesc)

file1.seek(0) 
file1.close() # Close the file after process completes.
