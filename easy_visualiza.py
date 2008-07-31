# -*- coding: utf-8 -*-
from euclid import LineSegment2, Point2
from itertools_recipes import pairwise

def flatten(l):
    r = []
    for i in l:
        if type(i) == type([]):
            r += i
        else:
            r.append(i)
    return r

class Visualiza(object):

    def __init__(self, inicio, elementos):
        '''
        elementos -> [inicio, ... puntos, [puntos],... fin]
        '''
        elementos = elementos[:]
        self.puntos = [Point2(float(x),float(y)) for x,y in flatten(elementos) if (x,y) != inicio]
        self.origen = Point2(float(inicio[0]),float(inicio[1]))
        self.destinos = self.puntos[:]
        #print self.destinos.remove(self.origen)   #No tiene sentido que un punto se vea a si mismo

        self.poligonos = [self.armar_poligono(e) for e in elementos if isinstance(i, list)]
        self.segmentos = list(flatten(self.poligonos))

    def armar_poligono(self, puntos):
        #print "ARMAR POLIGONO:", puntos
        #puntos.append(puntos[0]) # cerrar el poligono
        puntos = [Point2(float(x),float(y)) for x,y in puntos]
        r =[]
        #for p1, p2 in pairwise(puntos):
        #    r.append(LineSegment2(p1,p2))

        #FIXME: segmentos redudantes
        #solo funcionara para figuras convexas
        for p1 in puntos:
            for p2 in puntos:
                if p1 != p2:
                    r.append(LineSegment2(p1,p2))
        return r

    def es_visible(self, destino):
        print self.origen, destino, self.destinos
        segmento1 = LineSegment2(self.origen, destino)
        for segmento2 in self.segmentos:
            r = segmento1.intersect(segmento2)
            if r and r != self.origen and r != destino:
                return False
        return True
    
if __name__ == '__main__':
    '''
    Salida esperada:
    Point2(0.00, 4.00) es visible
    Point2(3.00, 0.00) es visible
    Point2(3.00, 2.00) es visible
    Point2(3.00, 4.00) es visible
    Point2(5.00, 0.00) no es visible
    Point2(5.00, 4.00) no es visible
    Point2(7.00, 2.00) no es visible
    '''
    elementos = [(0,0), (0,4), [(3,0), (3,2), (3,4), (5,4), (5,0)], (7,2)]
    inicios = [(0,0), (3,2), (5,4)]

    for inicio in inicios:
        v = Visualiza(inicio, elementos)

        print "Desde", inicio
        for destino in v.destinos:
            print destino, "es visible" if v.es_visible(destino) else "no es visible"
        print "*"*80
