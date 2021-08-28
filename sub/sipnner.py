import threading
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Any

class Spinner:
  def __init__(self,func) -> None:
    self.done = False
    self.func = func

  def spinner(self):
    chars = r'/-\|'
    while not self.done:
      for char in chars:
        sys.stdout.write( '\b' + char)
        sys.stdout.flush()
        time.sleep(0.12)
    sys.stdout.write('\b' + ' ' )  # 最後に末尾1文字を空白で書き換える
    sys.stdout.flush()


  def __call__(self, *args: Any, **kwds: Any) -> Any:
    return self.run(*args, **kwds)

  def run(self, *args: Any, **kwds: Any) -> Any:
    with ThreadPoolExecutor(2) as executor:
      executor.submit(self.spinner)
      future = executor.submit(self.func, *args, **kwds)
      result = future.result()
      self.done = True
    return result