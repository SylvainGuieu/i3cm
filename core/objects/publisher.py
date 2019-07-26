
def publish(obj, publisher):
    try:
        m = getattr(obj, "__str_%s__"%publisher.name)
    except AttributeError:
        return publisher.write(obj)         
    return m(publisher)    

class ASCII:
    tab_str = "  "
    level = 0
    name = "ascii"
    def __init__(self, level=0, tab_str="  "):
        self.level = level
        self.tab_str = tab_str
        
    def child(self, **kwargs):
        kwargs.setdefault('level', self.level+1)
        return self.__class__(**kwargs)
    
    def write(self, s):
        return "%s%s"%(self.tab_str*self.level, s)
    
    def write_margin(self, s):
        return s
    
    def header(self, s, sublevel=1): 
        level = sublevel
               
        if level<=1:
            txt = [self.write(s)]
            txt.append(self.write("="*len(txt[0])))
        elif level==2:
            txt = [self.write(s)]
            txt.append(self.write("-"*len(txt[0])))
        else: 
            txt = [self.write("%s%s"%("#"*level, s))]
            txt.append('')
        return '\n'.join(txt)
    