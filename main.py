import sqlite3


class DatabaseManager:
    def __init__(self, db_name="todos.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_name)
        create_table_command = """
            CREATE TABLE IF NOT EXISTS todo(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed BOOLEAN DEFAULT 0
            );
        """
        c = conn.cursor()
        c.execute(create_table_command)
        conn.commit()
        c.close()

    def add_task(self, task):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO todo(task)
                VALUES(?);
            """, (task,))
            conn.commit()

    def update_task(self, task_id, task, completed):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("""
                UPDATE todo
                SET task = ?, completed = ?
                WHERE id = ?;
            """, (task, completed, task_id))

    def get_all_tasks(self):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT * FROM todo;
            """)
            result = []
            for row in c.fetchall():
                result.append({
                    "id": row[0],
                    "task": row[1],
                    "completed": row[-1]
                })
            return result

    def delete_task(self, task_id):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("""
                DELETE FROM todo
                WHERE id = ?;
            """, (task_id,))


db_manager = DatabaseManager()
# db_manager.add_task("Java homework")
# db_manager.update_task(1, "Python homework", 1)
print(db_manager.get_all_tasks())
