import heapq


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def empty(self):
        return len(self.queue) == 0

    def push(self, data, prio):
        heapq.heappush(self.queue, (data, prio))

    def get(self):
        return heapq.heappop(self.queue)[1]