import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # Will be set when saved to the database

    @classmethod
    def create_table(cls):
        # Create the dogs table if it doesn't exist
        conn = sqlite3.connect('dogs.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        # Drop the dogs table if it exists
        conn = sqlite3.connect('dogs.db')
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS dogs')
        conn.commit()
        conn.close()

    def save(self):
        # Save the dog instance to the database
        conn = sqlite3.connect('dogs.db')
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
            self.id = cursor.lastrowid
        else:
            cursor.execute('UPDATE dogs SET name = ?, breed = ? WHERE id = ?', (self.name, self.breed, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, breed):
        # Create a new Dog instance and save it to the database
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        # Create a Dog instance from a database row
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        # Retrieve all dogs from the database
        conn = sqlite3.connect('dogs.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dogs')
        rows = cursor.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        conn.close()
        return dogs

    @classmethod
    def find_by_name(cls, name):
        # Find a dog by name
        conn = sqlite3.connect('dogs.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        # Find a dog by ID
        conn = sqlite3.connect('dogs.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM dogs WHERE id = ?', (dog_id,))
        row = cursor.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    def update(self):
        # Update the dog's information in the database
        self.save()

    # Bonus methods (uncomment to use)

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    # Overriding the __str__ method for a nice string representation
    def __str__(self):
        return f'Dog(id={self.id}, name="{self.name}", breed="{self.breed}")'
