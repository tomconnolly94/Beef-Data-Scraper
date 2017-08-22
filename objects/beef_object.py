class BeefObject:
    
    def __init__(self, title, relevant_actors, content, date, categories):
        
        self.title = title
        self.relevant_actors = relevant_actors
        self.content = content
        self.date = date
        self.categories = categories
        
        print(self.title)
        print(self.relevant_actors)
        print(self.content)
        print(self.date)
        print(self.categories)
        