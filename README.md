# Rob-GhanaRadio: G-Radio Acquisition Framework (GRAF)

**Rob-GhanaRadio** is a research project dedicated to building a robust neural audio fingerprinting system for high-interference Ghanaian radio broadcasts using joint sound event separation.

This repository contains the **G-Radio Acquisition and Processing Framework (GRAF)** and the **G-Radio Dataset infrastructure**.

---

## Documentation Links

- 📖 **[Operational Guide](OPERATIONAL_GUIDE.md)** - Comprehensive walkthrough on recording radio stations, validation, batch processing, and ML pipeline usage.
- ⚙️ **[Configuration Reference](graf/config.py)** - Environment variables, path management, and defaults.
- 📜 **[G-Radio Metadata Specification (GRMS-1.0)](graf/metadata/models.py)** - Research dataset schema and provenance models.

---

## Quick Command Reference

```bash
# Framework Status & Station List
python3 cli.py info

# Test Recording (30 seconds for Peace FM)
python3 cli.py test-record --station-id peace_fm --duration 30

# Start Continuous Multi-Station Stream Acquisition
python3 cli.py record

# Run QA Segment Validation
python3 cli.py validate

# Run Downstream ML Pipeline
python3 cli.py pipeline

# Run Test Suite
python3 -m unittest discover -s tests -p "test_*.py"
```
