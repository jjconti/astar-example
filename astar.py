from copy import deepcopy
from math import sqrt
from euclid import LineSegment2, Point2
from easy_visualiza import Visualiza

class Problema(object):

    def __init__(self, elementos):
        self.inicio = elementos[0]
        self.fin = elementos[-1]
        self.elementos = elementos
        x,y = self.inicio
        pinicio = Point2(float(x), float(y))
        xf, yf = self.fin
        pfin = Point2(float(xf), float(yf))
        self.nodo = Nodo(elementos, pinicio, pfin)
        self.nodos_a_expandir = []

    def meta(self):
        x,y = self.fin
        a = self.nodo.point
        b = Point2(float(x), float(y))
        return a == b 

    def resolver(self):
        while not self.meta():
            nodos = self.nodo.expandir()
            for nodo in nodos:
                if nodo not in self.nodos_a_expandir:
                    self.nodos_a_expandir.append(nodo)
            #self.nodos_a_expandir += nodos
            self.nodos_a_expandir.sort()
            if self.nodos_a_expandir:
                self.nodo = self.nodos_a_expandir.pop(0)
            else:
                print "No se encontro solucion."
                return []
        # Devolver resultado
        r = []
        while self.nodo:
            r.append(self.nodo)
            self.nodo = self.nodo.father
        return reversed(r)
        
class Nodo(object):

    def __init__(self, elementos, point, fin, d=0, father=None):
        '''
        d es la distancia recorrida desde el inicio.
        '''
        #print "CREANDO NODO"
        self.elementos = elementos
        self.v = Visualiza(point, deepcopy(self.elementos))
        self.point = point
        self.fin = fin
        try:
            h = self.point.distance(fin)
        except:
            h = 0
        self.h = h
        self.d = d
        self.father = father

    def pos(self):
        return (self.point.x, self.point.y)

    def __cmp__(self, o):
        return cmp(self.d + self.h, o.d + o.h)

    def __repr__(self):
        return str(self.point)
            def expandir(self):
        r = []
        for des in self.v.destinos:
            #print "DESTINO: ", des
            if self.v.es_visible(des):
                r.append(des)
        return [Nodo(self.elementos, des, self.fin, self.d + self.point.distance(des), father=self) for des in r]

if __name__ == '__main__':
    elementos = [(0,0), (0,4), [(3,0), (3,2), (3,4), (5,0), (5,4)], (7,2)]
    p = Problema(elementos)
    for n in p.resolver():
        print n,
