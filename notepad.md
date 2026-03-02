
# I have to do this .
while True:
    collect_inputs()  
    update_memory()  
    update_world_state()
    reason()    
    plan()      # im here
    act()
    sleep(very_short_interval)
