import heapq

class UrlMaxHeap:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}  # mapping of urls to scores
        self.REMOVED = '<removed-url>'  # placeholder for a removed url
        self.counter = 0  # unique sequence count

    # Function to add a new URL to the heap
    def add_url(self, url, score, depth):
        if url not in self.entry_finder:

            # Create a new entry and add it to the heap and entry finder
            entry = [-score, self.counter, url, depth]
            self.entry_finder[url] = entry
            heapq.heappush(self.heap, entry)
            self.counter += 1

    # Function to remove a URL from the heap
    def remove_url(self, url):
        # Mark an existing entry as REMOVED
        entry = self.entry_finder.pop(url)
        entry[-2] = self.REMOVED
        self.counter -= 1

    # Function to clean up the heap
    def cleanup(self):
        self.heap = [entry for entry in self.heap if entry.url is not self.REMOVED]
        heapq.heapify(self.heap)

    # Function to pop the URL with the highest score
    def pop_url(self):
        while self.heap:
            score, count, url, depth = heapq.heappop(self.heap)
            if url is not self.REMOVED:
                del self.entry_finder[url]
                self.counter -= 1
                return score, url, depth

        raise KeyError('pop from an empty priority queue')

    # Function to update the score of a URL
    def update_score(self, url, new_score):
        self.add_url(url, new_score)