import cmd
import sys
from Google_Drive import Driver


class Database(cmd.Cmd):
    
    driver = str()
    selected = str()
    current_dir = str()
    dir_items = []
    
    def __init__(self):
        super().__init__()
        self.driver = Driver()
        
        for item in self.driver.items(parent_id = ''):
            self.dir_items.append({item['name'] : item})
            
            
                    
    def select(self, name):        
        data = "Item {} Not Found".format(name)
        for item in self.dir_items:
            if name in item.keys():
                self.selected = item[name]
                data = "Item {} Selected".format(name)
                break   
                
        return data
    
    
    def lsdir(self, extension = 'All'):
        
        id = ''
        if self.current_dir: id = self.current_dir['id']
        items_container = self.driver.items(parent_id = id)
        
        list_container = []
        name_container = []
        for item in items_container:
            
            if item['name'].endswith(extension):
                name_container.append(item['name'])
                
            if extension == 'folder' and item['mimeType'].endswith(extension) :
                name_container.append(item['name'])
                
            if extension == 'All':
                name_container.append(item['name'])
                 
            list_container.append({item['name'] : item})
        self.dir_items = list_container
        return name_container
    
    def chdir(self, name):
        response = "Dir {} Not Found".format(name)
        for item in self.dir_items:
            if name in item.keys():
                self.current_dir = item[name]
                response = 'Dir Changed to {}'.format(name)
                break   
                
        return response
    
    def updir(self):
        if 'parents' in self.current_dir:
            self.current_dir = {'id':self.current_dir['parents'][0]}
        else:
            return "No Parent Folder"
    
    #cmd functions
    
        
    def do_lsdir(self, args):
        print(self.lsdir(args))
    
    def do_select(self, args):
        print(self.select(args))
        
    def do_chdir(self, args):
        print(self.chdir(args))
        
    def do_updir(self, args):
        print(self.updir())
        
    
        

if __name__ == "__main__":
    obj = Database()
    obj.cmdloop()