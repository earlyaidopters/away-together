import unittest
from experiments.v2.generate_final import document_digest,verify_audit_source

class AuditBindingTests(unittest.TestCase):
 def test_reworded_document_invalidates_cached_audit(self):
  docs=[{'id':'one','text':'The pool costs extra.'}]
  audit={'documents_sha256':document_digest(docs),'answers':[{'id':'one'}]}
  verify_audit_source(audit,docs)
  with self.assertRaises(ValueError):verify_audit_source(audit,[{'id':'one','text':'The pool is free.'}])
 def test_duplicate_empty_and_missing_cases_rejected(self):
  with self.assertRaises(ValueError):document_digest([{'id':'one','text':''}])
  with self.assertRaises(ValueError):document_digest([{'id':'one','text':'a'},{'id':'one','text':'b'}])
  docs=[{'id':'one','text':'Terms'}]
  with self.assertRaises(ValueError):verify_audit_source({'documents_sha256':document_digest(docs),'answers':[]},docs)

if __name__=='__main__':unittest.main()
