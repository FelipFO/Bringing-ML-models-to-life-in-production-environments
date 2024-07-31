from locust import HttpUser, task, between
from locust import events

dog_image = 'dog.jpeg'
class APITestUser(HttpUser):
    wait_time = between(1, 5) 

    @task
    def index_page(self):
        self.client.get("/")

    @task
    def upload_image(self):
        files = {'file': (dog_image, open(dog_image, 'rb'), 'image/jpeg')}
        self.client.post("/", files=files)

    @task
    def predict_image(self):
        files = {'file': (dog_image, open(dog_image, 'rb'), 'image/jpeg')}
        self.client.post("/predict", files=files)

    @task
    def send_feedback(self):
        feedback_data = {
            'filename': dog_image,
            'prediction': 'test_prediction',
            'score': '0.95'
        }
        self.client.post("/feedback", data=feedback_data)

        
    def teardown(self):
       with open("test_results.txt", "w") as file:
            for request_stats in self.environment.stats.entries.values():
                file.write(f"{request_stats.name},{request_stats.num_requests},{request_stats.avg_response_time}\n")
                

