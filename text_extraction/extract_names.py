import nltk

def extract_names(text):
    return_list = []
    
    for sent in nltk.sent_tokenize(text):
        
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            
            if hasattr(chunk, 'label') and chunk.label() == "PERSON":
                
                if ' '.join(c[0] for c in chunk.leaves()) not in return_list:
                    
                    actor.name = ' '.join(c[0] for c in chunk.leaves())
                    actor.db_id = ""
                    
                    return_list.append(actor)

    return return_list