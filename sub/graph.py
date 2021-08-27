from pathlib import Path

class GridGraphError(Exception):pass

class GridGraphVertex:
  def __init__(self,coord:tuple[int,int]) -> None:
    self.coord   = coord
    self.outPath = [None,None,None,None]
  
  def __getitem__(self,index):
    return self.outPath[index%4]
  
  def __setitem__(self,index,item):
    self.outPath[index%4] = item


class GridGraphPath:
  def __init__(self,start:GridGraphVertex,end:GridGraphVertex) -> None:
      self.start = start
      self.end = end
      vec = tuple(map(lambda e,s:e-s,end.coord,start.coord))
      self.dirction = [(0,1),(1,0),(0,-1),(-1,0)].index(vec)
      start[self.dirction] = self
      self.enable = True
  
  def disable(self):
    self.enable = False
  
  def __bool__(self):
    return self.enable


class GridGraphCycle:
  def __init__(self,gridGraphPath:GridGraphPath) -> None:
      self.vertices:list[GridGraphVertex] = [gridGraphPath.start]
      self.pathes:list[GridGraphPath] = [gridGraphPath]
      self.closed = False

  def addPath(self,gridGraphPath:GridGraphPath):
    assert self.pathes[-1].end is gridGraphPath.start
    # 曲がっている場合のみ始点を点群に追加
    if self.pathes[-1].dirction != gridGraphPath.dirction:
      self.vertices.append(gridGraphPath.start)
    self.pathes.append(gridGraphPath)
    self.lastPath = gridGraphPath

  def close(self):
    assert self.pathes[0].start == self.lastPath.end
    # 使用したパスを非有効化
    [path.disable() for path in self.pathes]

    # 最初と最後の方向が同じ場合は最初の点を削除
    if self.pathes[0].dirction == self.pathes[-1].dirction:
      self.vertices.pop(0)
    
    self.closed = True
  
  @property
  def length(self):
    return len(self.pathes)

  def exportPoints(self) -> list[tuple[int,int]]:
    assert self.closed
    return [ vertex.coord for vertex in self.vertices]


class GridGraph:
  def __init__(self,xmax,ymax) -> None:
    self.xmax = xmax
    self.ymax = ymax
    self.paths:list[GridGraphPath] = []
    self.verteces:dict[tuple[int,int],GridGraphVertex] = {}

  @property
  def activePaths(self):
    return [ path for path in self.paths if path]

  def __getitem__(self,coord:tuple[int,int]):
    x,y = coord
    assert type(x) is type(y) is int
    assert x <= self.xmax
    assert y <= self.ymax

    if coord not in self.verteces:
      self.verteces[coord] = GridGraphVertex(coord)

    return self.verteces[coord]

  def addPath(self,start:GridGraphVertex,end:GridGraphVertex):
    self.paths.append(GridGraphPath(start,end))

class DotGridGraph(GridGraph):
  def plot(self,x:int,y:int):
    self.addPath(self[x,y],self[x,y+1])
    self.addPath(self[x,y+1],self[x+1,y+1])
    self.addPath(self[x+1,y+1],self[x+1,y])
    self.addPath(self[x+1,y],self[x,y])
  
  # アウトラインの頂点データを取得
  def solve(self):
    cycles:list[GridGraphCycle] = []
    while self.activePaths:
      cycle = self.getClockwizeCycle(self.activePaths.pop(0))
      # 往復するだけのサイクルの場合無視
      if cycle.length == 2:continue
      cycles.append(cycle)
    return [cycle.exportPoints() for cycle in cycles]

  def getClockwizeCycle(self,firstPath:GridGraphPath):
    cycle = GridGraphCycle(firstPath)
    path = firstPath
    # 時計回りで最も近いoutPathを選択
    while True:
      dir = path.dirction
      for i in range(dir-2,dir+2):
        if path.end[i]:
          path = path.end[i]
          break

      if path is firstPath:
        cycle.close()
        return cycle

      cycle.addPath(path)
