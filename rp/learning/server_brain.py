from rp.learning.interface import Interface
import rp.optim_server.optim_server.endpoints.worker_endpoints as work_endpoints


class BrainOnline(Interface):
    """ This class replace the interface used define to get the tasks
    from the optimization server """
    def __init__(self, optim_problem="quad_learning"):
        self.id = ""  # id refers to a specific test sample
        self.optim_problem = optim_problem
    
    def next_val_to_test(self):
        """ return the array of parameters to be tested """
        self.id, params = work_endpoints.get_task(self.optim_problem)
        print "...got task params: {}".format(params)
        return params

    def set_result(self, score):
        """ score is a float -> speed...
            send back the results to the server"""

        #score = square_function(params)
        print " ..returned {}".format(score)
        work_endpoints.send_results(self.id, score)

