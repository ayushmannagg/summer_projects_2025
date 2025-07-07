class connector():

    import mysql.connector

    # engine

    conn = mysql.connector.connect(
        host = 'localhost',
        username = "root",
        password = "Ayush@786",
        database = "SCHOOL"
    )

    cur = conn.cursor()
    cur.execute("insert into contact_us(full_name, age, phone_number, email, message) values('kriss', 20, '38789946464', 'moris@gmail.com', 'this is message from kriss');")

    conn.commit()