class BeefObject:
    
    def __init__(self, title, relevant_actors, content, date, highlights, data_source, categories, img_title, media_link):
        
        self.title = title
        self.relevant_actors = relevant_actors
        self.content = content
        self.date = date
        self.highlights = highlights
        self.data_source = data_source
        self.categories = categories
        self.img_title = img_title
        self.media_link = media_link
        
        
    def print_beef(self):
        
        print(self.title)
        print(self.relevant_actors)
        print("content length: " + str(len(self.content)))
        print(self.date)
        print(self.highlights)
        print(self.data_source)
        print(self.categories)
        print(self.img_title)
        print(self.media_link)

    def get_fields_as_array(self):
        
        return [self.title, self.relevant_actors, self.content, self.date, self.highlights, self.data_source, self.categories, self.img_title, self.media_link]