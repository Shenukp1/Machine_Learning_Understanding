#!/usr/bin/env bash

# going to make it to "ml" stage unless "gui" is passed as an argument
MODE="${1:-ml}"

if [[ "$MODE" == "gui" ]]; then
    IMAGE_NAME="ml-assignment:gui"
    TARGET="gui"
else
    IMAGE_NAME="ml-assignment:ml"
    TARGET="ml"
fi

# Build the specific stage (--target) if the image doesn't exist yet
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
    echo "Building $IMAGE_NAME (target: $TARGET)..."
    docker build --target "$TARGET" -t "$IMAGE_NAME" .
fi

# Run the chosen container
if [[ "$MODE" == "gui" ]]; then
    echo "Starting GUI + ML environment..."
    docker run -it --rm \
        --gpus all \
        --ipc=host \
        -v "$(pwd):/workspace" \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v /mnt/wslg:/mnt/wslg \
        -e DISPLAY="$DISPLAY" \
        -e WAYLAND_DISPLAY="$WAYLAND_DISPLAY" \
        -e XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" \
        -e PULSE_SERVER="$PULSE_SERVER" \
        "$IMAGE_NAME"
else
    echo "Starting clean ML environment (Jupyter port 8888 enabled)..."
    docker run -it --rm \
        --gpus all \
        --ipc=host \
        -p 8888:8888 \
        -v "$(pwd):/workspace" \
        "$IMAGE_NAME"
fi
