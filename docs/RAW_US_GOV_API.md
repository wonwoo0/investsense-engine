#SAM.gov Get Opportunities Public API #

Overview
Get Opportunities API provides all the published opportunity details based on the request parameters. This API requires pagination, and the response will be provided to users synchronously.

This API only provides the latest active version of the opportunity. To view all version of the opportunity, please visit Data Services Section of SAM.gov. All active notices in SAM.gov are updated daily and all archived notices are updated on a weekly basis.

Active Opportunities

Archived Opportunities

Getting Started
Get Opportunities API can be accessed from Production or Alpha via the following environments:

Version Control - v2
Production:
https://api.sam.gov/opportunities/v2/search
Alpha:
https://api-alpha.sam.gov/opportunities/v2/search
Authentication and API Keys
User of this public API must provide an API key to use this Opportunities public API. Request per day are limited based on the federal or non-federal or general roles. Note: User can request a public API Key in the Account Details page on SAM.gov (if testing in production) Else on alpha.sam.gov (if testing in prodlike).

User Account API Key Creation
Registered user can request for a public API on ‘Account Details’ page. This page can be accessed on Account Details page on SAM.gov
User must enter account password on ‘Account Details’ page to view the API Key information. If an incorrect password is entered, an error will be returned.
After the API Key is generated on ‘Account Details’ page, the API Key can be viewed on the Account Details page immediately. The API Key is visible until user navigates to a different page.
If an error is encountered during the API Key generation/retrieval, then user will receive an error message and must try again.
Get Opportunities Request Parameters
Users can search by any of the below request parameters with Date field as mandatory.

Request Parameters that API accepts	Description	Required	Data Type	Applicable Versions
api_key	Public Key of users	Yes	String	v2
ptype	Procurement Type. Below are the available Procurement Types:
u= Justification (J&A)
p = Pre solicitation
a = Award Notice
r = Sources Sought
s = Special Notice
o = Solicitation
g = Sale of Surplus Property
k = Combined Synopsis/Solicitation
i = Intent to Bundle Requirements (DoD-Funded)

Note: Below services are now retired:
f = Foreign Government Standard
l = Fair Opportunity / Limited Sources

Use Justification (u) instead of fair Opportunity	No	String	v2
solnum	Solicitation Number	No	String	v2
noticeid	Notice ID	No	String	v2
title	Title	No	String	v2
postedFrom	Posted date From
Format must be MM/dd/yyyy
Note: Date range between Posted Date From and To is 1 year	Yes	String	v2
postedTo	Posted date To Format must be MM/dd/yyyy
Note: Date range between Posted Date From and To is 1 year	Yes	String	v2
deptname	Department Name (L1)	No	String	v2 - Deprecated
subtier	Agency Name (L2)	No	String	v2 - Deprecated
state	Place of Performance (State)	No	String	v2
status (Coming Soon)	Status of the opportunity
Accepts following: active, inactive, archived, cancelled, deleted	No	String	v2
zip	Place of Performance (Zip code)	No	String	v2
organizationCode	Code of associated organization	No	string	v2
organizationName	Name of associated organization. This Request Parameter can be used to filter the dataset by Department Name or Subtier Name
Note: General Search can be performed	No	String	v2
typeOfSetAside	Refer Set-Aside Value Section	No	String	v2
typeOfSetAsideDescription	Set Aside code Description. See above descriptions mentioned against each of the Set Aside Code	No	String	v2
ncode	NAICS Code. This code is maximum of 6 digits	No	String	v2
ccode	Classification Code	No	String	v2
rdlfrom	Response Deadline date. Format must be MM/dd/yyyy
Note: If response date From & To is provided, then the date range is 1 year	No	String	v2
rdlto	Response Deadline date. Format must be MM/dd/yyyy
Note: If response date From & To is provided, then the date range is 1 year	No	String	v2
limit	Total number of records to be retrieved per page. This field must be a number
Max Value = 1000. Default limit value is 1.	No	Int	v2
offset	Indicates the page index. Default offset starts with 0	No	Int	v2
Get Opportunities Response Parameters
Based on the request parameters, API provides below response parameters.

Request Parameters that API accepts	Description	Data Type	Applicable Versions
totalRecords	Total number of records for the search	Number	v2
limit	Limit entered by a user while making the request i.e. total number of records that user wished to retrieve per page	Number	v2
offset	Page index specified by a user. Default offset starts with 0 if user does not provide any offset in the request	Number	v2
title	Opportunity Title	String	v2
solicitationNumber	Solicitation Number	String	v2
fullParentPathName	Names of all organizations notice is associated with	String	v2
fullParentPathCode	Codes of all organizations notice is associated with	String	v2
department	Department (L1)	String	v2 - Deprecated
subtier	Sub-Tier (L2)	String	v2 - Deprecated
office	Office (L3)	String	v2 - Deprecated
postedDate	Opportunity Posted Date
YYYY-MM-DD HH:MM:SS	String	v2
type	Opportunity current type	String	v2
baseType	Opportunity original type	String	v2
archiveType	Archive Type	String	v2
archiveDate	Archived Date	String	v2
setAside	Set Aside Description	String	v2
setAsideCode	Set Aside Code	String	v2
reponseDeadLine	Response Deadline Date	String	v2
naicsCode	NAICS Code. This code is maximum of 6 digits	String	v2
classificationCode	Classification Code	String	v2
active	If Active = Yes, then the opportunity is active, if No, then opportunity is Archived	String	v2
data.award	Award Information (If Available):
Award amount
Awardee
Award date
Award Number	JSON Object	v2
data.award.number	Award Number	String	v2
data.award.amount	Award Amount	Number	v2
data.award.date	Award Date	Date and Time	v2
data.award.awardee	Name
Location
ueiSAM	JSON Object	v2
data.award.awardee.name	Awardee Name	String	v2
data.award.awardee.ueiSAM	Unique Entity Identifier SAM - Allow 12 digit value, alphanumeric
Example: ueiSAM=025114695AST	String	v2
data.award.awardee.location.
streetAddress	Awardee Street Address 1	String	v2
data.award.awardee.location.
streetAddress2	Awardee Street Address 2	String	v2
data.award.awardee.location.
city	Awardee City	JSON Object	v2
data.award.awardee.location.
city.code	Awardee City Code	String	v2
data.award.awardee.location.
city.name	Awardee City Name	String	v2
data.award.awardee.location.
state	Awardee State	JSON Object	v2
data.award.awardee.location.
state.code	Awardee State Code	String	v2
data.award.awardee.location.
state.name	Awardee State Name	String	v2
data.award.awardee.location.
country	Awardee Country	JSON Object	v2
data.award.awardee.location.
country.code	Awardee Country Code	String	v2
data.award.awardee.location.
country.name	Awardee Country Name	String	v2
data.award.awardee.location.
zip	Awardee Zip	String	v2
pointofContact	Point of Contact Information. It can have below fields if available:
Fax
Type
Email
Phone
Title
Full name	JSON Array	 
data.pointOfContact.type	Point of Contact Type	String	v2
data.pointOfContact.title	Point of Contact Title	String	v2
data.pointOfContact.fullname	Point of Contact Full Name	String	v2
data.pointOfContact.email	Point of Contact Email	String	v2
data.pointOfContact.phone	Point of Contact Phone	String	v2
data.pointOfContact.fax	Point of Contact Fax	String	v2
description	A link to an opportunity description.
Note: To download the description, user should append the public API Key. If no description is available then, user is shown an error message “ Description not found”	String	v2
data.pointOfContact.additionalInfo	Additional Information
Note: This field will only show if additional information is given	JSON Array	v2
data.pointOfContact.additionalInfo.content	Content of Additional Information
Note: This field will only show if a text is provided for additional information	String	v2
organizationType	Type of an organization – department/sub-tier/office	String	v2
officeAddress	Office Address Information. It can have below fields if available:
City
State
Zip	String	v2
data.officeAddress.city	Office Address City	String	v2
data.officeAddress.state	Office Address State	String	v2
data.officeAddress.zip	Office Address Zip	String	v2
placeOfPerformance	Place of performance information. It can have below fields if available: Street
City
State
Zip	JSON Object	v2
data.placeOfPerformance.streetAddress	Pop Address	String	v2
data.placeOfPerformance.streetAddress2	Pop Address2	String	v2
data.placeOfPerformance.city	JSON Object	Pop City	v2
data.placeOfPerformance.city.code	Pop City code	String	v2
data.placeOfPerformance.city.name	Pop City name	String	v2
data.placeOfPerformance.city.state	JSON Object	Pop City state	v2
data.placeOfPerformance.state.code	Pop city state code	String	v2
data.placeOfPerformance.state.name	Pop city state name	String	v2
data.placeOfPerformance.country	JSON Object	Pop Country	v2
data.placeOfPerformance.country.code	Pop Country Code	String	v2
data.placeOfPerformance.country.name	Pop Country name	String	v2
data.placeOfPerformance.zip	Pop Country zip	String	v2
additionalInfoLink	Any additional info link if available for the opportunity	String	v2
uiLink	Direct UI link to the opportunity. To view the opportunity on UI, user must have either a contracting officer or a Contracting Specialist role. If user hits the link without logging in, user is directed to 404 not found page	String	v2
links	Every record in a response has this links array consisting of:
rel: self
href: link to the specific opportunity itself. User should provide an API key to access the opportunity directly

Also, every response has a master links array consisting of:
rel: self
href: link to the actual request. User should provide an API key to access the request	Array	v2
resourceLinks	Direct URL to download attachments in the opportunity	Array of Strings	v2
Set-Aside Values
Several methods pertaining to submitting Contract Opportunities involve the Set-Aside Type field. Use the Set-Aside codes to submit notices.

Only one Set-Aside value is accepted in the field at this time

Refer below table for valid Set-Aside values:

Code	SetAside Values
SBA	Total Small Business Set-Aside (FAR 19.5)
SBP	Partial Small Business Set-Aside (FAR 19.5)
8A	8(a) Set-Aside (FAR 19.8)
8AN	8(a) Sole Source (FAR 19.8)
HZC	Historically Underutilized Business (HUBZone) Set-Aside (FAR 19.13)
HZS	Historically Underutilized Business (HUBZone) Sole Source (FAR 19.13)
SDVOSBC	Service-Disabled Veteran-Owned Small Business (SDVOSB) Set-Aside (FAR 19.14)
SDVOSBS	Service-Disabled Veteran-Owned Small Business (SDVOSB) Sole Source (FAR 19.14)
WOSB	Women-Owned Small Business (WOSB) Program Set-Aside (FAR 19.15)
WOSBSS	Women-Owned Small Business (WOSB) Program Sole Source (FAR 19.15)
EDWOSB	Economically Disadvantaged WOSB (EDWOSB) Program Set-Aside (FAR 19.15)
EDWOSBSS	Economically Disadvantaged WOSB (EDWOSB) Program Sole Source (FAR 19.15)
LAS	Local Area Set-Aside (FAR 26.2)
IEE	Indian Economic Enterprise (IEE) Set-Aside (specific to Department of Interior)
ISBEE	Indian Small Business Economic Enterprise (ISBEE) Set-Aside (specific to Department of Interior)
BICiv	Buy Indian Set-Aside (specific to Department of Health and Human Services, Indian Health Services)
VSA	Veteran-Owned Small Business Set-Aside (specific to Department of Veterans Affairs)
VSS	Veteran-Owned Small Business Sole source (specific to Department of Veterans Affairs)
Examples
Example 1: Search by award type
Request URL
Response (JSON Output) v2
Example 2: Updated v2 Endpoint with FH Information
Request URL
Response (JSON Output)
OpenAPI Specification File
You can view the full details of this API in the OpenAPI Specification file available here: OpenAPI File

Get Opportunities Public API v2
HTTP Response Codes
200 - Success

404 – No Data found

400 – Bad Request

500 – Internal Server Error

Error Messages
Scenario	Error Messages
For limit, user provides range beyond 1000.	Limit valid range is 0-1000. Please provide valid input.
For limit or offset, user inputs characters/special characters.	limit/offset must be a positive number.
For postedFrom, postedTo, rdlfrom, rdlto user enters an invalid date format.	Invalid Date Entered. Expected date format is MM/dd/yyyy
User does not provide postedFrom and postedTo values.	PostedFrom and PostedTo are mandatory
User provides more than 1 year of date range for postedFrom and postedTo
OR
User provides more than 1 year of date range for rdlfrom and rdlto	Date range must be 1 year(s) apart
User provides invalid API Key	An invalid api_key was supplied
User does not provide any API key	No api_key was supplied
User clicks on the description link available in the response and description content is not available	Description Not Found
FAQ
Back to top

Contact Us
Reach out to the SAM.gov team at www.fsd.gov
Change Log
Date	Version	Description
5/20/19	v0.1	Base Version
8/6/19	v0.2	Format Updated
10/17/19	v0.3	Added Set-Aside Code
10/23/19	v0.4	Set-Aside Values Updated
10/24/19	v0.5	Office Address Description Updated
11/1/19	v1.0	Initial Release Finalized
12/2/19	v1.1	Added OpenAPI Specification
12/18/19	v1.2	Opportunities Response parameters updated to include Award Details JSON Specification and provided the examples
1/20/2020	v1.3	Added Award Response and Versioning columns
1/31/2020	v1.4	Added field “ResourceLinks” with Coming Soon to prod
2/18/2020	v1.5	Added UEI information and versioning column and response example for awards
2/27/2020	v1.6	Added ResourceLinks to Response Section
6/20/2020	v1.7	Added additional information field to point of contact parameter in the response
7/3/2020	v1.8	Updated field parameters to include all FH information for given notices in both request and response
9/14/2020	v1.9	Updated OpenAPI Specification section to include v2 endpoints
10/25/2020	v1.91	Added new request field for status
05/12/2021	v1.92	Changed Beta.SAM to SAM and Changed Beta to Prodution based on JIRA IAEDEV-51713
05/17/2021	v1.93	Changed Beta to Prod and removed coming soon JIRA IAEDEV-51713
05/18/2021	v1.94	Changed SAM.Gov to SAM.gov based on JIRA IAEDEV-51713
05/18/2021	v1.95	Changed Prod to Production JIRA IAEDEV-51713
05/19/2021	v1.96	Changed SAM.Gov to SAM.gov based on JIRA IAEDEV-51713
06/11/2021	v1.97	Added inactive in status


#SAM.gov Contract Awards API
verview
The Contract Awards API allows users to request revealed Award and IDV contract data, and unrevealed Award and IDV contract data, based on the user’s account and/or system account accessing the Contract Awards API.

Award and IDV contract data consists of:

Delivery/Task Orders
Government-Wide Agency Contracts
Basic Ordering Agreements
Blanket Purchasing Agreements
Indefinite Delivery Contracts
Other Transaction IDVs
Federal Supply Schedules
Purchase Orders
Definitive Contracts
BPA Calls
Other Transaction Orders
Other Transaction Agreements
Revealed/Unrevealed Data
Revealed data includes contracts that were either funded or awarded by a Civilian Subtier, as well as contracts funded and awarded by DoD, provided the Date Signed is at least 90 days prior to today’s date. Unrevealed data consists of all revealed contracts, plus DoD contracts that were funded and awarded with a Date Signed less than 90 days prior to today. Additionally, the UEI and Name for the Immediate Parent and Domestic Parent of the Awardee is included in the Unrevealed API response and excluded from the Revealed API response.

Key Features of the Contract Awards API
It offers several optional search parameters, filtering by sections, AND (&), OR (~), NOT (!) conditions, null searches, and a free text search q to obtain the desired data.
It returns synchronous responses.
It returns ten records per page in the JSON format by default, and allows users to increase the response to 100 records per page through the use of the limit parameter.
It can return only the first 400,000 records.
The following characters are not allowed to be sent in the parameter values with the API request: & | { } ^ \
Additional Features of the Contract Awards API
Extract
It can serve as an Extract API with the addition of the “format” parameter in the request. Following are the key features of the getList Contracts Extract API:

It offers several optional search parameters, filtering by sections, AND, OR, NOT conditions and a free text search q to obtain the desired data.
It returns asynchronous responses by sending file downloadable link.
It returns data in the JSON or CSV format as selected by the user.
It can return only the first 1,000,000 records.
PIID Aggregation
The piidAggregation parameter allows users to retrieve a high-level summary of a contract and any contracts that reference it. This parameter must be used in conjunction with the piid parameter. If the piid alone is not unique, the parameter referencedIdvPiid must also be provided.

When piidAggregation is sent and a valid PIID is provided, the response will include an award family summary with:

The total number of records within the award family. (including base and modifications)
The total dollars obligated
If the provided PIID is an IDV (excluding FSS), the summary will also include a summary of referencing Delivery Orders or BPA Calls:

The number of Base Delivery Orders or BPA Calls (excluding modifications) referencing the IDV
The number of Delivery Orders or BPA Calls (including base and modifications) referencing the IDV
The total dollars obligated on those Delivery Orders or BPA Calls
If the provided PIID is an FSS, the summary will include a summary of BPAs referencing the PIID, and a summary of BPA Calls referencing the BPAs:

The number of Base BPAs (excluding modifications) referencing the FSS
The number of BPAs (including base and modifications) referencing the FSS
The total dollars obligated on those BPAs
The number of Base BPA Calls referencing the BPAs (excluding modifications)
The number of BPA Calls referencing the BPAs
The total dollars obligated on those BPA Calls
Deleted Contracts
The Contract Awards API can be used to pull the deleted contracts by sending the query parameter ‘deletedStatus’. When the query parameter ‘deletedStatus’ is sent in the API request, the Contract Award API will return deleted contracts only. The same revealed/unrevealed logic will be applied when parameter ‘deletedStatus’ is provided in the request. The Contract Awards API will have the capability to return contracts deleted within the last 6 months.

Back to top

Getting Started
API endpoints
Production:

https://api.sam.gov/contract-awards/v1/search?api_key=
https://api.sam.gov/contract-awards/v1/search?deletedStatus=yes&api_key=
Alpha:

https://api-alpha.sam.gov/contract-awards/v1/search?api_key=
https://api-alpha.sam.gov/contract-awards/v1/search?deletedStatus=yes&api_key=
User Requirements
To access revealed contract data:

Users must have a non-Federal/Federal Individual (Personal) account and the respective API Key, or a non-Federal/Federal System Account and the respective API Key in SAM.gov.
Users can make GET calls using any Browser or a Restful API client such as Postman.
To access unrevealed contract data:

Available only to users assigned to DoD.
Users must have a Federal Individual (Personal) account or a Federal System Account and the respective API Key in SAM.gov.
Users can make GET calls using any Browser or a Restful API client such as Postman.
Individual (Personal) Accounts
The SAM.gov Federal or non-Federal registered users must obtain the API Key from the https://sam.gov/profile/details page using the field, “Public API Key”.
image info
Click on the “Eye” icon, enter the “Enter One-time Password” (this value will be sent to your email address that is associated with your registered account), hit “Submit”, for the API Key value to appear in the box.
System Accounts
The SAM.gov non-Federal registered users must request for a System Account. If their registration and request criteria are satisfied, then they will be provided with the System Accounts” widget on their SAM.gov “Workspace” page.
The SAM.gov Federal registered users must contact their CCB representatives for obtaining the “System Accounts” widget on their SAM.gov “Workspace” page.
Users must create their System Account using the “System Accounts” widget and get it approved.
Users must then set the password for the System Account.
After the above step is successfully completed, users will see a new section for retrieving the API Key. Users must enter the password to retrieve this value.
System Accounts must satisfy the following criteria to successfully utilize the Contract Awards API:

System Information
Unique System ID: The System Account ID
Permissions
Contract-Awards: read public –> Gives access to the contract-awards data.
Security Information
IP Address: List all the IP Addresses that the System invokes the API from.
Type of Connection: REST APIs
System Account Password
System Account API Key
API Key Rate Limits
Type of User Account	Type of API Key	Default API Daily Rate Limit
Non-federal user with no Role in SAM.gov	Personal API key	10 requests/day
Non-federal user with a Role in SAM.gov	Personal API key	1,000 requests/day
Federal User	Personal API key	1,000 requests/day
Non-federal System user	System account API key	1,000 requests/day
Federal System user	System account API key	10,000 requests/day
Utilizing the API Extract
To retrieve Contract data in the CSV format, “format=csv” must be provided in the request.
To retrieve Contract data in the JSON format, “format=json” must be provided in the request.
If the request is executed successfully, then a file downloadable URL with Token will be returned. This URL can also be obtained in emails by providing “emailId=Yes” in the request.
In the file downloadable URL, the phrase REPLACE_WITH_API_KEY must be replaced with a valid API Key and sent as another request.
If the file is ready for download, then the users can retrieve it. If the file is not ready for download, then the users will need to try again in some time.
API Description
Query String Parameters:
The Contract Awards API offers several optional search parameters that can be provided independently or in combination with each other.
Response Schema:
Based on the request parameters and account associated with the API Key provided in the request, the API returns the following response parameters.
Back to top

OpenAPI Specification File
You can view the full details of this API in the OpenAPI Specification file available here: Open API specification file for the Contract Awards API

Additional Help References
Go to SAM.gov Data Services for mapping and Data Dictionary documents.

HTTP Response Codes
The API will return one of the following responses:

Code	Description
200	The API call is successful.
204	- No Data found:
v1:
“message”: “No Content Found”
“detail”: “Any Date parameter must be provided in the MM/DD/YYYY or [MM/DD/YYYY,MM/DD/YYYY] format.”
400	Application Level Error Messages
400	- Invalid “Date” format:
v1:
“message”: “Dates must be specified in the MM/DD/YYYY or [MM/DD/YYYY,MM/DD/YYYY] format.”
“detail”: “Any Date parameter must be provided in the MM/DD/YYYY or [MM/DD/YYYY,MM/DD/YYYY] format.”
400	- Invalid “Dollar” format:
v1:
“message”: “Dollars must be specified in a numeric format excluding commas or in the range format contained within brackets with a comma separating the lower range and upper range [Lower Range,Upper Range].”
“detail”: “Any Dollar parameter must be provided in the numeric format excluding commas or [Lower Range,Upper Range] format.”
400	- Invalid Search Parameter:
v1:
“message”: “The search parameter, < user-provided invalid parameter > does not exist.”
“detail”: “Please refer to https://open.gsa.gov/api/contract-awards/ for a list of allowable search parameters.”
400	- If ‘includeSections’, ‘emailId’ or ‘format’ is sent in the “q” parameter:
v1:
“message”: “The search parameters ‘includeSections’,’emailId’, ‘piidaggregation’, and ‘format’ are not permitted inside Query Param(q)”
“detail”: “Please provide these parameters separately”.
400	- More than 100 UEI values are sent:
v1:
“message”: “More than 100 Unique Entity IDs are not allowed.”
“detail”: “Please limit the number of Unique Entity IDs to 100.”
400	- More than 100 Parent UEI values are sent:
v1:
“message”: “More than 100 Parent Unique Entity IDs are not allowed.”
“detail”: “Please limit the number of Parent Unique Entity IDs to 100.”
400	- More than 100 Consortia UEI values are sent:
v1:
“message”: “More than 100 Consortia Unique Entity IDs are not allowed.”
“detail”: “Please limit the number of Consortia Unique Entity IDs to 100.”
400	- More than 100 CAGE Code values are sent:
v1:
“message”: “More than 100 CAGE Codes are not allowed.”
“detail”: “Please limit the number of CAGE Codes to 100.”
400	- More than 100 PSC Codes are sent:
v1:
“message”: “More than 100 Product or Service Codes are not allowed.”
“detail”: “Please limit the number of Product or Service Codes to 100.”
400	- More than 100 NAICS Codes are sent:
v1:
“message”: “More than 100 NAICS Codes are not allowed.”
“detail”: “Please limit the number of NAICS Codes to 100.”
400	- “emailId” is sent on its own:
v1:
“message”: “The search parameter ‘emailId’ must be provided in conjunction with the search parameter ‘format’.”
“detail”: “Users can opt for receiving the requested JSON/CSV files in their emails.”
400	- “piidaggregation” is sent on its own:
v1:
“message”: “The search parameter ‘piidaggregation’ must be provided in conjunction with the search parameter ‘piid’.”
“detail”: “The ‘piidaggregation’ parameter cannot be provided on its own.”
400	- “piidaggregation” is sent with a PIID that is not unique:
v1:
“message”: “The search parameter ‘piidaggregation’ must be provided in conjunction with the search parameters ‘piid’ and ‘referencedIdvPiid’ when the ‘piid’ is not unique.”
“detail”: “The ‘piidaggregation’ parameter must return a unique record.”
400	- File size exceeded for JSON or CSV exports:
v1:
“message”: “Total Number of Records: < the total number > exceeded the maximum allowable limit: 1,000,000. Please provide a suitable search parameter to refine your search.”
“detail”: “Count Exceeded Error”
400	- JSON or CSV file generation is in-progress:
v1:
“message”: “The requested JSON or CSV file is not generated yet. Please try again later.”
“details”: “Larger files will take some time to process.”
400	- Using an expired Token for downloading JSON or CSV files:
v1:
“message”: “The requested JSON or CSV file token is expired.”
“detail”: “Please verify the token number.”
400	- Different IP Address than that mentioned in the System Account:
v1:
“message”: “IP Addresses associated with this System Account are different from that sending the request. Please submit your requests from a valid system.”
“detail”: “Please verify your IP Address sending this request is associated with this System Account.”
400	- Insufficient API Key privileges to download a JSON or CSV File:
v1:
“message”: “The API Key is not authorized to access this < file type > Extract”
400	- Query parameter limit sent with a value greater than 100:
v1:
“message”: “The max value allowed for parameter ‘limit’ is 100.”
“detail”: “Please provide a value equal to or less than 100 for the query parameter ‘limit’.”
400	- Query parameter ‘limit’ multiplied by ‘offset’ is greater than 400,000:
v1:
“message”: “You may only page through the first 400,000 records. Any request where ‘offset’ x ‘limit’ is greater than 400,000 will be rejected.”
“detail”: “Please provide values equal to or less than 400,000 for the query parameters ‘offset’ x ‘limit’.”
403	Forbidden
403	- Missing API Key:
v1:
“message”: “No API Key was supplied. Please submit with a valid API key.”
403	- An invalid API Key:
v1:
“message”: “An invalid API key was supplied. Please submit with a valid API key.”
403	- A disabled API Key:
v1:
“message”: “The API key supplied has been disabled. Please submit with a valid API key.”
500	Internal Server Error
Back to top

Examples
Example 1: Get Base Contracts modified between January 1st, 2025 and today, Contracted by DoD with a Dollar Obligated between $0.00 and $100,000,000.99.
Request URL:
Response (JSON Output)
Example 2: Get Purchase Orders Approved between January 1st, 2025 and August 19th, 2025 with a NIACS code of 513310 or 541512 or 111150.
Request URL:
Response (JSON Output)
Example 3: Get only the Contract IDs for GSA IDVs closed between January 1st, 2025 and today.
Request URL:
Response (JSON Output)
Example 4: Get Service Contracts performed in Virginia in FY25 with a Contracting Officer’s Business Size Selection of Small, and only return the Contract ID, Award Details, and Awardee Data
Request URL:
Response (JSON Output)
Example 5: Get Deleted Contracts modified between Oct 1st and Oct 2nd, 2025, and return only the Contract ID.
Request URL:
Response (JSON Output)
Back to top

Additional Information
You can view the full details of the differences between the FPDS legacy API and SAM.gov API available here: Variance Document

Disclaimer: Limitation on Permissible Use of Dun & Bradstreet, Inc. (D&B) Data

This website contains data supplied by third party information suppliers, including Dun & Bradstreet (D&B). For the purposes of the following limitation on permissible use of D&B data, which includes each entity’s DUNS Number and its associated business information, “D&B Open Data” is defined as the following data elements: Legal Business Name, Street Address, City Name, State/Province Name, Country Name, County Code, State/Province Code, State/Province Abbreviation, ZIP/Postal Code, Country Name and Country Code. Entity registration, exclusion, or contract award records in SAM may contain D&B-supplied data. Applicable records containing D&B data include all base award notices with an award date earlier than 4/4/2022. These records show the Entity Validation Service (EVS) Source as D&B in outbound data streams.
D&B hereby grants you, the user, a license for a limited, non-exclusive right to use D&B Open Data within the limitations set forth herein. By using this website you agree that you shall not use D&B Open Data without giving written attribution to the source of such data (i.e., D&B) and shall not access, use or disseminate D&B Open Data in bulk, (i.e., in amounts sufficient for use as an original source or as a substitute for the product and/or service being licensed hereunder).
Except for data elements identified above as D&B Open Data, under no circumstances are you authorized to use any other D&B data for commercial, resale or marketing purposes (e.g., identifying, quantifying, segmenting and/or analyzing customers and prospective customers). Systematic access (electronic harvesting) or extraction of content from the website, including the use of “bots” or “spiders”, is prohibited. Federal government entities are authorized to use the D&B data for purposes of acquisition as defined in FAR 2.101 and for the purpose of managing Federal awards, including sub-awards, or reporting Federal award information.
GSA assumes no liability for the use of the D&B data once it is downloaded or accessed. The D&B data is provided “as is” without warranty of any kind. The D&B data is the intellectual property of D&B. In no event will D&B or any third party information supplier be liable in any way with regard to the use of the D&B data. For more information about the scope of permissible use of D&B data licensed hereunder, please contact D&B at datause_govt@dnb.com.
Back to top

Contact Us
Reach out to the SAM.gov team at www.fsd.gov for inquiries and help desk support.
Before contacting the help desk, conduct your own initial troubleshooting
Conduct a recent review of the open.gsa.gov/api specifications
Confirm that the API key being used is still active
Confirm that the system account you are using has “read public” permissions as applicable (PUBLIC Calls)
Confirm that the IP addresses registered with your system account are current
When submitting help desk tickets for API or system connection issues, provide the following:
The exact API requests that you were trying to send
The exact error messages that you were receiving
The exact dates and times when you received the errors
Screenshots (with the actual API request and the error) [Attach to the ticket]
The System Account ID/Name that was trying to make API calls
Screenshots of the parameters used for API call [Attach to the ticket]
Screenshots of the Headers used for the API call [Attach to the ticket]
Users requesting access to the test site (alpha.sam.gov) should follow the below steps. These steps ONLY apply to alpha.sam.gov access requests.
Navigate to www.fsd.gov
Sign into the FSD platform using your FSD credentials
Select “Create an Incident”
Create an Incident
System Name: SAM(System for Award Management)
Issue Type: System Accounts
Issue Type 2: Manage Account
Subject: System account approval in alpha.sam.gov
Please describe your issue: (Copy and paste the below information into the ticket, filling in your information within the brackets)
I am creating/editing a system account and have submitted my account in alpha.sam.gov for approval. I would like to request alpha.sam.gov system account review and approval for [Name of the alpha.sam.gov system account].
Back to top

Change Log
Date	Version	Description
12/05/2025	v1.0	Base Version

#Federal Procurement Data System - FPDS API
https://www.fpds.gov/fpdsng_cms/index.php/en/worksite.html

#SAM.gov Entity/Exclusions Extracts Download API
Overview
The Extracts Download API allows users to request Unclassified (“Public”), Controlled Unclassified Information (CUI) “For Official Use Only” (FOUO) or CUI “Sensitive” entity extracts and Unclassified (“Public”) exclusion extract, based on the sensitivity level of the user account and through several optional request parameters.

Public Entity Extracts:

They constitute publicly available entities and their unclassified data available under the Freedom of Information Act (FOIA) for those registered in SAM.gov to do business with the Federal government.

FOUO (CUI) Entity Extracts:

They constitute both the publicly available entities and the entities that have opted out of public display, along with their unclassified data available under the Freedom of Information Act (FOIA) and FOUO CUI data.

Sensitive (CUI) Entity Extracts:

They constitute both the publicly available entities and the entities that have opted out of public display, along with their unclassified data available under the Freedom of Information Act (FOIA), FOUO CUI data and Sensitive CUI data.

Public Exclusions Extracts:

They constitute publicly available list of all parties with a currently active exclusion in SAM.gov.

Extract Calendar

Monthly Public, FOUO (CUI) and Sensitive (CUI) Extracts	
They are produced on the first Sunday of each month. Kindly check after 7 AM Eastern time.
The date on the .ZIP file matches the date when the file was generated.
E.g.: The April monthly files were generated and dated on 20220403.
The date on the .ZIP file matches the date on the .dat file inside.
These files contain all active entities and entities expired in the last 6 months.
File Naming Convention:
Monthly ASCII:
SAM_PUBLIC_MONTHLY_V2_YYYYMMDD.ZIP
SAM_FOUO_MONTHLY_V2_YYYYMMDD.ZIP
SAM_SENSITIVE_MONTHLY_V3_YYYYMMDD.ZIP
Monthly UTF-8:
SAM_PUBLIC_UTF-8_MONTHLY_V2_YYYYMMDD.ZIP
SAM_FOUO_UTF-8_MONTHLY_V2_YYYYMMDD.ZIP
SAM_SENSITIVE_UTF-8_MONTHLY_V3_YYYYMMDD.ZIP
Daily FOUO (CUI) and Sensitive (CUI) Extracts	
They are produced every Tuesday-Saturday. Kindly check after 7 AM Eastern time.
The date on the .ZIP file matches the date when the file was generated.
E.g.: The file generated on 04/05/2022 will show 20220405.
The date on the .ZIP file matches the date on the .dat file inside.
These are incremental files that contain new/updated/deactivated/expired entities since the previous day’s file.
File Naming Convention:
Daily ASCII:
SAM_FOUO_DAILY_V2_YYYYMMDD.ZIP
SAM_SENSITIVE_DAILY_V3_YYYYMMDD.ZIP
Daily UTF-8:
SAM_FOUO_UTF-8_DAILY_V2_YYYYMMDD.ZIP
SAM_SENSITIVE_UTF-8_DAILY_V3_YYYYMMDD.ZIP
Daily Exclusion Extracts	
They are produced every day. Kindly check after 7 AM Eastern time.
The date on the .ZIP file matches the date when the file was generated.
E.g.: The file generated on 04/05/2022 will show 2022095.
The date on the .ZIP file matches the date on the .CSV file inside.
These files contain all the active exclusions.
File Naming Convention:
Daily ASCII:
SAM_Exclusions_Public_Extract_V2_YYDDD.ZIP (YYDDD is the Julian Date)
E.g.: The file for 04/06/2022 would be SAM_Exclusions_Public_Extract_V2_22096.ZIP.
Daily FASCSA Exclusion Extracts	
They are produced every day. Kindly check after 7 AM Eastern time.
The date on the .CSV file matches the date when the file was generated.
The file generated on 10/04/23 will show 23277.
These files contains all FASCSA active exclusions.
File Naming Convention:
Daily ASCII:
FASCSAOrdersYYDDD.CSV (YYDDD is the Julian Date)
E.g.: The file for 10/04/2023 would be FASCSAOrders23277.CSV.
Back to top

Getting Started
API endpoints
Production:

https://api.sam.gov/data-services/v1/extracts?api_key=
https://api.sam.gov/data-services/v1/extracts?
Alpha:

https://api-alpha.sam.gov/data-services/v1/extracts?api_key=
https://api-alpha.sam.gov/data-services/v1/extracts?
User Requirements
To access Public extracts:

Users must have a non-Federal/Federal Individual (Personal) account and the respective API Key, a non-Federal/Federal System Account with the “Read Public” permission and the respective API Key in SAM.gov.
Users can make GET calls using any Browser or a Restful API client such as Postman.
To access FOUO (CUI) extracts:

Users must have a Federal System Account with the “Read FOUO” permission and the respective API Key in SAM.gov.
Users can make GET calls using any Browser, or a Restful API client such as Postman.
To access Sensitive (CUI) extracts:

Users must have a Federal System Account with the “Read Sensitive” permission and the respective API Key in SAM.gov.
Users must make POST calls using a Restful API client such as Postman.
Individual (Personal) Accounts
The SAM.gov Federal or non-Federal registered users must obtain the API Key from the https://sam.gov/profile/details page using the field, “Public API Key”.
image info
Click on the “Eye” icon, enter the “Enter One-time Password” (this value will be sent to your email address that is associated with your registered account), hit “Submit”, for the API Key value to appear in the box.
System Accounts
The SAM.gov non-Federal registered users must request for a System Account. If their registration and request criteria are satisfied, then they will be provided with the System Accounts” widget on their SAM.gov “Workspace” page.
The SAM.gov Federal registered users must contact their CCB representatives for obtaining the “System Accounts” widget on their SAM.gov “Workspace” page.
Users must create their System Account using the “System Accounts” widget and get it approved.
Users must then set the password for the System Account.
After the above step is successfully completed, users will see a new section for retrieving the API Key. Users must enter the password to retrieve this value.
System Accounts must satisfy the following criteria to successfully utilize this API:

System Information
Unique System ID: The System Account ID
Permissions
Entity Information: read public –> Gives access to the Public extracts
Entity Information: read public, read fouo –> Gives access to the Public and FOUO (CUI) extracts.
Entity Information: read public, read fouo, read sensitive –> Gives access to the Public, FOUO (CUI) and Sensitive (CUI) extracts.
Security Information
IP Address: List all the IP Addresses that the System invokes the API from.
Type of Connection: Data Service Extracts
System Account Password
System Account API Key
API Key Rate Limits
Type of User Account	Type of API Key	Default API Daily Rate Limit
Non-federal user with no Role in SAM.gov	Personal API key	10 requests/day
Non-federal user with a Role in SAM.gov	Personal API key	1,000 requests/day
Federal User	Personal API key	1,000 requests/day
Non-federal System user	System account API key	1,000 requests/day
Federal System user	System account API key	10,000 requests/day
Sensitive API Process:
Back to top

API Description
Query String Parameters:
The Extracts Download API offers several optional search parameters.
Extract Mapping Document and Layouts:
Please refer to the following:
Sample Extract File Names:
Extract Download API Sample Requests:
OpenAPI Specification File
You can view the full details of this API’s in the OpenAPI Specification file available here:
Open API specification file for the Entity/Exclusions Extracts Download API

Back to top

Sample Extract Files
Extract files with UEI Information:

Click to view Public Monthly V2 Extract File
Click to view FOUO Monthly V2 Extract File
Click to view Sensitive Monthly V3 Extract File
Click to view Exclusions Public V2 Extract File
Click to view FASCSA Order Exclusions Public V2 Extract File
Back to top

HTTP Response Codes
The API will return one of the following responses:

HTTP Response Code	Description
200	Successful. Data will be returned in JSON format.
400	Application Level Error Messages:
* User does not have permission to download the file.
* Missing required parameters, fileName OR fileType
* The requested extract file not found
* Invalid date format
* This http method is not allowed to download sensitive extracts. Only POST is supported for sensitive extracts.
* This http method is not allowed to download non-sensitive extracts. Only GET is supported for non-sensitive extracts.
* No api_key was supplied in request body. Please submit with a valid API key.
* No system account credentials are provided. Please provide credentials via basic authentication.
* The parameter fileName cannot be used with any other parameters.
* The File does not exist with the provided parameters
* The requested extract file needs FOUO roles to download
* IP Addresses associated with this System Account are different from that sending the request. Please submit your requests from a valid system.
* Insufficient privileges to perform the operation - System account must have Type of Connection as Restful.
406	Invalid Accept Header.
415	Invalid Content-Type Header.
Back to top

Contact Us
Reach out to the SAM.gov team at www.fsd.gov for inquiries and help desk support.
Before contacting the help desk, conduct your own initial troubleshooting
Conduct a recent review of the open.gsa.gov/api specifications
Confirm you are using an API tool, not a browser to send the request. (FOUO & Sensitive Calls)
Confirm you are using the username/password for the system account that created the API key in the authentication header. (Sensitive Calls)
Confirm you used POST and not GET for this request (Sensitive Calls)
Confirm that the API key is from a system account (FOUO & Sensitive Calls)
Confirm that the API key being used is still active
Confirm that the system account you are using has “read fouo” or “read sensitive” permissions as applicable (FOUO & Sensitive Calls)
Confirm that the IP addresses registered with your system account are current
When submitting help desk tickets for API or system connection issues, provide the following:
The exact API requests that you were trying to send
The exact error messages that you were receiving
The exact dates and times when you received the errors
Screenshots (with the actual API request and the error) [Attach to the ticket]
The System Account ID/Name that was trying to make API calls
Screenshots of the parameters used for API call [Attach to the ticket]
Screenshots of the Headers used for the API call [Attach to the ticket]
Users requesting access to the test site (alpha.sam.gov) should follow the below steps. These steps ONLY apply to alpha.sam.gov access requests.
Navigate to www.fsd.gov
Sign into the FSD platform using your FSD credentials
Select “Create an Incident”
Create an Incident
System Name: System for Award Management (SAM)
Is this related to the American Rescue Plan Act?: No
Issue Type: Other
Business Type: Other
Subject (select 1):
Option A: I need a role to test in alpha.sam.gov.
Option B: System account approval in alpha.sam.gov
Please describe the issue: (Copy and paste the below information into the ticket, filling in your information within the brackets)
Option A: I have already navigated to alpha.sam.gov and created a user account, following the same steps for creating an account in sam.gov. I would like to conduct testing but do not have the necessary role(s) in alpha.sam.gov. The account that needs role assignment is associated with [EMAIL ADDRESS]. I request a [ROLE] role for the [DOMAIN] domain in alpha.sam.gov.
Option B: I am creating/editing a system account and have submitted my account in alpha.sam.gov for approval. I would like to request alpha.sam.gov system account review and approval for [Name of the alpha.sam.gov system account].
Back to top

Change Log
Date	Version	Description
06/03/2019	v1.0	Base Version
08/15/2019	v1.1	* Added Beta.SAM.Gov to the page title.

* Clarified the Alpha and Beta endpoints.
12/20/2019	v1.2	* Added Sample FOUO and Sensitive File Names and Revised extract layouts for the upcoming UEI/EVS changes.

* Added “COMING SOON” section for upcoming changes to Alpha and Beta endpoints to meet new API standards.
02/25/2020	v1.3	* Updated Alpha endpoint to meet new API standards.

* Added Sample Extract Files.
02/28/2020	v1.4	* Updated Beta endpoint to meet new API standards.

* Removed “COMING SOON” information in Getting Started section.

* Added FOUO and Sensitive Sample Extract Files for different versions.
04/20/2020	v1.5	Updated Public, FOUO and Sensitive Sample Extract Files that includes UEI information.
06/10/2020	v1.6	Added the endpoint, new process and an example for the Download API .
08/17/2020	v1.7	* The Sensitive Alpha endpoint in “Getting Started” has been corrected and the Sample Extract Authorization screenshot in “Explanation of the API using Examples” has also been updated to reflect the correct endpoint.

* Sensitive data sample calls in the “Explanation of the API using Examples” have also been updated to show that the API key is no longer sent in the request URL.

* The “Sensitive Download API Process” section has been updated with additional steps for sending Sensitive requests (sending “Accept” and “Content-Type” parameters).

* The Sample Request Header screenshot in the “Explanation of the API using Examples” has been updated to reflect the new parameters as well. Two new codes (406, 415) have been added in the “HTTP Response Codes” section.
08/31/2020	v1.8	* Updated the Getting Started section to include the Sensitive Beta endpoint.
02/05/2021	v1.9	* Added V1/V2 Public, V3 Sensitive, and V2 FOUO files available in Alpha S3.

* Added version parameter

* Updated error messages

* Added note to charSet parameter stating exclusions file type is not applicable
03/12/2021	v2.0	* Added additional FOUO sample files.

* Added note that only system account keys can be used for FOUO and sensitive downloads.
04/08/2021	v2.1	* Updated Contact Us information.

* Added Entity Extract Calendar under Overview.
04/29/2021	v2.2	* Added note above list of sample files mentioning that files are for Alpha.

* Added description to 400 http response code describing Type of Connection error.

* Updated openapi spec file.
05/12/2021	v2.3	* Updated instances of beta.sam.gov to SAM.gov.

* Removed non-relevant information for Beta api.
07/16/2021	v2.4	* Updated the instructions on sending “Basic Auth” under the “Authorization” header.

* Added the Type of Connections and Rate Limits table.

* Updated the Contact Us information.

* Added example curl requests.
09/21/2021	v2.5	* Added the “Please refer to the SAM Master Extract Mapping document” subsection under the “Explanation of the API using Examples” section.
10/06/2021	v2.6	* Updated the “Contact Us” section.
10/21/2021	v2.7	* Added Expected Results to Data Package Sample API Calls.

* Updated Extract Mapping Files.
02/01/2022	v2.8	* Updated the Exclusions Extract Layout file.

* Updated the Exclusions Public V2 Extract file.
04/04/2022	v2.9	* Sample Extract Files section: Removed old sample files that had DUNS information and provided new files with UEI information.

* Updated “Effective April 2022: SAM Master Extract Mapping” to remove the DUNS occurrences.

* Updated the “April 2022 release: FOUO Extract Layout” with the correct Sensitivity levels for the Points Of Contact elements.

* Updated the “April 2022 release: Sensitive Extract Layout” to reflect the correct order for “IMMEDIATE PARENT EVS SOURCE”.

* Updated the “April 2022 release: Exclusions Extract Layout” to remove the DUNS occurrences.

04/08/2022	v3.0	* Removed all the references to older files that are no longer valid.

* Provided references to the new files.

* Reorganized the Sensitive Postman and curl examples for a better flow of content.

08/08/2022	v3.1	* Updated to clarify the use of Controlled Unclassified Information (CUI) data.

03/13/2023	v3.2	* Deleted the MPIN row from the “SAM Master Extract Mapping” file.

* Updated row # 288 (which used to track MPIN) in the “Sensitive Extract Layout” file to indicate that the field is deprecated.

* Removed the MPIN value from the sample “Sensitive Monthly V3 Extract File”.

06/27/2023	v3.3	* Updated “Effective April 2022” to “Effective June 2023”.

* Updated the “June 2023 release: SAM Master Extract Mapping” STRING Clarification tab to include the following updates:
 1. NAICS Exception String table updated to reflect January 2023
 changes
 2. SBA Business Types String table updated to include new value:
 “A4- SBA Certified Small Disadvantaged Business”

09/11/2023	v3.4	* Removed “SAM Master Extract Mapping document”.

12/01/2023	v3.5	A new FASCSA Order Exclusions Extract has been created, and the V1 Extracts Download API is now enabled to download this extract. As part of this change, below are the associated changes made to this OpenGSA page:

* Updated the Extract Calendar to include information on the new FASCSA extract.

* Updated the Query String Parameters section to reflect an example FASCSA extract file name.

* Updated the Extract Mapping Document and Layouts section with a new FASCSA Exclusions extract layout document.

* Updated the Sample Extract File Names with sample FASCSA Exclusions File Names.

* Updated the Extract Download API Sample Requests section with a sample request for a FASCSA extract.

* Updated the Sample Extract Files section with a new FASCSA Order Exclusions Public extract file.


#Regulations.gov API

Overview
When Congress passes laws, federal agencies implement those laws through regulations. These regulations vary in subject, but include everything from ensuring water is safe to drink to setting health care standards. Regulations.gov is the place where users can find and comment on regulations. The APIs allow for users to find creative ways to present regulatory data. To learn more about the program visit the About Us page.

Back to top

Getting Started
To begin using this API, you will need to register for an API Key below.

If you want to use commenting API, you MUST use the form below to register for an API key.

Your API key for kazuhajajapan@gmail.com has been e-mailed to you. You can use your API key to begin making web service requests immediately.

If you don't receive your API Key via e-mail within a few minutes, please contact us.

For additional support, please contact us. When contacting us, please tell us what API you're accessing and provide the following account details so we can quickly find you:

Account Email: kazuhajajapan@gmail.com
Account ID: d7b7a43d-7082-4910-992b-c50460c290ce
After registration, you will need to provide this API key in the X-Api-Key HTTP header with every API request.

HTTP Header Name	Description
X-Api-Key	API key from api.data.gov. For sample purposes, you can use DEMO_KEY as an API key.
Back to top

API Description
Regulations.gov offers a GET API for documents, comments, and dockets. These endpoints can be used for searching documents, comments, and dockets.

Searching for documents
You can search for a list of documents based on the criteria passed by using the endpoint /v4/documents. The search operation supports full text keyword searches and filtering based on a number of available parameters.

Detailed information for a single document
In order to obtain more details about a single document, you can use the endpoint /v4/documents/{documentId}. A document is defined by one of the following types: Proposed Rule, Rule, Supporting & Related, or Other. Each document type has its own set of attributes, which vary based on the Agency posting the document. Another defining characteristic is if the document is part of a Rulemaking or Nonrulemaking Docket.

You can choose to include attachments using include parameter. Attachments are not included by default.

Searching for comments
You can search for a list of comments based on the criteria passed by using the endpoint /v4/comments. The search operation supports full text keyword searches and filtering based on a number of available parameters.

Detailed information for a single comment
In order to obtain more details about a single comment, you can use the endpoint /v4/comments/{commentId}. Each comment has its own set of attributes, which vary based on the Agency posting the comment. Another defining characteristic is if the comment is part of a Rulemaking or Nonrulemaking Docket.

You can choose to include attachments using include parameter. Attachments are not included by default.

Searching for dockets
A docket is an organizational folder containing multiple documents. Dockets can be searched using the endpoint: /v4/dockets.

Detailed information for a single docket
In order to obtain more details about a single docket, you can use the endpoint /v4/dockets/{docketId}. Each docket has its own set of attributes, which vary based on the Agency posting the docket. Another defining characteristic is if the docket is a Rulemaking or a Nonrulemaking Docket

Back to top

Data Limitations
A recent GAO report expressed concerns over whether comment data is fully described to the public, including any limitations. Various aspects of the commenting process can create limitations for certain external users of public comment data and some data fields are managed solely by agencies. For agency-specific commenting practices, contact eRulemaking@gsa.gov. The Open API Specification document has been updated with information on agency configurable fields. For convenience, the data is also provided below in a concise format:

List of fields that are always publicly viewable on a comment
Here is the list of fields that is always available in the JSON response for a comment:

agencyId
comment
commentOnId
docketId
documentId - This field is returned as an Id of the document in the JSON response.
documentType
postedDate
receiveDate
restrictReason - if restrictReasonType is set to “Other”
restrictReasonType - if the document is restricted
reasonWithdrawn - if the comment has been withdrawn
title
trackingNbr
withdrawn
List of agency configurable comment fields
Agency configured fields can be updated by an agency at any point in time and made accessible or inaccessible in the JSON response of a comment. Here is the list of these fields:

city
country
docAbstract
firstName
govAgency
govAgencyType
lastName
legacyId
organization
pageCount
postmarkDate
stateProvinceRegion
subtype
zip
List of fields that are never publicly viewable on a comment
originalDocumentId
address1
address2
email
phone
fax
Examples
Searching for documents
Here are few example queries for searching documents:

Search for term water:
https://api.regulations.gov/v4/documents?filter[searchTerm]=water&api_key=DEMO_KEY
Filter documents by a specific date:
https://api.regulations.gov/v4/documents?filter[postedDate]=2020-09-01&api_key=DEMO_KEY
Filter documents by a date range:
https://api.regulations.gov/v4/documents?filter[postedDate][ge]=2020-09-01&filter[postedDate][le]=2020-09-01&api_key=DEMO_KEY
Search for a documentId:
https://api.regulations.gov/v4/documents?filter[searchTerm]=FDA-2009-N-0501-0012&api_key=DEMO_KEY
Sort documents by posted date in asc:
https://api.regulations.gov/v4/documents?sort=postedDate&api_key=DEMO_KEY
Sort documents by posted date in desc:
https://api.regulations.gov/v4/documents?sort=-postedDate&api_key=DEMO_KEY
Detailed information for a single document
There are few ways a user can query documents endpoint to retrieve detailed information for a document.

Get document details without attachments:
https://api.regulations.gov/v4/documents/FDA-2009-N-0501-0012?api_key=DEMO_KEY
Get document details with attachments:
https://api.regulations.gov/v4/documents/FDA-2009-N-0501-0012?include=attachments&api_key=DEMO_KEY
Searching for comments
Here are few example queries for searching comments:

Search for term water:
https://api.regulations.gov/v4/comments?filter[searchTerm]=water&api_key=DEMO_KEY
Filter comments by a specific date:
https://api.regulations.gov/v4/comments?filter[postedDate]=2020-09-01&api_key=DEMO_KEY
Filter comments by a date range:
https://api.regulations.gov/v4/comments?filter[postedDate][ge]=2020-09-01&filter[postedDate][le]=2020-09-01&api_key=DEMO_KEY
Search for a commentId:
https://api.regulations.gov/v4/comments?filter[searchTerm]=HHS-OCR-2018-0002-5313&api_key=DEMO_KEY
Sort comments by posted date in asc:
https://api.regulations.gov/v4/comments?sort=postedDate&api_key=DEMO_KEY
Sort comments by posted date in desc:
https://api.regulations.gov/v4/comments?sort=-postedDate&api_key=DEMO_KEY
Retrieve all comments for a docket where number of comments is less than 5000:

Step 1: Get all documents for the docketId FAA-2018-1084:
https://api.regulations.gov/v4/documents?filter[docketId]=FAA-2018-1084&api_key=DEMO_KEY
It returns two documents, FAA-2018-1084-0001 and FAA-2018-1084-0002. Each document metadata includes an objectId attribute.

Step 2: Get all comments for each document using objectId:
https://api.regulations.gov/v4/comments?filter[commentOnId]=0900006483a6cba3&api_key=DEMO_KEY
The above request returns a list of comments for document FAA-2018-1084-0001.

Note: Step 2 should be repeated for FAA-2018-1084-0002 in the above example.

Retrieve all comments for a docket where number of comments is greater than 5000:

Step 1: Get all documents for the docketId EOIR-2020-0003:
https://api.regulations.gov/v4/documents?filter[docketId]=EOIR-2020-0003&api_key=DEMO_KEY
The above query returns five documents where four documents are Supporting & Related Material documents and one document is a Proposed Rule. Response for the above request includes an attribute objectId for each document and its set to 09000064846eebaf for the Proposed Rule, EOIR-2020-0003-0001.

Step 2: Get all comments for each document using objectId:
https://api.regulations.gov/v4/comments?filter[commentOnId]=09000064846eebaf&api_key=DEMO_KEY
The above request returns a list of comments for document EOIR-2020-0003-0001, the only Proposed Rule in the docket. totalElements under meta attribute shows that this document has total 88,061 comments.

Note: Step 2 should be repeated for each document.

Step 3: Page through the first set of 5000 documents:
https://api.regulations.gov/v4/comments?filter[commentOnId]=09000064846eebaf&page[size]=250&page[number]=N&sort=lastModifiedDate,documentId&api_key=DEMO_KEY
The first 5000 documents can be retrieved using the query above and paging through the results where N is the page number between 1 and 20. Please note we are sorting the results by lastModifiedDate to ensure we can filter our data by lastModifiedDate later. On the last page of this set, please note the lastModifiedDate of the last document. In our case, EOIR-2020-0003-5548 is the last document on page 20 and the lastModifiedDate attribute of the document is 2020-08-10T15:58:52Z. We will be filtering the data in the next step using this date.

Step 4: Page through the next set of 5000 documents:
https://api.regulations.gov/v4/comments?filter[commentOnId]=09000064846eebaf&filter[lastModifiedDate][ge]=2020-08-10 11:58:52&page[size]=250&page[number]=N&sort=lastModifiedDate,documentId&api_key=DEMO_KEY
The next 5000 documents can be retrieved using the query above and paging through the results where N is the page number between 1 and 20.

The lastModifiedDate attribute of the last document in the first set (Step 3) was 2020-08-10T15:58:52Z. This date translates to 2020-08-10 11:58:52 in Eastern time. Running the above query should return all documents where lastModifiedDate is greater than or equal to 2020-08-10T15:58:52Z. Its important to note that we are running a “greater than or equal to” query to ensure we do not miss any documents where last modified date is 2020-08-10T15:58:52Z.

On the last page of this set, please note the lastModifiedDate of the last document and repeat.

Note: Step 4 should be repeated for as many times as needed to retrieve all 88,061 comments.

Detailed information for a single comment
There are few ways a user can query comments endpoint to retrieve detailed information for a comment:

Get comment details without attachments:
https://api.regulations.gov/v4/comments/HHS-OCR-2018-0002-5313?api_key=DEMO_KEY
Get comment details with attachments:
https://api.regulations.gov/v4/comments/HHS-OCR-2018-0002-5313?include=attachments&api_key=DEMO_KEY
Searching for dockets
Here are few example queries for searching dockets:

Search for term water:
https://api.regulations.gov/v4/dockets?filter[searchTerm]=water&api_key=DEMO_KEY
Search for a docketId:
https://api.regulations.gov/v4/dockets?filter[searchTerm]=EPA-HQ-OAR-2003-0129&api_key=DEMO_KEY
Filter dockets by multiple agencyIds:
https://api.regulations.gov/v4/dockets?filter[agencyId]=GSA,EPA&api_key=DEMO_KEY
Sort dockets by title in asc order:
https://api.regulations.gov/v4/dockets?sort=title&api_key=DEMO_KEY
Sort dockets by title in desc order:
https://api.regulations.gov/v4/dockets?sort=-title&api_key=DEMO_KEY
Detailed information for a single docket
To retrieve detailed information on a docket, the following query can be used:

https://api.regulations.gov/v4/dockets/EPA-HQ-OAR-2003-0129?api_key=DEMO_KEY
Back to top

OpenAPI Specification File
You can view the full details of this API in the OpenAPI Specification file available here: Open API specification file for the Regulations.gov API

Back to top

Frequently Asked Questions
I am not seeing all fields returned by v3/documents endpoint in v4/documents endpoint. How do I access this information?
Our v3 API had a single search endpoint which returned information about documents, comments and dockets. To streamline our data, we have split our search into three endpoints:

Document Search
Comment Search
Docket Search
Further, some data that could be retrieved using search in v3 has now been moved under details endpoint. For example, you can retrieve RIN for a docket using /dockets/{docketId} endpoint. The rin is not returned by /documents endpoint anymore.

How do I get document status from the new /documents endpoint?
The new /v4/documents carries a withdrawn field. This is a boolean field. If set to true, the document is withdrawn otherwise it’s a posted document.

There are strict pagination limits in v4. How do I retrieve all comments in a docket posted on the same day if the number of comments is greater than 2500?
We have added an example that shows how to retrieve more than 5000 comments on a docket. Please see the example section.

Please note the new parameter lastModifiedDate is in beta and may be removed when we have a permanent bulk download solution available.

What is DEMO_KEY api key?
As indicated by name, DEMO_KEY should only be used for demonstration purposes. We have added this api_key to our examples to make it easier for users to copy/paste the urls. It should not be used for anything more than exploring our APIs.

What is the staging API url?
Users should be able to access our staging API at https://api-staging.regulations.gov. Please use this environment for testing purposes.

I have an API key. How many requests can I make per hour and how do I know I am about to reach my request limit?
Please review https://api.data.gov/docs/rate-limits/ for information on rate limits. Commenting API is restricted to 50 requests per minute with a secondary limit of 500 requests per hour.

Can I request rate limit increases for my keys?
GSA may grant a rate limit increase on the GET keys for an indefinite period. Such requests must establish the need to justify the rate limit increases. Each submission will be reviewed and considered on a case-by-case basis.

Back to top

API Calls
Regulations.gov API
 4.0 
OAS 3.0
Public API for Regulations.gov

Servers

https://api.regulations.gov/v4 - Production endpoint for Regulations.gov API

Authorize
documents


GET
/documents
List of documents


GET
/documents/{documentId}
Get detailed information for specified documentId

comments


GET
/comments
List of comments


GET
/comments/{commentId}
Get detailed information for specified commentId

dockets


GET
/dockets
List of dockets


GET
/dockets/{docketId}
Get detailed information for specified docketId

comment submission utilities


GET
/agency-categories
Returns a list of categories

Regulations.gov API:
ghC0vhEdxLcw96KBRIbeshYSmTsrc5smzamiQrlk

#Contract-Awarded Labor Category (CALC) API
This project is in BETA
This project is providing Digital Experience (DX) CALC+ Quick Rate API. Have feedback or questions? Please let us know!

LEGACY RATES API DECOMMISSION

DECOMMISSION DATE: February 2025

The legacy Rates API has been retired.

The legacy CALC Rates API has been replaced by a modernized version powered by AWS OpenSearch with a broad range of feature enhancements, optimizations, and data quality improvements.

The new CALC+ application (and APIs) can be experienced at the following URL: https://buy.gsa.gov/pricing/

The new Ceiling-Rates API documentation can be found below.

Overview
The CALC+ Labor Ceiling Rates tool is a pricing research tool located on buy.gsa.gov to support government acquisition professionals in services pricing business intelligence. Acquisition staff can use Labor Ceiling Rates data to help conduct market research with price analysis, develop Independent Government Cost Estimates (IGCEs), and aid in benchmarking competitive pricing.

Access to the CALC+ Prices Paid tool begins with Pricing Central, https://buy.gsa.gov/pricing/. Access to this tool does not require user credentials or authentication.

The CALC+ Labor Ceiling Rates tool is powered by the CEILINGRATES API.

The CEILINGRATES API data is refreshed everyday overnight.

Entrypoint
The legacy URL is being retired and you should not use it. Please see decommissioning message above. https://api.gsa.gov/acquisition/calc/v2/api/rates/

The URL for the CALC+ Quick Rate API is

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/

The default API URL used within our application is

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?
page=1
&page_size=20
&ordering=current_price
&sort=asc
&filter=experience_range:0,45
&filter=price_range:15,500
We use this to provide a sensible default experience for all users when first loading the application.

JSON Response
A CEILINGRATES API JSON response will consist of an array of objects nested within a hits object. Here is an example:

"hits": {
    "total": {
        "value": 10000,
        "relation": "gte"
    },
    "max_score": null,
    "hits": [
        {
            "_index": "ceilingrates",
            "_type": "_doc",
            "_id": "6340611",
            "_score": null,
            "_source": {
                "contract_end": "2028-12-17",
                "security_clearance": "No",
                "next_year_price": 17.52,
                "second_year_price": 17.52,
                "vendor_name": "ALCAZAR TRADES, INC.",
                "idv_piid": "GS21F026BA",
                "business_size": "S",
                "contract_start": "2013-12-18",
                "labor_category": "Special Event Set-Up",
                "schedule": "MAS Consolidated MOD Refresh 15+",
                "cont_end_dtg": "20281217",
                "min_years_experience": 1,
                "sin": "561210FAC",
                "worksite": "Customer Facility",
                "education_level": "HS",
                "id": 6340611,
                "current_price": 17.52,
                "dt_termg": null,
                "category": "Facilities",
                "subcategory": "Facilities Maintenance and Repair",
                "_timestamp": "2024-05-02T10:00:24Z",
                "cont_beg_dtg": "20131218"
            },
            "sort": [
                17.52
            ]
        },
        ...etc
    ]
}
Valid Fields
Note

These are important to remember as the API will only respond to properly formed requests against valid fields.
Suggestion/Search/Keyword Fields	Filter Fields	Ordering Fields
labor_category	education_level	labor_category
vendor_name	experience_range	current_price
idv_piid	min_years_experience	education_level
 	price_range	keywords
 	current_price	certifications
 	worksite	min_years_experience
 	business_size	vendor_name
 	security_clearance	schedule
 	sin	 
 	category	 
 	subcategory	 
API Examples
Suggestions
Suggestions are useful for retrieving actual values contained within the CEILINGRATES data set.
It’s useful to pair these suggestions within your search= API calls.
Suggest (Legacy)
Note

Think, begins with…
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest=labor_category:co https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest=vendor_name:te https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest=idv_piid:47q

Multiple Suggestions
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest=labor_category:co&suggest=vendor_name:te&suggest=idv_piid:47q

Suggest-Contains (Recommended)
Note

Think, should contain…
Does not support submission of multiple suggesters at once.
Two character minimum
Labor Category
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=labor_category:chief https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=labor_category:sys https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=labor_category:pr

Vendor Name
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=vendor_name:adv https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=vendor_name:group,

Contract Numbers
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=idv_piid:012 https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=idv_piid:f02 https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?suggest-contains=idv_piid:20

Exact Match Search
Note

Think, exact match
Labor Category
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=labor_category:Engineer+II&page=1&page_size=100

Vendor Name
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=vendor_name:Management+Consulting,+Inc.&page=1&page_size=100

Contract Numbers
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=idv_piid:GS10F0303V&page=1&page_size=100

Keyword Search
Note

Think, wildcard
Keyword search for partial strings (two character minimum)
Keyword searching looks at the following fields:
labor_category
vendor_name
idv_piid
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&keyword=soft https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&keyword=king https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&keyword=f00

Filtering
Note

You can submit one or many filters at once
You can combine filters with search or keyword API calls
Single filter
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=education_level:BA

Many filters
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=200&filter=education_level:BA|HS&filter=price_range:10,30&filter=experience_range:3,40

education_level
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=education_level:MA

experience_range
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=experience_range:25,40

min_years_experience
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=min_years_experience:12

price_range
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=price_range:10,80

current_price
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=current_price:29.62

worksite
possible values: contractor, customer, both

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=worksite:Contractor

business_size
possible values: S, O
S=Small Business
O=Other than Small Business
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=business_size:S

security_clearance
possible values: yes, no
yes, will pull all variations of ‘yes’
no, will pull all variations of ‘no’
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=security_clearance:yes

sin
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=sin:541330ENG

category
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=category:Transportation%20and%20Logistics%20Services

subcategory
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?page=1&page_size=100&filter=subcategory:Testing%20and%20Analysis

Searching and Filtering
Search + Filters
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=labor_category:Project+Manager+II&page=1&page_size=100&filter=education_level:BA|HS|MA&filter=price_range:60,130&filter=experience_range:3,40&filter=business_size:S&filter=site:customer

Keyword + Filters
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=Project&page=1&page_size=100&filter=education_level:BA&filter=price_range:60,130&filter=experience_range:3,40&filter=business_size:S&filter=site:customer&filter=security_clearance:no

Ordering
Note

Default order is ascending on current_price
You can sort by multiple fields
Parameters should be passed in pairs with ordering first, then sort second
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=project&page=1&page_size=300&ordering=labor_category&sort=asc

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=project&page=1&page_size=300&ordering=vendor_name&sort=asc

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=project&page=1&page_size=300&ordering=education_level&sort=desc

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=project&page=1&page_size=300&ordering=min_years_experience&sort=desc

Ordering with Multiple Fields
The API will process field and sort(asc/desc) based on the order the parameters are sent

1	2
&ordering=performance_state&sort=desc	&ordering=performance_city&sort=asc
&ordering=performance_state&sort=desc&ordering=performance_city&sort=asc

Examples

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=labor_category:Engineer+II&page=1&page_size=100&ordering=education_level&sort=asc&ordering=current_price&sort=desc

https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=project&page=1&page_size=300&ordering=min_years_experience&sort=desc&ordering=vendor_name&sort=desc

Excluding
Note

Pass in records to exclude by separating them with a pipe |
Use the _id field from a specific record ` “_id”: “6340611”,` to exclude it from results
The excluded row is simply omitted from the result set, it is not deleted.
Since the excluded rows are not part of the result set returned, they are also not a part of any calculations or aggregations.
Since the excluded rows are not part of the result set returned, they will not be included in any exported file.
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=idv_piid:GS10F0303V&page=1&page_size=100&exclude=6275099|6275111|6275123

Exporting
Note

Export results to a CSV file
add &export=y to any API call
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?search=idv_piid:GS10F0303V&page=1&page_size=100&exclude=6275099|6275111|6275123&export=y

Pagination
Note

page and page_size should be passed in every api call
https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=king&page=1&page_size=20 https://api.gsa.gov/acquisition/calc/v3/api/ceilingrates/?keyword=king&page=8&page_size=50

Aggregations
Note

Aggregations are returned with every API call
They reflect the counts of respective data within the current query result set
They are useful to create menu filtering options
"aggregations": {
    "labor_category": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
            {
                "key": "Driver",
                "doc_count": 4
            },
            {
                "key": "ADMINISTRATOR, PROPERTY, LEVEL 1  ",
                "doc_count": 2
            },
            {
                "key": "General Clerk II",
                "doc_count": 2
            },
            {
                "key": "Accounting Clerk III",
                "doc_count": 1
            },
            {
                "key": "Admin Assistant",
                "doc_count": 1
            },
            {
                "key": "Customer Service Manager",
                "doc_count": 1
            },
            {
                "key": "Customer Service Representative - Senior",
                "doc_count": 1
            },
            {
                "key": "Tire Repairer",
                "doc_count": 1
            },
            {
                "key": "Truckdriver, Tractor-Trailer",
                "doc_count": 1
            }
        ]
    },
    "security_clearance": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
            {
                "key": "No",
                "doc_count": 32
            },
            {
                "key": "As Required",
                "doc_count": 2
            },
            {
                "key": "N/A",
                "doc_count": 1
            },
            {
                "key": "None",
                "doc_count": 1
            },
            {
                "key": "Yes",
                "doc_count": 1
            }
        ]
    },
    "worksite": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
            {
                "key": "Both",
                "doc_count": 41
            },
            {
                "key": "Customer Site",
                "doc_count": 7
            },
            {
                "key": "Customer",
                "doc_count": 6
            },
            {
                "key": "Contractor Facility",
                "doc_count": 3
            },
            {
                "key": "Customer Facility",
                "doc_count": 3
            }
        ]
    },
    "min_years_experience": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
            {
                "key": "3",
                "doc_count": 28
            },
            {
                "key": "5",
                "doc_count": 18
            },
            {
                "key": "4",
                "doc_count": 6
            },
            {
                "key": "10",
                "doc_count": 4
            },
            {
                "key": "7",
                "doc_count": 1
            }
        ]
    },
    "education_level": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
            {
                "key": "HS",
                "doc_count": 33
            },
            {
                "key": "BA",
                "doc_count": 18
            },
            {
                "key": "AA",
                "doc_count": 9
            }
        ]
    },
    "wage_histogram": {
        "buckets": [
            {
                "min": 19.65999984741211,
                "key": 19.69499969482422,
                "max": 19.729999542236328,
                "doc_count": 2
            },
            {
                "min": 20.780000686645508,
                "key": 20.780000686645508,
                "max": 20.780000686645508,
                "doc_count": 1
            },
            {
                "min": 22.06999969482422,
                "key": 22.06999969482422,
                "max": 22.06999969482422,
                "doc_count": 1
            },
            {
                "min": 22.6299991607666,
                "key": 22.759999593098957,
                "max": 22.959999084472656,
                "doc_count": 3
            },
            {
                "min": 23.8700008392334,
                "key": 23.8700008392334,
                "max": 23.8700008392334,
                "doc_count": 3
            },
            {
                "min": 24.489999771118164,
                "key": 24.641666730244953,
                "max": 24.940000534057617,
                "doc_count": 6
            },
            {
                "min": 25.75,
                "key": 25.82599983215332,
                "max": 25.920000076293945,
                "doc_count": 5
            },
            {
                "min": 26.15999984741211,
                "key": 26.34799995422363,
                "max": 26.530000686645508,
                "doc_count": 5
            },
            {
                "min": 26.899999618530273,
                "key": 27.018749952316284,
                "max": 27.25,
                "doc_count": 8
            },
            {
                "min": 27.459999084472656,
                "key": 27.610000133514404,
                "max": 27.780000686645508,
                "doc_count": 4
            },
            {
                "min": 28.010000228881836,
                "key": 28.495384509746845,
                "max": 28.889999389648438,
                "doc_count": 13
            },
            {
                "min": 29.360000610351562,
                "key": 29.720000161064995,
                "max": 29.969999313354492,
                "doc_count": 9
            }
        ]
    },
    "current_price": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
            {
                "key": "27.00",
                "doc_count": 6
            },
            {
                "key": "23.87",
                "doc_count": 3
            },
            {
                "key": "25.82",
                "doc_count": 3
            },
            {
                "key": "28.76",
                "doc_count": 1
            },
            {
                "key": "28.89",
                "doc_count": 1
            },
            {
                "key": "29.36",
                "doc_count": 1
            },
            {
                "key": "29.97",
                "doc_count": 1
            }
        ]
    },
    "business_size": {
        "doc_count_error_upper_bound": 0,
        "sum_other_doc_count": 0,
        "buckets": [
            {
                "key": "S",
                "doc_count": 52
            },
            {
                "key": "O",
                "doc_count": 8
            }
        ]
    },
    "median_price": {
        "values": {
            "50.0": 27.0
        }
    },
    "wage_stats": {
        "count": 60,
        "min": 19.65999984741211,
        "max": 29.969999313354492,
        "avg": 26.58933334350586,
        "sum": 1595.3600006103516,
        "sum_of_squares": 42803.63203610231,
        "variance": 6.401219616299446,
        "variance_population": 6.401219616299446,
        "variance_sampling": 6.509714864033335,
        "std_deviation": 2.530063164488082,
        "std_deviation_population": 2.530063164488082,
        "std_deviation_sampling": 2.5514142870246173,
        "std_deviation_bounds": {
            "upper": 31.649459672482024,
            "lower": 21.529207014529696,
            "upper_population": 31.649459672482024,
            "lower_population": 21.529207014529696,
            "upper_sampling": 31.692161917555094,
            "lower_sampling": 21.486504769456626
        }
    }
}
HTTP Response Codes
The API will return one of the following responses:

HTTP Response Code	Description
200	Successful. Data will be returned in JSON format.
4XX	Additional 400-level are caused by some type of error in the information submitted.