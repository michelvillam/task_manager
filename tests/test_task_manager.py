import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from task_manager.TaskManager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.manager = TaskManager()
        self.manager.FILE_NAME = str(Path(self.temp_dir.name) / "tasks.json")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initial_state(self):
        self.assertEqual(self.manager.tasks, [])
        self.assertEqual(self.manager.next_id, 1)

    def test_add_task_assigns_incrementing_ids_and_saves_tasks(self):
        with redirect_stdout(io.StringIO()):
            self.manager.add_task("First task", "First description")
            self.manager.add_task("Second task", "Second description")

        self.assertEqual(
            [(task.id, task.name, task.description) for task in self.manager.tasks],
            [
                (1, "First task", "First description"),
                (2, "Second task", "Second description"),
            ],
        )
        self.assertEqual(self.manager.next_id, 3)

        with open(self.manager.FILE_NAME, encoding="utf-8") as file:
            saved_tasks = json.load(file)
        self.assertEqual(
            [task["id"] for task in saved_tasks],
            [1, 2],
        )

    def test_delete_task_removes_and_saves_matching_task(self):
        with redirect_stdout(io.StringIO()):
            self.manager.add_task("Keep", "Keep description")
            self.manager.add_task("Delete", "Delete description")
            self.manager.delete_task(2)

        self.assertEqual([task.id for task in self.manager.tasks], [1])
        with open(self.manager.FILE_NAME, encoding="utf-8") as file:
            saved_tasks = json.load(file)
        self.assertEqual([task["id"] for task in saved_tasks], [1])

    def test_delete_unknown_id_keeps_tasks_and_reports_missing_task(self):
        with redirect_stdout(io.StringIO()):
            self.manager.add_task("Existing", "Description")

        output = io.StringIO()
        with redirect_stdout(output):
            self.manager.delete_task(99)

        self.assertEqual([task.id for task in self.manager.tasks], [1])
        self.assertIn("No task found with ID 99.", output.getvalue())

    def test_get_tasks_reports_when_empty(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.manager.get_tasks()

        self.assertIn("No tasks available.", output.getvalue())

    def test_get_tasks_prints_each_task(self):
        with redirect_stdout(io.StringIO()):
            self.manager.add_task("Review", "Review the changes")
        self.manager.tasks[0].mark_completed()

        output = io.StringIO()
        with redirect_stdout(output):
            self.manager.get_tasks()

        self.assertIn("Task: Review", output.getvalue())
        self.assertIn("Description: Review the changes", output.getvalue())
        self.assertIn("Status: Completed", output.getvalue())

    def test_mark_task_completed_updates_and_saves_task(self):
        with redirect_stdout(io.StringIO()):
            self.manager.add_task("Complete me", "Description")

        output = io.StringIO()
        with redirect_stdout(output):
            self.manager.mark_task_completed(1)

        self.assertTrue(self.manager.tasks[0].completed)
        self.assertIn("Task 'Complete me' marked as completed.", output.getvalue())
        with open(self.manager.FILE_NAME, encoding="utf-8") as file:
            saved_task = json.load(file)[0]
        self.assertTrue(saved_task["completed"])

    def test_mark_unknown_id_reports_missing_task(self):
        output = io.StringIO()
        with redirect_stdout(output):
            self.manager.mark_task_completed(99)

        self.assertEqual(self.manager.tasks, [])
        self.assertIn("No task found with ID 99.", output.getvalue())

    def test_load_tasks_restores_tasks_and_next_id(self):
        with redirect_stdout(io.StringIO()):
            self.manager.add_task("Saved task", "Saved description")
        restored_manager = TaskManager()
        restored_manager.FILE_NAME = self.manager.FILE_NAME

        restored_manager.load_tasks()

        self.assertEqual(
            [
                (
                    task.id,
                    task.name,
                    task.description,
                    task.completed,
                )
                for task in restored_manager.tasks
            ],
            [(1, "Saved task", "Saved description", False)],
        )
        self.assertEqual(restored_manager.next_id, 2)

    def test_load_tasks_without_file_starts_with_no_tasks(self):
        self.manager.tasks = [object()]

        self.manager.load_tasks()

        self.assertEqual(self.manager.tasks, [])
        self.assertEqual(self.manager.next_id, 1)


if __name__ == "__main__":
    unittest.main()
