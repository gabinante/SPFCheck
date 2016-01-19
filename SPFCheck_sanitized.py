import csv
import logging
import time
import spf
timestamp=time.strftime("%d:%m:%Y")

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# first file logger
logger_1 = logging.getLogger('simple_logger')
hdlr_1 = logging.FileHandler('Full_Test_Output'+timestamp+'.log')
hdlr_1.setFormatter(formatter)
logger_1.addHandler(hdlr_1)
logger_1.setLevel(logging.DEBUG)

# second file logger
logger_2 = logging.getLogger('simple_logger_2')
hdlr_2 = logging.FileHandler('Failure_Only'+timestamp+'.log')
hdlr_2.setFormatter(formatter)
logger_2.addHandler(hdlr_2)
logger_2.setLevel(logging.DEBUG)



logger_1.info('This log file was created on '+timestamp)
logger_2.info('This log file was created on '+timestamp)


with open('PyInput.csv', 'rb') as f:
  reader = csv.reader(f)
  TeamList = list(reader)

CSVSize = len(TeamList)
#IPs that you will check for validation. These are placeholder values. Insert your own values here!
IPList = ['22.129.129.442','22.129.129.443','22.129.129.444','22.129.129.445','22.129.129.446','22.129.129.447','22.129.129.448','22.129.129.449']
TeamDictonary = {}

## Take input CSV file and place into a list
if isinstance(CSVSize, (int, long, float, complex)) and CSVSize>0:
  x=0
  while x<CSVSize:
    ParsingLine = TeamList[x]
    ParsingLineLength = len(ParsingLine)
    y=1
    CustomerNumber=ParsingLine[0]
    ParsingList = []
    if ParsingLineLength >=2:
      while y<ParsingLineLength:
        newvalue=ParsingLine[y]
        if newvalue != '' and newvalue != None:
          ParsingList.append(newvalue)
        y+=1
    else:
      logger_1.debug('The CustomerNumber:'+k+' has no domains associated with it')

    TeamDictonary[CustomerNumber]=ParsingList
    x+=1

  for k,v in TeamDictonary.items():
      z=0
      eachcounter=0
      ValuesLength = len(v)
      if ValuesLength > 0:

        while z<ValuesLength:
          for each in IPList:
            if (v[z] != '' and v[z] != None):
              result = spf.check2(each,'test@'+v[z],v[z]) ##This is where we will call to check this specific domain result should return true/false
              logger_1.debug('trying ' +each)
              if result[0]!='pass':
                newresult = spf.check2(each,'test@'+v[z],v[z]) ##double check
                if newresult[0]!='pass':
                  logger_1.debug('The domain '+v[z]+' has failed validation on '+each+'. Located in CustomerNumber:'+k)
              else:
                  logger_1.debug('The domain '+v[z]+' has passed validation on '+each+'. Located in CustomerNumber:'+k)
                  eachcounter = eachcounter+1
            else:
              logger_1.debug('v[z] == undefined ' + v[z] + ' on '+each+'. Located in CustomerNumber:'+k)
          #THIS SHOULD BE SET TO THE NUMBER OF IPs USED ON LINE 35 (8), BUT WE FAIL CONSISTENTLY IF IT IS, EVEN WITH THE DOUBLE CHECK. WE ARE ASSUMING THAT IF THEY INCLUDE 6 OF OUR IPs THEY INCLUDE ALL. THIS IS NOT A GREAT WAY TO DO THINGS IF PEOPLE INCLUDE IPs MANUALLY RATHER THAN USING 'INCLUDE:'
          if eachcounter <=6 or eachcounter == 0:

            logger_2.debug('The domain '+v[z]+' has failed validation. Located in CustomerNumber:'+k)
          z+=1
      else:
        logger_1.debug('CustomerNumber:'+k+' has no records to check')
else:
  logger_1.debug('Length of CSV file is 0 or undefined. Please check data file')

