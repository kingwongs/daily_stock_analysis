# -*- coding: utf-8 -*-
"""
===================================
get_latest_data 测试
===================================

职责：
1. 验证 get_latest_data 方法
2. 测试返回数据按日期降序排列
3. 测试 days 参数限制
"""

import os
import tempfile
import unittest
from datetime import date, timedelta

import pandas as pd

from src.config import Config
from src.storage import DatabaseManager, StockDaily
from data_provider.base import DataFetcherManager


class GetLatestDataTestCase(unittest.TestCase):
    """get_latest_data 方法测试"""

    def setUp(self) -> None:
        """Initialize isolated test database for each case."""
        self._temp_dir = tempfile.TemporaryDirectory()
        self._db_path = os.path.join(self._temp_dir.name, "test_get_latest_data.db")
        os.environ["DATABASE_PATH"] = self._db_path

        Config._instance = None
        DatabaseManager.reset_instance()
        self.db = DatabaseManager.get_instance()

    def tearDown(self) -> None:
        """Cleanup database resources."""
        DatabaseManager.reset_instance()
        self._temp_dir.cleanup()

    def _insert_stock_data(self, code: str, days_ago: int, close: float) -> None:
        """插入测试用股票数据"""
        target_date = date.today() - timedelta(days=days_ago)
        df = pd.DataFrame([{
            'date': target_date,
            'open': close - 1,
            'high': close + 1,
            'low': close - 2,
            'close': close,
            'volume': 1000000,
            'amount': 10000000,
            'pct_chg': 1.5,
        }])
        self.db.save_daily_data(df, code, data_source="TestData")

    def test_get_latest_data_returns_empty_when_no_data(self) -> None:
        """无数据时返回空列表"""
        result = self.db.get_latest_data("999999", days=2)
        self.assertEqual(result, [])

    def test_get_latest_data_returns_correct_count(self) -> None:
        """返回正确数量的数据"""
        # 插入5天数据
        for i in range(5):
            self._insert_stock_data("600519", days_ago=i, close=100.0 + i)

        # 请求2天数据
        result = self.db.get_latest_data("600519", days=2)
        self.assertEqual(len(result), 2)

        # 请求5天数据
        result = self.db.get_latest_data("600519", days=5)
        self.assertEqual(len(result), 5)

    def test_get_latest_data_ordered_by_date_desc(self) -> None:
        """验证数据按日期降序排列"""
        # 插入3天数据
        for i in range(3):
            self._insert_stock_data("600519", days_ago=i, close=100.0 + i)

        result = self.db.get_latest_data("600519", days=3)

        # 验证日期降序（最新日期在前）
        self.assertEqual(len(result), 3)
        self.assertGreater(result[0].date, result[1].date)
        self.assertGreater(result[1].date, result[2].date)

    def test_get_latest_data_filters_by_code(self) -> None:
        """验证按股票代码过滤"""
        # 插入不同股票的数据
        self._insert_stock_data("600519", days_ago=0, close=100.0)
        self._insert_stock_data("000001", days_ago=0, close=50.0)

        result = self.db.get_latest_data("600519", days=5)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].code, "600519")


if __name__ == "__main__":
    unittest.main()


class MarketFetcherPriorityTestCase(unittest.TestCase):
    """Verify Akshare-first policy for market-level fetch calls."""

    def test_market_fetcher_prefers_akshare_first(self) -> None:
        called = []

        class _Fetcher:
            def __init__(self, name: str):
                self.name = name
                self.priority = 0

            def get_main_indices(self, market: str = "US"):
                called.append(self.name)
                return [{"code": "x"}] if self.name == "AkshareFetcher" else None

            def get_market_stats(self, market: str = "US"):
                return None

            def get_sector_rankings(self, n: int = 5, market: str = "US"):
                return None

        manager = DataFetcherManager(
            fetchers=[
                _Fetcher("EfinanceFetcher"),
                _Fetcher("YfinanceFetcher"),
                _Fetcher("AkshareFetcher"),
            ]
        )
        data = manager.get_main_indices(market="US")
        self.assertTrue(data)
        self.assertEqual(called[0], "AkshareFetcher")
