import unittest
from agent import COURSES, PROFILES, validate_prerequisites


class TestCourseAgent(unittest.TestCase):

    def test_prerequisite_validation_profile_0(self):
        """Test that Mohammad Faraaz Khan (Profile 0) gets eligible courses correctly filtered."""
        profile = PROFILES[0]
        eligible, locked = validate_prerequisites(profile, COURSES)

        # CS101 requires no prereqs, CS102 requires CS101, WEB101 requires CS101
        self.assertIn("CS101", eligible)
        self.assertTrue(isinstance(eligible, list))
        self.assertTrue(isinstance(locked, list))

    def test_prerequisite_validation_profile_1(self):
        """Test that a profile with no known skills only unlocks fundamental courses."""
        profile = PROFILES[1]  # Ananya Sharma (0 known skills)
        eligible, locked = validate_prerequisites(profile, COURSES)

        # Should only unlock CS101 because it has no prerequisites
        self.assertEqual(eligible, ["CS101"])

    def test_courses_structure(self):
        """Validate that course catalog contains required fields."""
        for course in COURSES:
            self.assertIn("id", course)
            self.assertIn("title", course)
            self.assertIn("prerequisites", course)


if __name__ == "__main__":
    unittest.main()