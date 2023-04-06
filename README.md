# WikiRacingBot

This bot finds its way from one Wikipedia page to another through links on in-between pages.

Using the Wikipedia API, the bot finds links on a given page, adds them to the queue if they have not yet been viewed, and continues to review them until it finds a destination in the queue.

The found page-link relationships on the page are added to the PostgreSQL database. Therefore, if a page in the queue has already been reviewed and all its links have been added to the database, then the database records are used to retrieve the next pages. This allows to increase the speed and efficiency in general.

Interaction with the program is based on a Telegram bot that receives source and destination pages, checks whether such pages exist and whether it is possible to get at least one link from the first page, and finally gives the result or a message about the problem.

Here is an example of how the bot works.

![image](https://user-images.githubusercontent.com/89355159/230387141-6d526d05-f238-436c-b133-936a25b54456.png)
