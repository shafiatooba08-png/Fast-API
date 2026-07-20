from locust import HttpUser, task, between


class LeadUser(HttpUser):

    wait_time = between(1, 3)

    # Paste your JWT token here
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNCIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc4NDU0OTk4M30.HireKgG5H8EGvMjC55QkSuNLpuxLTZjo920mbLiLsBs"

    # Change this to an existing lead ID
    lead_id = 14


    def auth_headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }


    @task(3)
    def get_leads(self):
        """
        Test lead list endpoint
        """

        self.client.get(
            "/leads/?page=1&limit=10",
            headers=self.auth_headers()
        )


    @task(1)
    def update_lead_status(self):
        """
        Test lead status update endpoint
        """

        self.client.patch(
            f"/leads/{self.lead_id}",
            json={
                "status": "qualified"
            },
            headers=self.auth_headers()
        )