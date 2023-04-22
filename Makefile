IMAGE=summer-break
DOCKERFILE=Dockerfile
CONTAINER=summer-break-app

NIXOS_IMAGE=summer-break-nixos
NIXOS_DOCKERFILE=NixDockerfile
NIXOS_CONTAINER=nixos-summer-break-app

.PHONY: build
build:
	docker build -f $(DOCKERFILE) . -t $(IMAGE)

.PHONY: test
test:
	docker run -it --rm -w /app $(IMAGE) python3 -m pytest . 
	
.PHONY: run
run:
	docker run -h 0.0.0.0 -p 5001:5001 -w /app -it --name $(CONTAINER) $(IMAGE) python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 5001 

.PHONY: clean
clean:
	docker stop $(CONTAINER)
	docker rm $(CONTAINER)
	docker rmi $(IMAGE) 

.PHONY: build-nixos
build-nixos:
	docker build -f $(NIXOS_DOCKERFILE) . -t $(NIXOS_IMAGE)

.PHONY: run-nixos
run-nixos:
	docker run --name $(NIXOS_CONTAINER) -it $(NIXOS_IMAGE)

.PHONY: clean-nixos
clean-nixos:
	docker rm $(docker stop $(docker ps -a --filter ancestor=$(NIXOS_IMAGE) --format="{{.ID}}"))
	docker rmi $(NIXOS_IMAGE) 

.PHONY: clean-all
clean-all:
	clean clean-nixos
