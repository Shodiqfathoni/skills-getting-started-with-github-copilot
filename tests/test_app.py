"""
Comprehensive test suite for the Mergington High School Activities API

Uses pytest and FastAPI's TestClient to test all endpoints including:
- GET / (root redirect)
- GET /activities (list all activities)
- POST /activities/{activity_name}/signup (sign up for activity)
- DELETE /activities/{activity_name}/signup (remove from activity)

Tests follow the AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore various art techniques and create your own masterpieces",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills through debates",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["mia@mergington.edu", "liam@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design, build, and program robots for competitions",
            "schedule": "Mondays, 4:00 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Participate in theater productions and improve acting skills",
            "schedule": "Tuesdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["ava@mergington.edu", "jack@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Fridays, 2:00 PM - 3:30 PM",
            "max_participants": 20,
            "participants": ["amelia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the school soccer team and compete in local tournaments",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["ethan@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Practice basketball skills and play friendly matches",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["chloe@mergington.edu"]
        },
        "Photography Club": {
            "description": "Learn photography techniques and participate in photo walks",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["zoe@mergington.edu"]
        },
        "Music Band": {
            "description": "Play instruments and perform in school events",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["leo@mergington.edu"]
        },
        "Math Club": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu"]
        },
        "Book Club": {
            "description": "Read and discuss books from various genres",
            "schedule": "Wednesdays, 2:30 PM - 3:30 PM",
            "max_participants": 14,
            "participants": ["ben@mergington.edu"]
        }
    }
    yield
    # Reset after test
    activities.clear()
    activities.update(original)


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static/index.html"""
        # Arrange
        expected_location = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_location


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint"""
    
    def test_get_all_activities(self, client, reset_activities):
        """Test getting all activities"""
        # Arrange
        expected_activity_count = 14
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == expected_activity_count
        assert "Chess Club" in data
        assert data["Chess Club"]["description"]
        assert data["Chess Club"]["schedule"]
        assert data["Chess Club"]["max_participants"]
        assert data["Chess Club"]["participants"]
    
    def test_activities_contain_required_fields(self, client, reset_activities):
        """Test that each activity has all required fields"""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data
            assert isinstance(activity_data["participants"], list)
    
    def test_activities_have_initial_participants(self, client, reset_activities):
        """Test that initial participant data is present"""
        # Arrange
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        chess_club = data["Chess Club"]
        assert len(chess_club["participants"]) == 2
        for participant in expected_participants:
            assert participant in chess_club["participants"]


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint"""
    
    def test_successful_signup(self, client, reset_activities):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        expected_message = f"Signed up {email} for {activity_name}"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == expected_message
        assert email in activities[activity_name]["participants"]
    
    def test_signup_activity_not_found(self, client, reset_activities):
        """Test signup for non-existent activity"""
        # Arrange
        invalid_activity = "Non Existent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_signup_duplicate_student(self, client, reset_activities):
        """Test signup fails if student already registered"""
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"
    
    def test_signup_activity_full(self, client, reset_activities):
        """Test signup fails when activity is at capacity"""
        # Arrange
        activity_name = "Music Band"  # max 10, has 1 initial
        
        # Fill the activity to capacity
        for i in range(9):
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": f"student{i}@mergington.edu"}
            )
        
        # Act - try to sign up when full
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "overfull@mergington.edu"}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Activity is full"
    
    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """Test multiple different students can sign up for same activity"""
        # Arrange
        activity_name = "Art Club"
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        
        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert
        for email in emails:
            assert email in activities[activity_name]["participants"]
    
    def test_signup_same_student_different_activities(self, client, reset_activities):
        """Test same student can sign up for multiple activities"""
        # Arrange
        email = "versatile@mergington.edu"
        activities_to_join = ["Chess Club", "Art Club", "Programming Class"]
        
        # Act
        for activity in activities_to_join:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert
        for activity in activities_to_join:
            assert email in activities[activity]["participants"]


class TestDeleteEndpoint:
    """Tests for the DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_successful_delete(self, client, reset_activities):
        """Test successful deletion of student from activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])
        expected_message = f"Removed {email} from {activity_name}"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == expected_message
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1
    
    def test_delete_activity_not_found(self, client, reset_activities):
        """Test delete from non-existent activity"""
        # Arrange
        invalid_activity = "Non Existent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_delete_student_not_registered(self, client, reset_activities):
        """Test delete fails for student not registered in activity"""
        # Arrange
        activity_name = "Chess Club"
        unregistered_email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": unregistered_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student not registered for this activity"
    
    def test_delete_then_can_resign(self, client, reset_activities):
        """Test student can resign and then sign up again"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act - Delete
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        
        # Act - Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Assert
        assert email in activities[activity_name]["participants"]
    
    def test_delete_frees_capacity(self, client, reset_activities):
        """Test that deleting a student frees up capacity"""
        # Arrange
        activity_name = "Music Band"  # max 10, has 1 initial
        
        # Fill the activity to capacity
        for i in range(9):
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": f"student{i}@mergington.edu"}
            )
        
        # Act - Try to add when full (should fail)
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "overfull@mergington.edu"}
        )
        assert response.status_code == 400
        assert len(activities[activity_name]["participants"]) == 10
        
        # Act - Delete one student
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": "student0@mergington.edu"}
        )
        assert len(activities[activity_name]["participants"]) == 9
        
        # Act - Now should be able to sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "overfull@mergington.edu"}
        )
        
        # Assert
        assert response.status_code == 200
        assert "overfull@mergington.edu" in activities[activity_name]["participants"]


class TestIntegrationScenarios:
    """Integration tests for realistic usage scenarios"""
    
    def test_complete_signup_flow(self, client, reset_activities):
        """Test complete flow: list activities, signup, verify"""
        # Arrange
        activity_name = "Art Club"
        email = "newmember@mergington.edu"
        
        # Act - Get initial state
        response = client.get("/activities")
        assert response.status_code == 200
        all_activities = response.json()
        initial_participants = len(all_activities[activity_name]["participants"])
        
        # Act - Sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Act - Verify via list endpoint
        response = client.get("/activities")
        updated_activities = response.json()
        
        # Assert
        assert len(updated_activities[activity_name]["participants"]) == initial_participants + 1
        assert email in updated_activities[activity_name]["participants"]
    
    def test_concurrent_signups(self, client, reset_activities):
        """Test multiple concurrent signups work correctly"""
        # Arrange
        activity_name = "Gym Class"  # Has lots of space (30)
        emails = [f"student{i}@mergington.edu" for i in range(10)]
        
        # Act - All signups should succeed
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert - Verify all are registered
        response = client.get("/activities")
        activity = response.json()[activity_name]
        for email in emails:
            assert email in activity["participants"]
    
    def test_activity_data_persistence(self, client, reset_activities):
        """Test that activity data persists across requests"""
        # Arrange
        activity_name = "Art Club"
        new_emails = ["persist1@mergington.edu", "persist2@mergington.edu"]
        
        # Act - Get initial data
        response = client.get("/activities")
        initial = response.json()[activity_name]["participants"].copy()
        
        # Act - Make changes
        for email in new_emails:
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
        
        # Act - Get data again
        response = client.get("/activities")
        updated = response.json()[activity_name]["participants"]
        
        # Assert - Verify initial data is still there plus new data
        for email in initial:
            assert email in updated
        for email in new_emails:
            assert email in updated