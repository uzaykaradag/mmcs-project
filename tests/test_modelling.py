import unittest
import pandas as pd
from fraud_detection import modelling as md


class TestModelling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock Transactions Data
        cls.mock_transactions = pd.read_csv('test_data/test_transactions.csv').set_index('transaction_id')

        # Mock Frauds Data
        cls.mock_frauds = pd.read_csv('test_data/test_frauds.csv')

    def test_solve_initial_model(self):
        # Test solve_initial_model function
        results = md.solve_initial_model(self.mock_transactions, {'Utilities': 0.3}, {'Internet': 0.05}, 1000)
        self.assertIsInstance(results, tuple)
        self.assertIsInstance(results[0], list)  # Internal investigations
        self.assertIsInstance(results[1], list)  # External investigations
        self.assertIsInstance(results[2], float)  # Expected value saved

    def test_compute_actual_value_saved(self):
        # Test compute_actual_value_saved function
        fraud_ids = set(self.mock_frauds['transaction_id'])
        total_saved = md.compute_actual_value_saved([2343], [2413], self.mock_transactions, fraud_ids)
        print(total_saved)
        self.assertEqual(total_saved, 0)

        total_saved_no_fraud = md.compute_actual_value_saved([6, 7], [8, 9], self.mock_transactions, set())
        self.assertEqual(total_saved_no_fraud, 0)

    def test_solve_second_model(self):
        # Test solve_second_model function
        fraud_ids = set(self.mock_frauds['transaction_id'])
        results = md.solve_second_model(self.mock_transactions, fraud_ids, 1000)
        self.assertIsInstance(results, tuple)
        self.assertIsInstance(results[0], list)  # Internal investigations
        self.assertIsInstance(results[1], list)  # External investigations
        self.assertEqual(results[2], None)  # Value at stake


if __name__ == '__main__':
    unittest.main()
