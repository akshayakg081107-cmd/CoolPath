import unittest
from pathlib import Path
from app.routing import load_network, recommend_routes

ROOT = Path(__file__).resolve().parents[1]

class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.network = load_network(ROOT / "data" / "sample_network.json")

    def test_returns_route(self):
        routes = recommend_routes(self.network, "A", "D")
        self.assertTrue(routes)
        self.assertEqual(routes[0]["nodes"][0], "A")
        self.assertEqual(routes[0]["nodes"][-1], "D")

    def test_route_metrics_are_bounded(self):
        for route in recommend_routes(self.network, "A", "D"):
            self.assertGreater(route["distance_m"], 0)
            self.assertGreaterEqual(route["heat_risk_score"], 0)
            self.assertLessEqual(route["heat_risk_score"], 100)
            self.assertGreaterEqual(route["shade_pct"], 0)
            self.assertLessEqual(route["shade_pct"], 100)

    def test_unknown_node_fails_clearly(self):
        with self.assertRaises(KeyError):
            recommend_routes(self.network, "UNKNOWN", "D")

if __name__ == "__main__":
    unittest.main()
