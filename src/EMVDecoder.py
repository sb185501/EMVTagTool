import re
import SimpleTagParser
from SimpleTagParser import simpleTags
import BinaryTagParser
from BinaryTagParser import binaryTags

def decodeSimpleTags( tag, value ):    
    if tag not in simpleTags:
        return [value, '', '%s tag is not valid or not supported' %tag]

    tagData = simpleTags[tag]

    setValues = [value, tagData.name]

    if tagData.desc != '':
        setValues.append( tagData.desc )

    return setValues
    
def decodeBinaryTags( tag, value ):
    
    tagData = binaryTags[tag]
    errors = isValidValue(tag, value)
    if len(errors) != 0:
        return [value, tagData.name, errors]

    setBits = []
    
    intValue = int(value, 16)
    for bit in tagData.bitList:
        if intValue & bit[0] == bit[0]:
            setBits.append( ('%0' + str(tagData.fieldLength) + 'X' + ' ' + bit[1] ) % bit[0] )
        
    return [value, tagData.name, setBits]

def decodeTag9F34(tag, value):

    tagData = binaryTags[tag]

    errors = isValidValue( tag, value )
    if len(errors) != 0:
        return [value, tagData.name, errors]
    

    tag9F34Byte1 = {
        '5E': '5E Signature (paper)',
        '44': '44 Enciphered PIN verification performed by ICC',
        '42': '42 Enciphered PIN verified online',
        '1F': '1F No CVM required',
        '05': '05 Encrypted PIN by ICC + signature',
        '04': '04 Encrypted PIN by ICC',
        '03': '03 Plain PIN by ICC + signature',
        '02': '02 Encrypted PIN online',
        '01': '01 Plain PIN by ICC',
        '00': '00 Fail'
    }   

    tag9F34Byte2 = {
        '09': '09 If transaction in application currency and >= Y',
        '08': '08 If transaction in application currency and < Y',
        '07': '07 If transaction in application currency and >= X',
        '06': '06 If transaction in application currency and < X',
        '05': '05 If purchase + cash',
        '04': '04 If manual cash',
        '03': '03 If terminal supports CVM',
        '02': '02 If not (unattended cash, manual cash, purchase + cash)',
        '01': '01 If unattended cash'
    }

    tag9F34Byte3 = {
        '02': '02 Successful',
        '01': '01 Failed'
    }
    setValues = []
    
    setValues.append( tag9F34Byte1.get( value[0:2], value[0:2] + ' Unknown') )
    setValues.append( tag9F34Byte2.get( value[2:4], value[2:4] + ' Unknown') )
    setValues.append( tag9F34Byte3.get( value[4:6], value[4:6] + ' Unknown') )

    return [value, tagData.name, setValues]

def decodeTags( inputList ):
    superSetBits = {}
    for tagValue in inputList:
        tag = tagValue[0]
        value = tagValue[1]
        tag = tag.upper()

        if tag == '9F34':
            superSetBits[tag] = decodeTag9F34( tag, value )
            continue

        if tag not in binaryTags:
            tagInfoStr = decodeSimpleTags( tag, value )
            superSetBits[tag] = tagInfoStr
            continue
        
        tagInfoList = decodeBinaryTags( tag, value )
        superSetBits[tag] = tagInfoList
        continue

    return superSetBits
    
    
def isValidValue(tag, value):
    tagData = binaryTags[tag]
    if tagData != None and len(value) != tagData.fieldLength:
        return '%s must be exactly %d characters long' % (tag, tagData.fieldLength)
    if not re.match('^[0-9a-fA-F]+$', value):
        return '%s must contain only hexadecimal characters. ie 0-9 and A-F.' % tag
    return ()
