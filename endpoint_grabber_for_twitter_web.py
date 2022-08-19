# A script to parse through twitter javascript source files to find graphQL endpoints.
# Warning: Twitter will keep chnaging several constants and formats around, need to update as per changes
# Run on terminal : python3 endpoint_grabber_for_twitter_web.py

import requests,re,json
from datetime import datetime

now = datetime.now()
date_today = now.strftime("%d-%m-%Y_%H-%M-%S")
print("\n###########################################################################################")
print("######################### Twitter GraphQL Endpoint Grabber  ###############################")
print("###########################################################################################\n")
print("\nIterating through list of source files:\n")

# Baseurl where static twitter source files are stored
baseUrl = 'https://abs.twimg.com/responsive-web/client-web/'
# baseUrl = 'https://abs.twimg.com/responsive-web/client-web-legacy/'
basetweetdeckUrl = 'https://abs.twimg.com/responsive-web/client-web/'

fileName = []
graphqlList =[]
graphqllistwithfileName = []
# These headers generate different source files vs when no headers are sent - Probably Chrome vs other browsers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
# Sending the request to get all source file names from home page
getSourceReq = requests.get("https://www.twitter.com/?prefetchTimestamp=", headers=headers, allow_redirects=True).text
# Main file key is not along with the rest
getMainJsFileKeyDetails = re.findall("https://abs.twimg.com/responsive-web/client-web/main.(.*)8.js",getSourceReq)

# Regex to find and isolate list of source file name and cleaning it from the recieved string format into python acceptable dictionary format
firstRegex = re.findall(".u=e=>e+(.*)8.js",getSourceReq)
regexAgain = re.findall("{(.*)}",firstRegex[0])
acceptable = regexAgain[0].replace(":", ",").replace('"', "")
listRes = list(acceptable.split(","))

# Converting list into dictionary for easier iteration
res_dct = {listRes[i]: listRes[i + 1] for i in range(0, len(listRes), 2)}
res_dct.update({"main":str(getMainJsFileKeyDetails[0])})
#This will change as per twitter
res_dct.update({"bundle.Delegate":"d4714f1"})


for key,value in res_dct.items():
    print(key)
    #Twitter appends a random numerical to the end of the file name, the current number used is '8', keep checking for what the value is currently
    fileName.append(key+"."+value+"8"+".js")
    sourcecodeUrl = baseUrl + key+"."+value+"8"+".js"
    # print(sourcecodeUrl)

    #TODO :Currently not checking for status-codes, could lead to data not being fetched due to 404 or rate-limiting
    r = requests.get(sourcecodeUrl, allow_redirects=False).text
    # print(r)
    output = re.findall('params:(.*?)operationKind:', r)
    output_1 = re.findall('e.exports={(.*?)operationType:', r)
    # print(output)

    # if output != [] or output_1 != []:
    graphqllistwithfileName.append(key)
    if output != []:
        graphqllistwithfileName.append(output)
    if output_1 != []:
        graphqllistwithfileName.append(output_1)

    graphqllistwithfileName.append("\n")


with open("twitter_graphql_endpoints_"+date_today+".txt", "w") as outfile:
    outfile.write("\n".join(str(item) for item in graphqllistwithfileName))

print("\n#########################################################\n\nOutput File :"+ " twitter_graphql_endpoints_"+date_today+".txt")
print("\n#########################################################\n")
