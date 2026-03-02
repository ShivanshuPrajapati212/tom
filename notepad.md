
# I have to do this .
while True:
    collect_inputs()  
    update_memory()  
    update_world_state()
    reason()    
    plan()      # not doing 
    act()
    sleep(very_short_interval)
