import pandas 
import urllib
import re
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF, SKOS, OWL, RDFS, XSD
from rdflib.namespace import Namespace
from collections import OrderedDict, defaultdict
from countrycode.countrycode import countrycode
import random
import locale
PROV = Namespace('http://www.w3.org/ns/prov#')

import os, binascii
def random_string():
    return binascii.b2a_hex(os.urandom(8)).decode('ascii')

class TagLifter:
    """A class for convering HXL-style tagged data into RDF linked data
    guided by an OWL ontology. Builds an rdflib graph when build_graph method is called.
    
    Arguments:
    ontology - the path to the ontology to use during conversion [Required]
    source - the path to the data file to use during conversion (type determined by file extension) [Required]
    
    Values that can be set:
    
    .limit_rows - useful during debug to limit the number of rows of the data file processed by build_graph()
    
    Currently only csv files are handled
    """
    
    def class_title(self,string):
        return string[0].upper()+string[1:]
        
    
    def clean_string(self,string):
        string = re.sub('[^0-9a-zA-Z]+', '', string)
        return string
    
    def load_data(self,source):
           """Load data from a CSV file"""
           self.source = pandas.read_csv(source)
           self.map_tags()


            
    def load_ontology(self,ontology):
        """
        Load the ontology and set the default namespace
        """
        self.onto = Graph()
        self.onto.parse(ontology, format="xml")
        for prefix, ns in self.onto.namespaces():
            if prefix == "":
                self.ontology_string = str(ns)
                self.ontology = Namespace(ns)
                self.graph.bind("base",ns)
                return True
                
        self.ontology_string = "http://localhost/def/"
        self.ontology = Namespace(self.ontology_string)
            
    
    def map_tags(self):
        """Searches the first 25 rows of the dataset for #tags indicating the contents of a column.
        
        Uses these as column headers where they are available."""
        data = self.source
        mapping = OrderedDict()
        for line, row in data[0:25].iterrows():
            tag_count = 0
            for key in row.keys():
                if str(row[key])[0] == "#":
                    mapping[key] = row[key]
                    tag_count +=1
                else:
                    new_key = self.clean_string(self.class_title(key))
                    mapping[key] = new_key[0].lower()+new_key[1:]
            if tag_count > 3: # We assume we've found the tag row once we've got a row with more than 3 tags in
                #Remove all the rows above
                for rmrow in range(0,line+1):
                    data = data.drop(rmrow)
                break         

        if(tag_count < 2):
            print( "No column tagging found in first 25 rows. Skipping sheet.")
            data = []
        else:
            data = data.rename(columns=mapping)

        data = data.fillna("")
        self.map = data
    
    
    def get_country(self,row,path="#country",return_default = True):
        country = ""
        if path + "+code" in row.keys():
            country = row[path + '+code']
            return country.lower()
        
        if (len(country) < 2) and (path in row.keys()):
            if row.get(path,"xx") in self.country_cache.keys():
                country = self.country_cache[row.get(path,"xx")]
            else:
                country = countrycode(codes=[row.get(path,"")],origin='country_name',target="iso2c")[0]
                if(len(country)==2):
                    self.country_cache[row.get(path,"xx")] = country
                else:
                    country = self.clean_string(row.get(path,"xx")).strip()
                    self.country_cache[row.get(path,"xx")] = country
        else:
            if return_default:
                country = self.default_country
            else:
                country = "unknown"

        return country.lower()
    
    # ToDo - refactor in future 
    def get_country_code_from_name(self,name):
        try:
            country = self.country_cache[name]
        except KeyError:
            country = countrycode(codes=[name],origin='country_name',target="iso2c")[0]
            if(len(country)==2):
                self.country_cache[name] = country
            else:
                country = random_string()
                self.country_cache[name] = country
        
        return country.lower()
        
    def get_language(self,row):
        lang = row.get("#language",default=self.default_language)
        if len(lang) > 1:
            return lang
        else:
            return self.default_language

    def get_tag_type(self,tag):
        if tag in self.type_cache.keys():
            tag_type = self.type_cache[tag]
        else:
            if ( URIRef(self.ontology[self.class_title(tag)]), RDF.type, OWL.Class ) in self.onto:
                tag_type = "Class"
            elif ( URIRef(self.ontology[tag]), RDF.type, OWL.ObjectProperty ) in self.onto:
                tag_type = "ObjectProperty"
            elif ( URIRef(self.ontology[tag]), RDF.type, OWL.DatatypeProperty ) in self.onto:
                tag_type = "DataProperty"
            else: 
                tag_type = "Unknown"
            
            self.type_cache[tag] = tag_type
        return tag_type

    # Check for an def:identifierPattern property attached to any given class
    def get_id_pattern(self,tag):
        if tag in self.id_pattern_cache.keys():
            pattern = self.id_pattern_cache[tag]
        else: 
           pattern = self.onto.value(self.ontology[tag],self.ontology["identifierPattern"]) 
           if(pattern == None):
               pattern = '{random}'
           self.id_pattern_cache[tag] = pattern
        
        return pattern
    
    def generate_identifier(self,row,path,entity_type,country = "xx",lang="en"):
        #1. Check if this entity already has an identifier given in an +identifier column
        # E.g, if path is #project+country, look for #project+company+identifier
        if path + "+identifier" in row.keys():
            if not row[path + "+identifier"].strip() == "":
                return urllib.parse.quote(row[path + "+identifier"].strip(),safe='/')
        
        #2. Check if we have a default language tagged, or non-language tagged, column for this path
        # E.g. If the node found was #project+company+share, and we've been passed #project+company
        # check if #project+company+en or #project+company columns exist to give us a name
        # of the entity to work with
        if path + "+" + lang in row.keys():
            path = path + "+" + lang
        elif path in row.keys():
            path = path
        else: # We had nothing to work with, so generate a random string. 
            return country + "/" + random_string()
        
        #3. Check if we already have an identifier for a thing of this type, and with this name, in the cache
        cache_key = entity_type + self.clean_string(row[path])
        if cache_key in self.id_cache.keys() and len(self.clean_string(row[path]).strip()) > 1:
            return self.id_cache[cache_key]

        pattern = self.get_id_pattern(self.class_title(entity_type))
        
        #4. If not, construct an identifier based on the appropriate pattern
        # ID patterns include
        #  - Country {country} 
        #  - Country from name {country-from-name}
        #  - Random string {random}
        #  - Geographic random string (look for a country column) {country}-{random}
        #  - First and Second Word and random suffix {eyekey}-{suffix}
        #  - Clean string {cleanstring}
        
        if "{country}" in pattern:
            pattern = pattern.replace("{country}",country)
        
        if "{country-from-name}" in pattern:
            pattern = pattern.replace("{country-from-name}",self.get_country_code_from_name(self.clean_string(row[path]).strip()))
        
        if "{random}" in pattern:
            pattern = pattern.replace("{random}",random_string())
        
        if "{eyekey}" in pattern:
            pattern = pattern.replace("{eyekey}",self.generate_eyekey(row[path]))
        
        if "{suffix}" in pattern:
            pattern = pattern.replace("{suffix}",''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(6)))
    
        if "{cleanstring}" in pattern:
            pattern = pattern.replace("{cleanstring}",self.clean_string(row[path]).strip())
            
        identifier = pattern

        self.id_cache[cache_key] = identifier

        return identifier

    def generate_eyekey(self,name):
        """Generates an identifier that is easy to eye-ball and recognise when reading down a list of data

        If the project name is a single word, use the first 4 digits, then a 6 characther random alphanumeric string.
        If the project name is two words, use the first two digits of each word. 

        Uses clean_string to strip non alphanumeric ascii characters before processing. 

        """
        name = name.lower().split(" ")
        if len(name) == 1:
            eyekey = self.clean_string(name[0])[:4]
        else:
            eyekey = self.clean_string(name[0])[:2] + self.clean_string(name[1])[:2]

        return eyekey

    # Create a new entity of a given class (entity_type)
    def create_entity(self,entity_type,path,row,country,lang):
        identifier = self.generate_identifier(row,path,entity_type,country,lang)
        entity = URIRef(self.base+entity_type.lower()+"/"+identifier )
        self.graph.add((entity,RDF.type,self.ontology[self.class_title(entity_type)]))
        return entity 

    def create_metadata(self,meta_data = None):
        """
        Create a meta-data block. 
        
        Mostly uses provenance ontology, with other properties found covered in the local ontology.
        
        """
        if not meta_data:
            meta_data = self.source_meta
        
        entity = URIRef(self.base + "prov/source/" + random_string()) #ToDo - consider whether we should build this off of filename and time?
        self.graph.add((entity,RDF.type,PROV.Entity)) ## ToDo - ****** CORRECT THE ENTITY TYPE HERE *****
        
        for key in meta_data.keys():
            if key == "title":
                pass
            elif key == "source":
                pass
            elif key == "primarySource":
                pass
            elif key == "sourceType":
                pass
            else:
                self.graph.add((entity,self.ontology[key],Literal(meta_data[key])))
        return entity
            

        
    
    def build_graph(self):
        """
        Taking the mapped data in self.map and the ontology, build out a graph.
        
        As we work through the tags, we set:
        
        tag_path - an array of the components of a tag
        current_path - a string to identify the current path
        last_entity - the most recent top-level class we encountered 
        
        We build a cache of known entities in entity_cache identified by their path
        """
        if hasattr(self, 'limit_rows'): # During testing we may wish to only run against a limited number of rows
            data = self.map[0:self.limit_rows]
        else:
            data = self.map
        
        # We need to build the meta-data object.
        source = self.create_metadata()
        
        for line, row in data.iterrows():
            if self.debug:
                print("Processing row " + str(line))
                
            entity_cache = {}
            self.relationship_cache = {} # Reset the relationships cache for each row
            country = self.get_country(row)
            lang = self.get_language(row)
            
            # Add provenance information
            source_row =  URIRef(str(source)+"/row/"+str(line))
            self.graph.add((source_row,RDF.type,self.ontology['SourceRecord']))
            self.graph.add((source_row,PROV.wasDerivedFrom,source)) 
            
            #Set up variables for the first properties we encounter
            entity = source_row
            entity_class = self.ontology["Row"]
            last_entity = entity
            last_class = entity_class
            
            for key in row.keys():

                col_lang = lang
                current_path = ""

                tag_path = key.split("+")
                
                for n in range(len(tag_path)):
                    tag = tag_path[n]
                    if (not tag.isdigit()) and len(tag) > 2: #If this is a digit, or a language tag we skip.
                    
                        current_path += "+"+tag if not current_path == "" else tag
                        if tag[0] == "#":
                            tag = tag[1:]
                    
                        # Check if we are dealing with an entity count
                        if (tag_path[n+1] if len(tag_path) > n+1 else '').isdigit():
                            current_path += "+"+tag_path[n+1]
                            inc = 1
                        else:
                            inc = 0

                        if len((tag_path[n+1+inc] if len(tag_path) > n+1+inc else '')) == 2:
                            col_lang = tag_path[n+1+inc] 
                            inc += 1
                        
                        if(not(row[key]=="")): # Only process when there is a value here
                            tag_type = self.get_tag_type(tag)
                            if tag_type == "Class":
                                # ToDo: Check if it is in the entity cache
                                # print current_path
                                if current_path in entity_cache.keys():
                                    entity = entity_cache[current_path]['entity']
                                    entity_class =  entity_cache[current_path]['class']
                                else:
                                    entity = self.create_entity(tag,current_path,row,country,col_lang)
                                    self.graph.add((entity,PROV.wasDerivedFrom,source_row))
                                    entity_class = self.ontology[self.class_title(tag)]
                                    entity_cache[current_path] = {"entity":entity,"class":entity_class}
                            
                            
                                # Check if we have a name to apply to this column. 
                                # If the language is the same as the default language, or the row language, we use this as the prefLabel
                                if col_lang == self.default_language:
                                    label_rel = SKOS.prefLabel
                                else:
                                    label_rel = SKOS.altLabel
                                if (current_path + "+" + col_lang) in row.keys():
                                    self.graph.add((entity,label_rel,Literal(row[current_path + "+" + col_lang].strip(),lang=col_lang)))
                                elif current_path in row.keys():
                                    self.graph.add((entity,label_rel,Literal(row[current_path].strip(),lang=col_lang)))                                
                            
                                # First check if we can make a relationship between this entity, and it's parent, or nearest neighbour
                                if not last_entity == entity:
                                    relationship = self.seek_class_relationship(last_entity,entity,row,country,lang,source_row)
                                    if relationship:
                                        entity_cache[current_path] = relationship
                                last_entity = entity
                                last_class = self.ontology[self.class_title(tag)]
                            
                                # Now check for other possible relationships: https://github.com/timgdavies/tag-lifter/issues/1

                                possible_relationships = self.check_available_relationships(tag)

                                ###Implementing https://github.com/timgdavies/tag-lifter/issues/1 (but very inefficiently!)
                                # (2) Does a column exist at the next level of depth?
                                for rel in possible_relationships:
                                    search = current_path + "+" + rel[0].lower() + rel[1:]
                                    for skey in row.keys():
                                        if search in skey:
                                            try:
                                                possible_relationships.remove(rel) #If we're going to get to this relationship later, unset it. 
                                            except ValueError:
                                                pass # We might have already removed the element
                                           
                                # (3) Does a column exist at the parent level for these classes?
                                # First, work out the parent node
                                if n == 0:
                                    parent = "#"
                                else:
                                    parent = "+".join(tag_path[0:n]) + "+"
                            
                                # Now iterate through remaining relationships NEEDS TESTING
                                for rel in possible_relationships:
                                    search = parent + rel[0].lower() + rel[1:]
                                    #if not search in entity_cache.keys():
                                    for skey in row.keys():
                                        if search in skey:
                                            try:
                                                possible_relationships.remove(rel)
                                                if search in entity_cache:
                                                    relationship = self.seek_class_relationship(entity,entity_cache[search]['entity'],row,country,lang,source_row)
                                                else: 
                                                    print( search + " has not been created yet, so we can relate to it")
                                            except ValueError:
                                                pass   
                            
                                # (1) Is the entry already created
                            
                            elif tag_type == "ObjectProperty":
                                # We don't handle objectProperties right now.
                                pass
                            
                            elif tag_type == "DataProperty" or tag_type == "Unknown":
                                # We attach any data properties to the previous class in the tag_path, or in the last column if no classes found since then
                                # ToDo: This needs to take more account of data types from the ontology
                                # This needs to also check if we should be attaching to the class, or to a mediating class
                                if len(tag_path) > (1 + n + inc):
                                    print( "Data properties can only be qualified by language tags. " + key + " is an invalid tag.")
                                else:
                                    last_path = "+".join(tag_path[:-1])
                                    try: 
                                        step = entity_cache[last_path]['step']
                                        step_class = entity_cache[last_path]['step_class']
                                    except KeyError:
                                        step = None
                                        step_class = None
                            
                                    # We need to check any restrictions on the data property
                                    # 1. Can it be attached to the class;
                                    # 2. If not, can it be attached to the intermediary (found in the entity cache for the last path?)
                                    # 3. What typing do we need to provide? 
                            
                                    if self.add_data_property(entity,entity_class,self.ontology[tag],row[key]):
                                        pass
                                    elif step and self.add_data_property(step,step_class,self.ontology[tag],row[key]):
                                        pass
                                    else:
                                        if self.allow_extra_properties:
                                            self.graph.add((last_entity,self.ontology["misc/"+tag],Literal(row[key]))) 
                           
    def check_available_relationships(self,source):
          """
          Check what object relationships the current class can stand in, and return a list.
          """
          if source in self.relationship_cache.keys():
              return self.relationship_cache[source]
          else:
              source_class = self.ontology[self.class_title(source)]
              query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
              PREFIX owl: <http://www.w3.org/2002/07/owl#>
              PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
              PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
              SELECT DISTINCT ?t1 ?t2
              WHERE { 
                ?o  a owl:Class. 
                FILTER(?o = <%s>)
                {  
                  ?o rdfs:subClassOf+ ?restriction.
                  ?restriction a owl:Restriction. 
                  ?restriction owl:onProperty ?p1.
                  {
                    {
                      ?restriction owl:someValuesFrom ?t1.
                    } UNION {  
                      ?restriction owl:someValuesFrom ?restrictionClass.
                      ?t1 rdfs:subClassOf+ ?restrictionClass.
                    }
                  }
                }
                OPTIONAL {
                  ?t1 rdfs:subClassOf+ ?restriction2.
                  ?restriction2 a owl:Restriction.
                  ?restriction2 owl:onProperty ?p2.
                  {
                    {
                       ?restriction2 owl:someValuesFrom ?t2.
                    } UNION {
                       ?restriction2 owl:someValuesFrom ?restriction2class.
                       ?t2 rdfs:subClassOf+ ?restriction2class.
                    }
                  }
                }
              }"""%(source_class)
              rels = []
              if query in self.onto_query_cache:
                  q = self.onto_query_cache[query]
              else:
                  q = self.onto.query(query)
                  self.onto_query_cache[query] = q
              for res in q:
                  t1 = str(res['t1']).split("/")[-1]
                  if not t1 in rels:
                      rels.append(t1)
                  if res['t2']:
                      t2 = str(res['t2'].split("/")[-1])
                      if not t2 in rels:
                          rels.append(t2)
              
              self.relationship_cache[source] = rels
              return rels


    def add_data_property(self,subj,subj_class,predicate,value):
        """
        First check if the domain restrictions of the predicate allow it to be attached this subject.
        
        Then check any range restrictions for value typing.
        
        At present, we only pick up Range Restrictions directly attached to properties. 
        
        We are not picking up restrictions that can be inferred through subPropertyOf relationships.
        
        ToDo: Handle for subPropertyOf relationships.
        
        ToDo: Add caching to lookups
        
        We rely on Pandas to cast some values right now...
        
        """
        
        if ((predicate,RDFS.domain,subj_class)) in self.onto:
            predicate_range = self.onto.value(predicate,RDFS.range)
            if predicate_range == XSD.dateTime:
                value = pandas.to_datetime(value)
            elif predicate_range ==XSD.boolean:
                value = True if value else False ## ToDo - improve the handling of Booleans
            elif predicate_range ==XSD.float:
              #  value = str(value).translate(None,['1','2','3','4','5','7','8','9','0','.'])  # ToDo - set-up better replacemnt for errange % signs etc.
                try:
                    value = locale.atof(str(value))
                except ValueError:
                    value = value
            elif predicate_range ==XSD.integer:
              #  value = str(value).translate(None,['1','2','3','4','5','7','8','9','0','.'])
                try:
                    value = locale.atoi(str(value))
                except ValueError:
                    value = value
            self.graph.add((subj,predicate,Literal(value)))
            return True
        else:
            return False
        
  
        

    def seek_class_relationship(self,source,target,row,country,lang,source_row):
        """
        Given two classes, this routine aims to find either a direct relationship that can be made between them,
        or an indirect (one step removed) relationship that can be made.
        
        It then adds the appropriate triples to the graph, including inverse properties if they are available.
        
        Relationships are located based on OWL Restriction classes in the ontology.
        
        At present, the sparql only handles for owl:someValuesFrom - (ToDo: Extend this to include owl:allValuesFrom)
        
        """
        if not source == target:
            cache_key = str(source) + "_"+ str(target)
            if cache_key in self.relationship_cache.keys():
                return self.relationship_cache[cache_key]        
        
            source_class = self.graph.value(source, RDF.type)
            target_class = self.graph.value(target, RDF.type)
        
            rt_cache_key = str(source_class)+"_"+str(target_class)
            if rt_cache_key in self.relationship_cache.keys():
                relationships = self.relationship_cache[rt_cache_key]
            else:
                query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT DISTINCT ?o ?p1 ?t1 ?p2 ?t2 ?restrictionClass ?restriction2class
                WHERE { 
                  ?o  a owl:Class. 
                  FILTER(?o = <%s>)
                  {  
                    ?o rdfs:subClassOf+ ?restriction.
                    ?restriction a owl:Restriction. 
                    ?restriction owl:onProperty ?p1.
                    {
                      {
                        ?restriction owl:someValuesFrom ?t1.
                      } UNION {  
                        ?restriction owl:someValuesFrom ?restrictionClass.
                        ?t1 rdfs:subClassOf+ ?restrictionClass.
                      }
                    }
                  }
                  OPTIONAL {
                    ?t1 rdfs:subClassOf+ ?restriction2.
                    ?restriction2 a owl:Restriction.
                    ?restriction2 owl:onProperty ?p2.
                    {
                      {
                         ?restriction2 owl:someValuesFrom ?t2.
                      } UNION {
                         ?restriction2 owl:someValuesFrom ?restriction2class.
                         ?t2 rdfs:subClassOf+ ?restriction2class.
                      }
                      FILTER(?t2 = <%s>)

                    }
                  }

                }"""%(source_class,target_class)
                
                relationships = {"direct":[],"indirect":[]}
                if query in self.onto_query_cache:
                    q = self.onto_query_cache[query]
                else:
                    q = self.onto.query(query)
                    self.onto_query_cache[query] = q
                for res in q:
                    if res['t1'] == target_class:
                        relationships['direct'].append(res['p1'])
                    if res['t2'] == target_class:
                        relationships['indirect'].append({"p1":res['p1'],"t1":res["t1"],"p2":res["p2"]})
                #ToDo: Add handling to highlight cases of ambiguity (.e.g. when multiple possible direct or indirect relationships)        
                self.relationship_cache[rt_cache_key] = relationships

        
            for rel in relationships['direct']:
                self.graph.add((source,URIRef(rel),target))
                self.add_inverse(source,rel,target)
                self.relationship_cache[cache_key] = {"entity":target,"class":target_class}
                return self.relationship_cache[cache_key] 
        
            for rel in relationships['indirect']:
                # Need to create the entity t1
                # Then need to relate this to source, and to target
                # And return this entity to be written into the cache
                entity_type = rel['t1'].split("/")[-1]
                identifier =  entity_type.lower() + "/" + random_string()
                entity = URIRef(self.base+identifier )
                self.graph.add((entity,RDF.type,rel['t1']))
                self.graph.add((entity,PROV.wasDerivedFrom,source_row))
            
                self.graph.add((source,rel['p1'],entity))
                self.add_inverse(source,rel['p1'],entity) # We add the inverse relationships also
                self.graph.add((entity,rel['p2'],target))
                self.add_inverse(entity,rel['p2'],target) # We add the inverse relationships also
                self.relationship_cache[cache_key] = {"entity":target,"class":target_class,"step":entity,"step_class":rel['t1']}
                return self.relationship_cache[cache_key]

        
    def add_inverse(self,subj,predicate,obj):
        """
        Check for and add inverse relationships.
        
        
        ToDo: Check if caching would be useful here.
        
        """
        for inverse in self.onto.subjects(OWL.inverseOf,predicate):
            self.graph.add((obj,inverse,subj))
        for inverse in self.onto.objects(predicate,OWL.inverseOf):
            self.graph.add((obj,inverse,subj))
        
        

    def __init__(self, ontology = None, source = None, base = "http://localhost/data/",source_meta = None,debug=True):
        self.source_meta = source_meta
        self.debug = debug
        self.country_cache = {}
        self.id_cache = {}
        self.type_cache = {}
        self.relationship_cache = {}
        self.id_pattern_cache = {}
        self.default_language = "en"
        self.default_country = "xx"
        self.allow_extra_properties = True
        self.base = base
        self.graph = Graph()
        self.graph.bind("skos", SKOS)
        self.graph.bind("prov", PROV)
        self.onto_query_cache = {}
        if ontology:
            self.load_ontology(ontology)
        if source:
            self.load_data(source)

