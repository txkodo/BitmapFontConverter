from defcon.objects.contour import Contour
import numpy
from sub.graph import DotGridGraph
from PIL.Image import Image
import defcon

def unpackArg(func):
  def inner(self,arg):
    return func(self,*arg)
  return inner

class McGlyph:
  
  @unpackArg
  def __init__(self:'McGlyph',char:str,matrix:tuple[int,int,int,int,int,int],img:Image,domain:tuple[int,int]=None) -> None:
    self.char = char
    self.matrix = matrix
    self.domain = domain
    self.img = img
    self.state = 'init'

  def export(self) -> tuple[list[Contour], int]:
    self._calculate()
    self._operateMatrix()
    return self._exportContours()

  def _calculate(self):
    assert self.state == 'init'
    self.state = 'calculated'
    img = self.img if self.domain is None else self.img.crop((self.domain[0],0,self.domain[1],self.img.height))

    gridGlaph = DotGridGraph(img.width,img.height)
    # try:
    imgArray = numpy.asarray(img)
    # except SystemError as e:
    #   print(f'>>>{self.char}<<<::{ord(self.char):0x}::{(self.domain[0],0,self.domain[1],self.img.height)}\n')
    #   raise e

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

    def operate(coord:tuple[int,int]):
      x,y = coord
      return [a*x+b*y+dx,c*x+d*y+dy]

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