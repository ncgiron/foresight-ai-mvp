from collections import defaultdict, deque

HISTORY = defaultdict(lambda: deque(maxlen=50))