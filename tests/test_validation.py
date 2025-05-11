import unittest
from validation.validation import is_valid_filename, has_valid_headers, has_duplicate_batch_ids, is_valid_reading

# --- Test 1: Filename Validation ---
class TestFilenameValidation(unittest.TestCase):

    def test_valid_filename(self):
        self.assertTrue(is_valid_filename("MED_DATA_20250425140500.csv"))

    def test_invalid_filename(self):
        self.assertFalse(is_valid_filename("INVALID_FILENAME.csv"))

# --- Test 2: Header Validation ---
class TestHeaderValidation(unittest.TestCase):

    def test_valid_headers(self):
        headers = ["batch_id", "timestamp"] + [f"reading{i}" for i in range(1, 11)]
        self.assertTrue(has_valid_headers(headers))

    def test_invalid_headers(self):
        headers = ["batch", "time", "r1", "r2", "r3"]
        self.assertFalse(has_valid_headers(headers))

# --- Test 3: Batch ID Validation ---
class TestBatchIDValidation(unittest.TestCase):

    def test_no_duplicate_batch_ids(self):
        batch_ids = [1, 2, 3, 4, 5]
        self.assertFalse(has_duplicate_batch_ids(batch_ids))

    def test_with_duplicate_batch_ids(self):
        batch_ids = [1, 2, 2, 3, 4]
        self.assertTrue(has_duplicate_batch_ids(batch_ids))

# --- Test 4: Reading Value Validation ---
class TestReadingValidation(unittest.TestCase):

    def test_valid_reading(self):
        self.assertTrue(is_valid_reading(5.5))
        self.assertTrue(is_valid_reading(0.0))
        self.assertTrue(is_valid_reading(9.9))

    def test_invalid_reading(self):
        self.assertFalse(is_valid_reading(10.0))
        self.assertFalse(is_valid_reading(-1.0))
        self.assertFalse(is_valid_reading("invalid"))

if __name__ == "__main__":
    unittest.main()
