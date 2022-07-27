CREATE TABLE books (id serial PRIMARY KEY,
                                 title varchar (150) NOT NULL,
                                 author varchar (50) NOT NULL,
                                 pages_num integer NOT NULL,
                                 review text,
                                 date_added date DEFAULT CURRENT_TIMESTAMP);


INSERT INTO books (title, author, pages_num, review)
            VALUES (%s, %s, %s, %s),
            ('A Tale of Two Cities',
             'Charles Dickens',
             489,
             'A great classic!')
            )