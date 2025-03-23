import json

from faker import Faker

faker = Faker()

data = [{"id": i, "job": faker.job()[:50]} for i in range(1, 1001)]

with open("bulk_jobs_payload.json", "w") as f:
    json.dump(data, f, indent=2)
