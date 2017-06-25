from simplesat.transaction import Operation as SolverOperation


class Operation(object):
    def __init__(self, vim_dir):
        self.vim_dir = vim_dir

    def execute(self, operation):
        if not isinstance(operation, SolverOperation):
            msg = (
                '{0} is not an instance of {1}; '
                '{0} is an instance of {2}'
            ).format(operation, SolverOperation, type(operation))
            raise ValueError(msg)

        self.do_execute(operation)

    def do_execute(self, operation):
        raise NotImplemented
