def display_simu(t):
    """ display the 3d rendering of the seen during t steps"""
    for i in range(t):
        taskMgr.step()
