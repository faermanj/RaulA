class Module:
    agent = None
    name = ""
    section = None
        
    
    def __init__(self,agent,name,section):
       self.agent = agent
       self.name = name
       self.section = section
        
    def get_config(self,config_key):
        return self.section[config_key]