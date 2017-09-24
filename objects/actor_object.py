import json

class ActorObject:
    
    def __init__(self, stage_name, birth_name, nicknames, d_o_b, occupations, origin, achievements, bio, data_sources, associated_actors, links, img_title):
        
        self.stage_name = stage_name
        self.birth_name = birth_name
        self.nicknames = nicknames
        self.d_o_b = d_o_b
        self.occupations = occupations
        self.origin = origin
        self.achievements = achievements
        self.bio = bio
        self.data_sources = data_sources
        self.associated_actors = associated_actors
        self.links = links
        self.img_title = img_title
        
        
    def print_actor(self):
        
        print(self.stage_name)
        print(self.birth_name)
        print(self.nicknames)
        print(self.d_o_b)
        print(self.occupations)
        print(self.origin)
        print(self.achievements)
        print("bio length: " + str(len(self.bio)))
        print(self.data_sources)
        print(self.associated_actors)
        print(self.links)
        print(self.img_title)
        
    def set_stage_name(self, stage_name):
        
        self.stage_name = stage_name
        
    def toJSON(self):
        
        actor_json = {}
        
        actor_json['stage_name'] = self.stage_name
        actor_json['birth_name'] = self.birth_name
        actor_json['nicknames'] = self.nicknames
        actor_json['d_o_b'] = self.d_o_b
        actor_json['occupations'] = self.occupations
        actor_json['origin'] = self.origin
        actor_json['achievements'] = self.achievements
        actor_json['bio'] = self.bio
        actor_json['data_sources'] = self.data_sources
        actor_json['associated_actors'] = self.associated_actors
        actor_json['links'] = self.links
        actor_json['img_title'] = self.img_title
        
        return json.dumps(actor_json)    
    