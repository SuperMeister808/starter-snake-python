
import unittest
from unittest.mock import patch , MagicMock , call , ANY

from logger.emergency_logger import EmergencyLogger

import queue

import threading

import queue
import threading
import unittest
from unittest.mock import patch, MagicMock, call, ANY

from logger.emergency_logger import EmergencyLogger

# Tests that log_worker correctly processes queue entries and respects the is_running flag.
class TestLogWorker(unittest.TestCase):

    def setUp(self):
        EmergencyLogger.setup_runtime_logger("TestLogger", "test.log", False)

        patch.object(EmergencyLogger, "emergency_log", new=MagicMock(wraps=EmergencyLogger.emergency_log)).start()
        patch.object(EmergencyLogger, "flags", new={"is_running": False, "worker_thread": None}).start()
        patch.object(EmergencyLogger, "loger_queue", new=queue.Queue()).start()
        patch.object(EmergencyLogger.runtime_logger, "log").start()
        patch.object(EmergencyLogger, "create_message", side_effect=lambda where, exception: (where, exception)).start()

        self.addCleanup(patch.stopall)
        self.addCleanup(self._stop_worker)

        # test data
        self.entry_1 = ("wherever", "exception", "turn", "level")
        self.entry_2 = ("wherever2", "exception2", "turn2", "level2")

    def _start_worker(self):
        # starts the log worker thread and registers it in flags
        EmergencyLogger.flags["is_running"] = True
        thread = threading.Thread(target=EmergencyLogger.log_worker)
        thread.start()
        EmergencyLogger.flags["worker_thread"] = thread
        return thread

    def _stop_worker(self):
        # signals the worker to stop and waits for it to finish
        EmergencyLogger.flags["is_running"] = False
        thread = EmergencyLogger.flags["worker_thread"]
        if isinstance(thread, threading.Thread):
            thread.join(timeout=2)

    def test_processes_4_element_entries(self):
        # verifies that 4-element queue entries are unpacked and logged correctly
        thread = self._start_worker()

        where, exception, turn, level = self.entry_1
        where_2, exception_2, turn_2, level_2 = self.entry_2

        EmergencyLogger.loger_queue.put(self.entry_1)
        EmergencyLogger.loger_queue.put(self.entry_2)

        self._stop_worker()
        self.assertFalse(thread.is_alive())
        self.assertTrue(EmergencyLogger.loger_queue.empty())
        EmergencyLogger.emergency_log.assert_has_calls([
            call(where, exception, level=level, turn=turn),
            call(where_2, exception_2, level=level_2, turn=turn_2)
        ])

    def test_stops_when_flag_is_set_false(self):
        # verifies that the worker keeps running while is_running is True
        # and stops only after it is set to False
        thread = self._start_worker()

        EmergencyLogger.loger_queue.put(self.entry_1)
        EmergencyLogger.loger_queue.put(self.entry_2)

        # join without stopping — thread should still be alive
        thread.join(timeout=2)
        self.assertTrue(thread.is_alive())
        self.assertTrue(EmergencyLogger.loger_queue.empty())

        self._stop_worker()
        self.assertFalse(thread.is_alive())

    def test_processes_3_element_entries(self):
        # verifies that 3-element queue entries use default level 40
        thread = self._start_worker()

        where, exception, turn, _ = self.entry_1
        where_2, exception_2, turn_2, _ = self.entry_2

        EmergencyLogger.loger_queue.put((where, exception, turn))
        EmergencyLogger.loger_queue.put((where_2, exception_2, turn_2))

        self._stop_worker()
        self.assertFalse(thread.is_alive())
        self.assertTrue(EmergencyLogger.loger_queue.empty())
        EmergencyLogger.emergency_log.assert_has_calls([
            call(where, exception, turn=turn),
            call(where_2, exception_2, turn=turn_2)
        ])

    def test_processes_2_element_entries(self):
        # verifies that 2-element queue entries use default level and unknown turn
        thread = self._start_worker()

        where, exception, _, _ = self.entry_1
        where_2, exception_2, _, _ = self.entry_2

        EmergencyLogger.loger_queue.put((where, exception))
        EmergencyLogger.loger_queue.put((where_2, exception_2))

        self._stop_worker()
        self.assertFalse(thread.is_alive())
        self.assertTrue(EmergencyLogger.loger_queue.empty())
        EmergencyLogger.emergency_log.assert_has_calls([
            call(where, exception),
            call(where_2, exception_2)
        ])

    def test_fallback_on_invalid_entry(self):
        # verifies that invalid queue entries trigger the fallback logger
        thread = self._start_worker()

        EmergencyLogger.loger_queue.put("invalid")
        EmergencyLogger.loger_queue.put("invalid2")

        self._stop_worker()
        self.assertFalse(thread.is_alive())
        self.assertTrue(EmergencyLogger.loger_queue.empty())
        EmergencyLogger.emergency_log.assert_has_calls([
            call("log_worker_fallback", ANY),
            call("log_worker_fallback", ANY)
        ])

    def test_does_not_process_when_flag_is_false(self):
        # verifies that the worker stops immediately when is_running is False
        thread = self._start_worker()

        self._stop_worker()
        self.assertFalse(thread.is_alive())
        self.assertTrue(EmergencyLogger.loger_queue.empty())
        EmergencyLogger.emergency_log.assert_not_called()

    def test_processes_remaining_entries_after_flag_false(self):
        # verifies that entries added just before flag is set False are still processed
        thread = self._start_worker()

        where, exception, _, _ = self.entry_1
        where_2, exception_2, _, _ = self.entry_2

        EmergencyLogger.flags["is_running"] = False
        EmergencyLogger.loger_queue.put((where, exception))
        EmergencyLogger.loger_queue.put((where_2, exception_2))

        self._stop_worker()
        self.assertFalse(thread.is_alive())
        self.assertTrue(EmergencyLogger.loger_queue.empty())
        EmergencyLogger.emergency_log.assert_has_calls([
            call(where, exception),
            call(where_2, exception_2)
        ])

if __name__ == "__main__":

    unittest.main()