import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file, encoding="utf-8") as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file, encoding="utf-8") as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Example: Find the longest titles.
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Example: Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    # 指定されたタイトルに対応するページIDを返す
    def find_id_by_title(self, title):
        for page_id, page_title in self.titles.items():
            if page_title == title:
                return page_id
        return None
    
    # A helper function to find a path with cost.
    def find_path_withCost(self, goal_id, previous):
        path = []
        node = goal_id
        path.append(node)
        while previous[node][0] != None:
            node = previous[node][0]
            path.append(node)
        path.reverse()
        return path
    
    
    # A helper function to find a path.
    def find_path(self, goal_id, previous):
        path = []
        node = goal_id
        path.append(node)
        while previous[node] != None:
            node = previous[node]
            path.append(node)
        path.reverse()
        return path


    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        # BFSに工夫を入れる

        start_id = self.find_id_by_title(start)    # 与えられたstartタイトルのpageIDを探す
        goal_id = self.find_id_by_title(goal)      # 与えられた goalタイトルのpageIDを探す
        if start_id == None or goal_id == None:
            print(start_id,"or",goal_id,"のどちらかが存在しません")
            return False

        queue = collections.deque()
        visited = {}    # 既に探索したページを保管するところ
        previous = {}   # 探索するルート

        queue.append(start_id)

        # cost = 0
        visited[start_id] = True
        # previous[start_id] = [None,cost]
        previous[start_id] = None

        while len(queue):
            node = queue.popleft()
            if node == goal_id:
                break
            for child in self.links[node]:
                # cost = previous[node][1] + 1
                if not child in visited:
                    queue.append(child)
                    visited[child] = True
                    # previous[child] = [node,cost]
                    previous[child] = node

        if goal_id in previous:
            ans = self.find_path(goal_id,previous)
            print(" -> ".join(self.titles[item] for item in ans))
        else:
            print("cannot find")
        return True


    # Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        old_page_ranks = {}
        new_page_ranks = {}
        for title_key in self.titles:
            old_page_ranks[title_key] = 1
            new_page_ranks[title_key] = 0

        page_ranks_updated = True

        while page_ranks_updated:
            for title_key in self.titles:   # 新しい辞書を全て0にする
                new_page_ranks[title_key] = 0
            all_rank_share = 0
            # print(old_page_ranks)
            for from_id in self.links:  # 各ページを探索(from_id)して
                if len(self.links[from_id]) != 0:   # 子ノードが存在するとき
                    rank_share = old_page_ranks[from_id]*0.85 / len(self.links[from_id])   # そのノードから隣接ノードに割り振る値を計算
                    all_rank_share += 0.15 * old_page_ranks[from_id]    # 残りの15%を全ノードに分配
                    # print(rank_share,"=" , old_page_ranks[from_id],"/",self.links[from_id])
                    for to_id in self.links[from_id]:   # 各子ノード(to_id)へ
                        new_page_ranks[to_id] += rank_share # 値を割り振る
                else:   # 子ノードがないとき
                    all_rank_share += old_page_ranks[from_id]   # 全てに分配する
            delta = 0   # oldとnewでどれだけ変更があったかを保存
            for key in self.titles:
                new_page_ranks[key] += all_rank_share / len(self.links)  # 全ノードに分配する
                delta += (new_page_ranks[key]-old_page_ranks[key])**2
            
            if delta < 0.01:    # oldとnewで変更が少なければ、ページランクの更新を終わらせる
                page_ranks_updated = False

            old_page_ranks = new_page_ranks.copy() # 古いページランクを新しいものに書き換える
            # print(new_page_ranks)
        
        top_ten = sorted(new_page_ranks, key=new_page_ranks.get, reverse=True)[:10]
        print("Most popular page by PageRank:")
        for page_id in top_ten:
            print(self.titles[page_id],new_page_ranks[page_id])
            
        pass


    # Homework #3 (optional):
    # Search the longest path with heuristics.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_longest_path(self, start, goal):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Helper function for Homework #3:
    # Please use this function to check if the found path is well formed.
    # 'path': An array of page IDs that stores the found path.
    #     path[0] is the start page. path[-1] is the goal page.
    #     path[0] -> path[1] -> ... -> path[-1] is the path from the start
    #     page to the goal page.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def assert_path(self, path, start, goal):
        assert(start != goal)
        assert(len(path) >= 2)
        assert(self.titles[path[0]] == start)
        assert(self.titles[path[-1]] == goal)
        for i in range(len(path) - 1):
            assert(path[i + 1] in self.links[path[i]])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Example
    # wikipedia.find_longest_titles()
    # Example
    # wikipedia.find_most_linked_pages()
    # Homework #1
    wikipedia.find_shortest_path("渋谷", "小野妹子")
    wikipedia.find_shortest_path("A", "F")
    # Homework #2
    wikipedia.find_most_popular_pages()
    # Homework #3 (optional)
    wikipedia.find_longest_path("渋谷", "池袋")
