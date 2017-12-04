import ppp_lib
def sum_nested_list(arr, acc):
  while True:
    try:
    
      if len(arr) == 0:
        return acc
    
      sum = 0
      for e in arr[0]:
        if e == -1:
          arr, acc = arr[1:], acc
          raise ppp_lib.tail_call.NextCall
    
        sum += e
      arr, acc = arr[1:], acc+sum
      raise ppp_lib.tail_call.NextCall
    
      break
    except ppp_lib.tail_call.NextCall:
      continue
print(sum_nested_list([[1,1,1],[1,1],[1,1]], 0))
print(sum_nested_list([[1,-1,1],[1,1],[-1,1]], 0))
