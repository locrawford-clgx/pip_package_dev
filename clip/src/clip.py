import os 
import json 
import requests 
import pandas as pd 
from datetime import datetime, timedelta 

class Clip:
    def __init__(
        self,
        token_credentials: str = None,
        authorization_url: str = 'https://api-uat.corelogic.com/edgemicro-auth-clip/token?grant_type=client_credentials',
        clip_lookup_url: str = 'https://clip-lookup-uat.solutions.corelogic.com',
        clip_batch_url: str = 'https://clip-batch-uat.solutions.corelogic.com'
    ):
        '''
            Initializes an instance of the Clip class.
            
            Parameters:
                token_credentials (str): The token credentials for authorization. Default is None.
                authorization_url (str): The URL for obtaining the bearer token. Default is the UAT authorization URL.
                clip_lookup_url (str): The URL for the CLIP lookup service. Default is the UAT lookup URL.
                clip_batch_url (str): The URL for the CLIP batch service. Default is the UAT batch URL.
        '''
        self.bearer_token = os.getenv("__bearerToken")
        self.expires_in_time = os.getenv("__expiresInTime")
        self.token_timestamp = os.getenv("__tokenTimestamp")
        self.clip_batch_url = os.environ.get("clipBatchUrl", clip_batch_url)
        self.clip_lookup_url = os.environ.get("clipLookupUrl", clip_lookup_url)
        self.token_credentials = os.environ.get("tokenCredentials", token_credentials)
        self.authorization_url = os.environ.get("authorizationUrl", authorization_url)

        # Set a default value for expires_in_time if it is None
        if self.expires_in_time is None:
            self.expires_in_time = 300000


    def _refresh_token(
        self
    ):
        ''' 
            Description:
                This function is responsible for refreshing the token used for authorization in the Clip class. 
                It sends a POST request to the authorization URL provided and updates the necessary token-related 
                information in the environment variables and instance variables.

            Parameters:
                self: The instance of the Clip class.

            Exceptions:
                If there is an error while refreshing the token or accessing the authorization URL, an exception 
                is raised and an error message is printed.
            
            Return Value:
                This function does not return any value.

            Usage:
                You do not need to call this function directly. It is automatically invoked by other methods in 
                the Clip class when the token has expired or needs refreshing.
        '''
        try:
            response = requests.post(
                self.authorization_url, 
                headers = {
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                    "Authorization": self.token_credentials
                }
            )

        except Exception as e:
            print(f"ERROR: Refreshing token, verify the host name '{self.authorization_url}' and port 443 are correct and accessible: {e}")
        
        try:
            response_json = response.json()

            # Update the environment variables with the new token information
            os.environ["__bearerToken"] = response_json.get("access_token")
            os.environ["__tokenTimestamp"] = datetime.now().isoformat()

            if response_json.get("expires_in"):
                self.expires_in_time = response_json.get("expires_in") * 1000

            os.environ["__expiresInTime"] = str(self.expires_in_time)
            self.bearer_token = os.getenv("__bearerToken")
        except Exception as e:
            print(f"ERROR: Configuring internal parameters, ensure the proper libraries are installed.: {e}")



    def get_bearer_token(
        self
    ):
        '''
            Retrieves the bearer token for authentication.

            Returns:
                str: The bearer token for authentication.

            Raises:
                Exception: If there is an error comparing existing bearer token parameters.
        '''
        try:
            # Check if the current token has expired or needs refreshing
            if self.token_timestamp:
                token_date = datetime.fromisoformat(self.token_timestamp)
            else:
                token_date = datetime(2010, 1, 1)

            if datetime.now() - token_date >= timedelta(milliseconds=int(self.expires_in_time)):
                self._refresh_token()

            return self.bearer_token
        except Exception as e:
            print(f"ERROR: Failed comparing existing Bearer Token parameters: {e}")


    def lookup(
        self, 
        legacy_county_source: str = None, 
        best_match: str = None, 
        google_fallback: str = None, 
        apn: str = None, 
        address: str = None, 
        city: str = None, 
        state: str = None, 
        zip_code: str = None, 
        latitude: str = None, 
        longitude: str = None, 
        owners: str = None,
        clip: str = None,
        convert: bool = True,
    ):
        '''
            Description:
                This method is used to perform a lookup in the CLIP (CoreLogic Integrator Portal) API. It sends a 
                GET request to the CLIP lookup endpoint with the specified parameters and returns the response.

            Parameters:
                self: The instance of the Clip class.
                legacy_county_source (optional): A string representing the legacy county source.
                best_match (optional): A string representing the best match value.
                google_fallback (optional): A string representing the Google fallback value.
                apn (optional): A string representing the APN (Assessor's Parcel Number).
                address (optional): A string representing the address.
                city (optional): A string representing the city.
                state (optional): A string representing the state.
                zip_code (optional): A string representing the ZIP code.
                latitude (optional): A string representing the latitude.
                longitude (optional): A string representing the longitude.
                owners (optional): A string representing the owners.
                clip (optional): A string representing the CLIP value.
                convert (optional): A boolean indicating whether to convert the CLIP response to a DataFrame. 
                    Default is True.

            Returns:
                The function returns the CLIP response as either a DataFrame (if convert is True) or a JSON object.

            Example:
                # Create an instance of the Clip class and perform a lookup
                Clip().lookup(
                    legacy_county_source=True,
                    best_match=True,
                    google_fallback=False,
                    apn="",
                    address="501 Auburn Avenue NE",
                    city="Atlanta",
                    state="GA",
                    zip_code="30312",
                    latitude="",
                    longitude="",
                    owners="",
                    clip="",
                    convert=True
                )   
        '''
        # Send the GET request
        try:
            response = requests.get(
                url = f"{self.clip_lookup_url}/search", 
                headers = {
                    "Authorization": f"Bearer {self.get_bearer_token()}"
                }, 
                params = {
                    "legacyCountySource": legacy_county_source,
                    "bestMatch": best_match,
                    "googleFallback": google_fallback,
                    "apn": apn,
                    "address": address,
                    "city": city,
                    "state": state,
                    "zipCode": zip_code,
                    "latitude": latitude,
                    "longitude": longitude,
                    "owners": owners,
                    "clip": clip,
                }
            )
        except Exception as e:
            print(f"ERROR: GET request failed, verify the host name '{self.clip_lookup_url}' and port 443 are correct and accessible: {e}")
        
        if convert:
            try:
                return pd.DataFrame(response.json()['data'])
            except Exception as e:
                print(f"ERROR: Converting CLIP response to dataframe: {e}")
        else: 
            return response.json()
