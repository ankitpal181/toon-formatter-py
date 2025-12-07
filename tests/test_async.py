import unittest
import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from toon_parse import AsyncToonConverter

class TestAsyncToonConverter(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_async_json_to_toon(self):
        data = {"name": "Alice", "age": 30}
        
        async def run():
            return await AsyncToonConverter.from_json(data)
            
        toon = self.loop.run_until_complete(run())
        self.assertIn('name: "Alice"', toon)
        self.assertIn('age: 30', toon)

    def test_async_toon_to_json(self):
        toon = 'name: "Alice"\nage: 30'
        
        async def run():
            return await AsyncToonConverter.to_json(toon, return_json=False)
            
        json_data = self.loop.run_until_complete(run())
        self.assertEqual(json_data, {"name": "Alice", "age": 30})

    def test_async_csv_to_toon(self):
        csv_str = "name,age\nAlice,30"
        
        async def run():
            return await AsyncToonConverter.from_csv(csv_str)
            
        toon = self.loop.run_until_complete(run())
        self.assertIn('[1]{name,age}:', toon)

if __name__ == '__main__':
    unittest.main()
