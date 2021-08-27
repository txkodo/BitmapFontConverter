import numpy
from sub.graph import DotGridGraph
from PIL.Image import Image
import defcon
from defcon.objects.font import Font
from defcon.objects.glyph import Glyph

def unpackArg(func):
  def inner(self,arg):
    return func(self,*arg)
  return inner

class McGlyph:
  
  @unpackArg
  def __init__(self:'McGlyph',matrix:tuple[int,int,int,int,int,int],img:Image,domain:tuple[int,int]=None) -> None:
    self.matrix = matrix
    self.domain = domain
    self.img = img
    self.state = 'init'

  def export(self):
    self._calculate()
    self._operateMatrix()
    return self._exportContours()

  def _calculate(self):
    assert self.state == 'init'
    self.state = 'calculated'
    img = self.img if self.domain is None else self.img.crop((self.domain[0],0,self.domain[1],self.img.height))

    gridGlaph = DotGridGraph(img.width,img.height)
    imgArray = numpy.asarray(img)

    x,y = 0,0
    for x in range(img.width):
      for y in range(img.height):
        if imgArray[y,x] == 1:
          gridGlaph.plot(x,y)

    result = gridGlaph.solve()
    
    self.height = img.height

    if self.domain:
      self.width = self.domain[1] - self.domain[0]
      self.verteces = result
      return self

    def autoDomain(verteces:list[list[tuple[int,int]]]):
      maxx = max( vertex[0] for path in verteces for vertex in path ) if verteces else 0
      minx = min( vertex[0] for path in verteces for vertex in path ) if verteces else 0
      self.width = maxx - minx
      return [[(vertex[0]-minx,vertex[1]) for vertex in path] for path in verteces]
    self.verteces = autoDomain(result)
    return self

  def _operateMatrix(self):
    assert self.state == 'calculated'
    self.state = 'operated'
    a,b,c,d,dx,dy = self.matrix
    height = self.img.height

    def operate(coord:tuple[int,int]):
      x,y = coord
      return [a*x//height+b*y//height+dx,c*x//height+d*y//height+dy]

    p01 = operate((self.width,0))
    p10 = operate((0,self.height))
    self.width = abs(p01[0]+p10[0])

    self.verteces = [ [ operate(vertex) for vertex in path ] for path in self.verteces]

  def _exportContours(self):
    assert self.state == 'operated'
    self.state = 'exported'

    def getContour(path:list[tuple[int,int]]):
      contour = defcon.Contour()
      for vertix in path:
        contour.appendPoint(defcon.Point(vertix, 'line'))
      return contour

    return [getContour(path) for path in self.verteces], self.width