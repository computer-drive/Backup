import threading

class ThreadManager:
    def __init__(self):
        self.threads = {}

        self.threads_kinds = {}

    def create_thread(self, name:str,
                      target: callable,
                      args: tuple = (),
                      daemon: bool = False,
                      kinds: str = "normal"):
        
        thread = threading.Thread(name=name, target=target, args=args, daemon=daemon)
        self.threads[name] = thread
        
        if kinds not in self.threads_kinds:
            self.threads_kinds[kinds] = []

        self.threads_kinds[kinds].append(thread)
        
        return thread
    
    
    def get_thread(self, name:str):
        return self.threads.get(name)
    
    def get_threads(self, kinds: str):
        return self.threads_kinds.get(kinds)
    
    def get_all_threads(self):
        return self.threads.values()
    
    def join_threads(self, kinds: str):
        threads = self.threads_kinds.get(kinds)
        if threads is None:
            return
        
        for thread in threads:
            thread.join()

            self.threads_kinds[kinds].remove(thread)
            del self.threads[thread.name]

    def join_all_threads(self):
        for kinds in self.threads_kinds:
            self.join_threads(kinds)


            

    
    
    
