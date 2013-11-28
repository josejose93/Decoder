from django.db.models import Q
from abc import ABCMeta, abstractmethod

class SearchExpression(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def interpret(self, expr):
        pass

class LeafExpression(SearchExpression):
    
    def interpret(self, expr):
        try:
            field, query = expr.split(':')
            if field.strip() == 'autor':
                return Q(usuario__username__contains = query.strip())
            elif field.strip() == 'titulo':
                return Q(titulo__contains = query.strip())
            return Q()
        except:
            return Q(titulo__contains = expr.strip())

class AndExpression(SearchExpression):

    def interpret(self, expr):
        pos = expr.find(' AND ')
        leafexpr = LeafExpression()
        if pos == -1:
            return leafexpr.interpret(expr)
        else:
            return leafexpr.interpret(expr[:pos]) & self.interpret(expr[pos+4:])


class OrExpression(SearchExpression):

    def interpret(self, expr):
        pos = expr.find(' OR ')
        andexp = AndExpression()
        if pos == -1:
            return andexp.interpret(expr)
        else:
            return andexp.interpret(expr[:pos]) | self.interpret(expr[pos+4:])

