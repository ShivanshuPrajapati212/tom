
# I have to do this .
while True:
    collect_inputs()  
    update_memory()  # im here
    update_world_state()
    reason()
    plan()
    act()
    sleep(very_short_interval)
