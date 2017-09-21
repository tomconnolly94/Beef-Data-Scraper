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