IMAGE=summer-break
DOCKERFILE=Dockerfile
CONTAINER=summer-break-app
PORT=5000

HOST_PORT=5000

.PHONY: build
build:
	docker build -f $(DOCKERFILE) . -t $(IMAGE)

.PHONY: test
test:
	docker run -it --rm -w /app $(IMAGE) python3 -m pytest . 

.PHONY: test-coverage
test-coverage:
	docker run -it --rm -w /app $(IMAGE) coverage run -m pytest . && coverage report -m
	
.PHONY: run
run:
	docker run -h 0.0.0.0 -p $(HOST_PORT):$(PORT) -w /app -it --name $(CONTAINER) $(IMAGE) python3 -m uvicorn main:app --reload --host 0.0.0.0 --port $(PORT) 

.PHONY: clean
clean:
	docker stop $(CONTAINER)
	docker rm $(CONTAINER)
	docker rmi $(IMAGE) 
