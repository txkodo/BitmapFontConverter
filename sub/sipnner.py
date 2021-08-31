import itertools
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

T = TypeVar('T')
def spinner(func:T):
  running = True

  # runningの間ぐるぐるを表示する
  def spin():
    chars = itertools.cycle(r'/-\|')
    while running:
      sys.stdout.write( '\b' + next(chars))
      sys.stdout.flush()
      time.sleep(0.2)
    sys.stdout.write('\b')
    sys.stdout.flush()

  pallarel:T
  # 並列処理
  def pallarel(*arg,**kwarg):
    nonlocal running
    with ThreadPoolExecutor(2) as executor:
      executor.submit(spin)
      future = executor.submit(func, *arg, **kwarg)
      result = future.result()
      running = False
    return result

  return pallarel