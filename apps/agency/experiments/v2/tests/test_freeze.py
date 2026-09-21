import tempfile
from pathlib import Path
import unittest
from experiments.v2.freeze_candidate import sha, verify

class FreezeTests(unittest.TestCase):
    def test_tokenizer_and_code_tampering_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d); token=folder/'tokenizer.json'; code=folder/'engine.py'
            token.write_text('original tokenizer');code.write_text('original engine')
            record={'checkpoint':d,'checkpoint_files':{'tokenizer.json':sha(token)},'inference_source_files':{str(code):sha(code)}}
            self.assertTrue(verify(record))
            token.write_text('changed tokenizer')
            with self.assertRaises(ValueError):verify(record)
            token.write_text('original tokenizer');code.write_text('changed engine')
            with self.assertRaises(ValueError):verify(record)

if __name__=='__main__':unittest.main()
