from datetime import date
import pytest
#import pytest_asyncio

from app.models import (Season, Misconduct)

@pytest.mark.asyncio
@pytest.mark.usefixtures("init_database")
class TestSeasonTable:
    """Test Season Table"""
    def test_season_all(self):
        """Test Query gets correct number of rows"""
        result = self.db.session.query(Season).all()
        assert len(result) == 9

    def test_season_active_true(self):
        """Test to check active, true"""
        result = self.db.session.query(Season).filter_by(name="Soccer").first()
        assert result.active

    def test_season_active_false(self):
        """Test to check active, false"""
        result = self.db.session.query(Season).filter_by(name="Baseball").first()
        assert result.active


if __name__ == '__main__':
    unittest.main()
