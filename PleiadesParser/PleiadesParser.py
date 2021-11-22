"""
Downloads most recent data from Pleiades and parses data in to Python objects.
Each Pleiades entry is parsed as an object, with helper Classes.
Author: Annie K. Lamar
Version: 1.0 11/21/21
Credits: https://pleiades.stoa.org/ 

Quick Start:
    Make PleiadesGetter
    Run get_pleiades_data()
    Store results in list.
    
For full information from Pleiades JSON file, which may be 
redundant across object attributes or unnecessary, run:
    get_pleiades_data(object_type = 'PleiadesObject')
For reduced and organized information from PLeiades JSON file,
which contains most commonly used attributes, run:
    get_pleiades_data(object_type = 'Pleiad')
By default, this method returns Pleiad objects.

Classes:
    PleiadesGetter
    PleiadesObject
    class BboxContainer
    class GeometryContainer
    class AttestationsContainer
    class NamesContainer
    class Name

Module Functions:
    
    ---Download Data---
    wget_url(string url) -> string
    unzip_gz(string file) -> string
    get_file(string url) -> string
    get_df(string json_file) -> list of dictionaries
    get_data(string url) -> list of dictionaries
    
    ---Pleiades Top-Level Methods---
    get_pleiades_objects(list graph_data) -> list of PleiadesObjects
    get_pleiads(list graph_data) -> list of Pleiads
    get_Pleiades_data(string url) -> list of PleiadesObjects or Pleiads
"""

import wget
import json
import gzip
import shutil
import os

class PleiadesGetter:

    def wget_url (url):
        """
        Downloads the file at the given URL and returns the file name.

        Keyword arguments:
        url -- the URL from which to download the file (required)

        Returns:
        (string) file name of downloaded file
        """
        wget.download(url, url.split("/")[-1])
        return url.split("/")[-1]

    def unzip_gz (file):
        """
        Unzips the provided .gz file and returns the unzipped file.

        Keyword arguments:
        file -- the .gz file (required)

        Returns:
        (string) file name of unzipped file
        """
        new_name = file[:-3]
        with gzip.open(file, 'rb') as f_in:
            with open(new_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        f_in.close(); os.remove(file)
        f_out.close(); return file[:-3]

    def get_file (url):
        """
        Downloads, unzips, and returns the file at the given URL.

        Keyword arguments:
        url -- the URL from which to access the data (required)

        Returns:
        (string) file name
        """
        file = wget_url(url)
        if file.endswith(".gz"):
            file = unzip_gz(file)
        return file

    def get_df (json_file):
        """
        Opens the provided JSON file and loads it into a dataframe.

        Keyword arguments:
        json_file -- string name of JSON file with data to be loaded

        Returns:
        (list) dataset as list of dictionaries
        """
        json_file = open(json_file, "r+", encoding="utf8")
        df = json.load(json_file)
        return df

    def get_data (url):
        """
        Downloads, unzips, and loads the JSON file at the given URL.

        Keyword arguments:
        url -- web location of the JSON file from which to download data

        Returns:
        (list) dataset with JSON file data, list of dictionaries
        """
        return get_df(get_file(url))

    def get_pleiades_objects (graph_data):
        """
        Goes through each JSON object in file and turns it into a PleiadesObject.

        Keyword arguments:
        graph_data -- list of graph_data from JSON file

        Returns:
        (list) list of PleiadesObjects
        """
        pleiads = []
        for row in range(len(graph_data)):
            pleiads.append(PleiadesObject(graph_data[row]))
        return pleiads

    def get_pleiads (graph_data):
        """
        Goes through each JSON object in file and turns it into a Pleiad object.

        Keyword arguments:
        graph_data -- list of graph_data from JSON file

        Returns:
        (list) list of Pleiads
        """
        pleiads = []
        for row in range(len(graph_data)):
            pleiads.append(Pleiad(graph_data[row]))
        return pleiads

    def get_Pleiades_data (url = "http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz", object_type='Pleiad'):
        """
        Acquires most recent Pleiades data dump and parses contents to Python objects.

        Keyword arguments:
        url -- string name of url to download from (default: "http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz")

        Returns:
        (list) list of PleiadesObjects or Pleiad objects.
        """
        df = get_data("http://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz")
        graph_data = df['@graph'] #@graph is a list of dictionaries
        if object_type == 'PleiadesObject':
            pleiads = get_pleiades_objects(graph_data)
        else:
            pleiads = get_pleiads(graph_data)
        return pleiads

####################
#Parse Pleiades JSON
####################
class PleiadesObject:
    """
    A class to represent a Pleiades place. 
    This class contains all attributes from the Pleiades JSON data dump, except:
    -attributes related to content creators
    -attributes related to external scholarship or citations
    
    ---Attributes---
    
    Note that the following four dictionaries may contain redundant information, 
    i.e., multiple PleiadesObjects may hold the same information.
    They are included for each object for ease of access.
    time_periods : dictionary
        contains information about time periods
    confidence_metrics : dictionary
        contains information about confidence_metrics
    association_certainties : dictionary
        contains information about association certainties
    location_types : dictionary
        contains information about location types
        
    Information about the other attributes in the object may be found in the Pleiades documentation:
    https://pleiades.stoa.org/downloads
    
    ---Methods---
    add_time_period (time_period, time_period_uri)
    add_confidence_metric (confidence_metric, confidence_metric_uri)
    add_association_certainty (certainty, certainty_uri)
    add_location_type (self, location_type, location_type_uri)
    """
    #does not include contributers, editing history, references to external scholarship
    def __init__(self, graph_dict):
        #information
        self.time_periods = {}
        self.confidence_metrics ={}
        self.association_certainties = {}
        self.location_types ={}
        #features
        if graph_dict['features'] and graph_dict['features'][0]:
            if graph_dict['features'][0]['geometry']:
                self.features_geometry = GeometryContainer(graph_dict['features'][0]['geometry'])
            if graph_dict['features'][0]['type']:
                self.features_type = graph_dict['features'][0]['type']
            if graph_dict['features'][0]['id']:
                self.features_id = graph_dict['features'][0]['id']
            if graph_dict['features'][0]['properties']:
                self.features_properties = PropertiesContainer(graph_dict['features'][0]['properties'])
        #locations
        if graph_dict['locations'] and graph_dict['locations'][0]:
            if graph_dict['locations'][0]['associationCertainty']:
                self.locations_associationCertainty = graph_dict['locations'][0]['associationCertainty']
                (self.add_association_certainty(self.locations_associationCertainty, 
                                                graph_dict['locations'][0]['associationCertaintyURI']))
            if graph_dict['locations'][0]['attestations']:  
                self.locations_attestations = AttestationsContainer(graph_dict['locations'][0]['attestations'])
                for attestation in range(len(graph_dict['locations'][0]['attestations'])):
                    (self.add_time_period(graph_dict['locations'][0]['attestations'][attestation]['timePeriod'], 
                                          graph_dict['locations'][0]['attestations'][attestation]['timePeriodURI']))
                    (self.add_confidence_metric(graph_dict['locations'][0]['attestations'][attestation]['confidence'], 
                                          graph_dict['locations'][0]['attestations'][attestation]['confidenceURI']))
            if graph_dict['locations'][0]['id']:
                 self.locations_id = graph_dict['locations'][0]['id']
            if graph_dict['locations'][0]['featureTypeURI'] and graph_dict['locations'][0]['featureTypeURI'][0]:
                self.locations_featureTypeURI = graph_dict['locations'][0]['featureTypeURI'][0]
                self.add_location_type(graph_dict['locations'][0]['featureType'][0], self.locations_featureTypeURI)
            if graph_dict['locations'][0]['start']:
                self.locations_start = graph_dict['locations'][0]['start']
            if graph_dict['locations'][0]['end']:
                self.locations_end = graph_dict['locations'][0]['end']
            if graph_dict['locations'][0]['title']:
                self.locations_title = graph_dict['locations'][0]['title']
            if graph_dict['locations'][0]['archaeologicalRemains']:
                self.locations_archaeologicalRemains = graph_dict['locations'][0]['archaeologicalRemains']
            if graph_dict['locations'][0]['details']:
                self.locations_details = graph_dict['locations'][0]['details']
            if graph_dict['locations'][0]['accuracy_value']:
                self.locations_accuracy_value = graph_dict['locations'][0]['accuracy_value']
            if graph_dict['locations'][0]['featureType'] and graph_dict['locations'][0]['featureType'][0]:
                self.locations_featureType = graph_dict['locations'][0]['featureType'][0]
            if graph_dict['locations'][0]['description']:
                self.locations_description = graph_dict['locations'][0]['description']
            if graph_dict['locations'][0]['locationType'] and graph_dict['locations'][0]['locationType'][0]:
                self.locations_locationType = graph_dict['locations'][0]['locationType'][0]
            if graph_dict['locations'][0]['uri']:
                self.locations_uri = graph_dict['locations'][0]['uri']
            if graph_dict['locations'][0]['@type']:
                self.locations_type = graph_dict['locations'][0]['@type']
        #connections
        if graph_dict['connections'] and graph_dict['connections'][0]:
            self.connections = {}
            for item in graph_dict['connections']:
                connections[item['id']] = item['connectionType']
        if graph_dict['names'] and graph_dict['names'][0]:
            self.names = NamesContainer(graph_dict['names'])
        if graph_dict['id']:
             self.id = graph_dict['id'] 
        if graph_dict['subject'] and graph_dict['subject'][0]:
            self.subjects = []
            for subject in graph_dict['subject']:
                self.subjects.append(subject)
        if graph_dict['title']:
             self.title = graph_dict['title'] 
        if graph_dict['provenance']:
             self.provenance = graph_dict['provenance'] 
        if graph_dict['details']:
             self.details = graph_dict['details'] 
        if graph_dict['type']:
             self.type = graph_dict['type'] 
        if graph_dict['uri']:
             self.uri = graph_dict['uri'] 
        if graph_dict['description']:
             self.description = graph_dict['description'] 
        if graph_dict['placeTypes'] and graph_dict['placeTypes'][0]:
            self.place_types = []
            for place_type in graph_dict['placeTypes']:
                self.place_types.append(place_type)
        if graph_dict['bbox'] and graph_dict['bbox'][0]:
            self.bbox = BboxContainer(graph_dict['bbox'])
        if graph_dict['reprPoint'] and graph_dict['reprPoint'][0]:
            self.repr_point = graph_dict['reprPoint']

    def add_time_period (self, time_period, time_period_uri):
        """
        Adds info about a time period to appropriate dictionary.
        
        Keyword arguments:
        time_period -- time period type
        time_period_uri -- Pleiades uri for that time period
        """
        if time_period not in self.time_periods.keys():
            self.time_periods[time_period] = time_period_uri

    def add_confidence_metric (self, confidence_metric, confidence_metric_uri):
        """
        Adds info about a confidence metric to appropriate dictionary.
        
        Keyword arguments:
        confidence_metric -- confidence metric type
        confidence_metric_uri -- Pleiades uri for that confidence metric
        """
        if confidence_metric not in self.confidence_metrics.keys():
            self.confidence_metrics[confidence_metric] = confidence_metric_uri

    def add_association_certainty (self, certainty, certainty_uri):
        """
        Adds info about an association certainty to appropriate dictionary.
        
        Keyword arguments:
        certainty -- certainty type
        certainty_uri -- Pleiades uri for that association certainty
        """
        if certainty not in self.association_certainties.keys():
            self.association_certainties[certainty] = certainty_uri   

    def add_location_type (self, location_type, location_type_uri):
        """
        Adds info about a location type to appropriate dictionary.
        
        Keyword arguments:
        location_type -- location type
        location_type_uri -- Pleiades uri for that location type
        """
        if location_type not in self.location_types.keys():
            self.location_types[location_type] = location_type_uri   

class Pleiad:
    """
    A class to represent a single location from Pleiades.
    
    ---Attributes---
    geometry : GeometryContainer
        Contains info about coordinates and geographic type
    text_id : string
        Text id of the location
    attestations : AttestationsContainer
        Contains info about temporal attestations
    start_date : string
        The minimum date (decimal CE year) of any attested time period.
    end_date : string
        The maximum date (decimal CE year) of any attested time period.
    archaeological_remains : string
        How much archaeological remains are present at the site
    connections : dictionary
        Connections to other Pleiad objects
    names : NamesContainer
        Contains info about attested names for this location
    id : string
        Numeric id of the location
    subjects : list
        List of subjects relevant to the location
    title : string
        Standardized text title
    details : string
        Details about the location
    uri: string
        Stable Pleiades uri for the location
    description : string
        Long description of location
    place_types : list
        List of place types relevant to the location
    bbox : BboxContainer
        Bbox object with max area coordinates
    repr_point : list
        Representative long/lat point
    """
    def __init__(self, graph_dict):
        #features
        if graph_dict['features'] and graph_dict['features'][0]:
            if graph_dict['features'][0]['geometry']:
                self.geometry = GeometryContainer(graph_dict['features'][0]['geometry'])
            if graph_dict['features'][0]['id']:
                self.text_id = graph_dict['features'][0]['id']
        #locations
        if graph_dict['locations'] and graph_dict['locations'][0]:
            if graph_dict['locations'][0]['attestations']:  
                self.attestations = AttestationsContainer(graph_dict['locations'][0]['attestations'])
            if graph_dict['locations'][0]['start']:
                self.start_date = graph_dict['locations'][0]['start']
            if graph_dict['locations'][0]['end']:
                self.end_date = graph_dict['locations'][0]['end']
            if graph_dict['locations'][0]['archaeologicalRemains']:
                self.archaeological_remains = graph_dict['locations'][0]['archaeologicalRemains']
        #connections
        if graph_dict['connections'] and graph_dict['connections'][0]:
            self.connections = {}
            for item in graph_dict['connections']:
                connections[item['id']] = item['connectionType']
        #names
        if graph_dict['names'] and graph_dict['names'][0]:
            self.names = NamesContainer(graph_dict['names'])
        #general
        if graph_dict['id']:
             self.id = graph_dict['id'] 
        if graph_dict['subject'] and graph_dict['subject'][0]:
            self.subjects = []
            for subject in graph_dict['subject']:
                self.subjects.append(subject)
        if graph_dict['title']:
             self.title = graph_dict['title'] 
        if graph_dict['details']:
             self.details = graph_dict['details'] 
        if graph_dict['uri']:
             self.uri = graph_dict['uri'] 
        if graph_dict['description']:
             self.description = graph_dict['description'] 
        if graph_dict['placeTypes'] and graph_dict['placeTypes'][0]:
            self.place_types = []
            for place_type in graph_dict['placeTypes']:
                self.place_types.append(place_type)
        if graph_dict['bbox'] and graph_dict['bbox'][0]:
            self.bbox = BboxContainer(graph_dict['bbox'])
        if graph_dict['reprPoint'] and graph_dict['reprPoint'][0]:
            self.repr_point = graph_dict['reprPoint']
    
    
class BboxContainer:
    """
    A class to parse and organize bbox data.
    
    --Attributes---
    min_longitude : string
        Minimum longitude of a location
    min_latitude : string
        Minimum latitude of a location
    max_longitude : string
        Maximum longitude of a location
    max_latitude : string
        Maximum latitude of a location
    """
    def __init__(self, coordinates):
        self.min_longitude = coordinates[0]
        self.min_latitude = coordinates[1]
        self.max_longitude = coordinates[2]
        self.max_latitude = coordinates[3]

class GeometryContainer:
    """
    A class to parse and organize geometry data.
    
    ---Attributes---
    geom_type : string
        type of geographic location
    coordinates : list
        two item list of latitude, longitude
    """
    def __init__(self, geometry_dict):
        self.geom_type = geometry_dict['type']
        self.coordinates = geometry_dict['coordinates']

class PropertiesContainer:
    """
    A class to parse and organize properties data.
    
    ---Attributes---
    snippet : string
        short description of a place
    link : string
        stable link to Pleiades page
    description : string
        description of a place
    location_precision : string
        how precise of a geographic location this is
    title : string
        formal title of location
    """
    def __init__(self, properties_dict):
        self.snippet = properties_dict['snippet']
        self.link = properties_dict['link']
        self.description = properties_dict['description']
        self.location_precision = properties_dict['location_precision']
        self.title = properties_dict['title']

class AttestationsContainer:
    """
    A class to parse and organize relevant attestation data.
    
    ---Attributes---
    attestations : dictionary
        dictionary of timePeriods (keys) and confidences (values)
    """
    def __init__(self, attestations_list):
        self.attestations = {}
        for attestations_dict in attestations_list:
            self.attestations[attestations_dict['timePeriod']] = attestations_dict['confidence']

class NamesContainer:
    """
    A class to hold a collection of Name objects.
    
    ---Attributes---
    names : list
        list of Name objects
    
    """
    def __init__(self, names_list):
        self.names = []
        for name in range(len(names_list)):
            self.names.append(Name(names_list[name]))

class Name:
    """
    A class to represent a location name.
    
    ---Attributes---
    name_type : string
        name of the location
    transcription_accuracy : string
        accuracy of name as transmitted
    association_certainty : string
        Level of certainty in association between places and locations or names
    romanized_name : string
        Transliteration of the attested name to Roman characters following the
        Classical Atlas Project scheme.
    attestations : AttestationsContainer
        AttestationsContainer object of attestations of this place name
    name_id : string
        id of the name
    transcription_completeness : string
        how complete the transcribed place name is
    language : string
         Short identifier for language and writing system associated with the 
         attested spelling
    description : string
        description of name and source
    name_uri : string
        uri of the name on Pleiades
    name_attested : string
        Attested spelling of ancient name, not necessarily the same as the "title"
    """
    def __init__(self, attributes):
        self.name_type = attributes['nameType']
        self.transcription_accuracy = attributes['transcriptionAccuracy']
        self.association_certainty = attributes['associationCertainty']
        self.romanized_name = attributes['romanized']
        self.attestations = AttestationsContainer(attributes['attestations'])
        self.name_id = attributes['id']
        self.transcription_completeness = attributes['transcriptionCompleteness']
        self.language = attributes['language']
        self.description = attributes['description']
        self.name_uri = attributes['uri']
        self.name_attested = attributes['attested']