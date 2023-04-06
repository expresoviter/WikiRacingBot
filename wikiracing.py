from typing import List
import requests
from database import *
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class WikiRacer:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:marzipan@localhost/postgres', echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    @staticmethod
    def request(title: str) -> List[str]:
        URL = "https://uk.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "query",
            "titles": title,
            "format": "json",
            "prop": "links",
            "pllimit": "max"
        }
        R = requests.get(url=URL, params=PARAMS)
        DATA = R.json()
        PAGES = DATA["query"]["pages"]
        success=1
        linksList = []
        for k, v in PAGES.items():
            if k != '-1':
                for l in v["links"]:
                    if l["ns"] == 0:
                        linksList.append(l["title"])
            else:
                success=-1
        return linksList,success

    def find_path(self, startTitle: str, endTitle: str) -> List[str]:
        searchTime = datetime.now()
        visited = []
        queue = [startTitle]
        dictionary = {}
        i = 0
        while endTitle not in queue and queue!=[]:
            page = queue[0]
            visited.append(page)
            query = self.session.query(Page).filter(Page.name == queue[0])
            databasePages = query.all()
            currentPage = Page(name=queue[0])
            if not databasePages:
                linksList,success = self.request(page)
                self.session.add(currentPage)
                self.session.commit()
                for j in linksList:
                    query = self.session.query(Link).filter(Link.name == j)
                    databasePages = query.all()
                    if not databasePages:
                        newLink = Link(name=j, nameId=page)
                        self.session.add(newLink)
                self.session.commit()
            else:
                query = self.session.query(Link).filter(Link.nameId == page)
                linksList = [k.name for k in query.all()]

            dictionary[page] = linksList
            finalList = []
            for j in linksList:
                if j not in visited and j not in queue:
                    finalList.append(j)
            queue = queue[1:]
            queue += finalList
            i += 1
            if i == 5000:
                return ["Path is not found"], datetime.now() - searchTime
        path = [endTitle]
        while path[-1] != startTitle:
            for i in dictionary:
                if path[-1] in dictionary[i]:
                    path.append(i)
                    break
        return path[::-1], datetime.now() - searchTime
