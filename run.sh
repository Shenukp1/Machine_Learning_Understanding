#!/usr/bin/env bash

# going to make it to "ml" stage unless "gui" is passed as an argument
MODE="${1:-ml}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/src"

mkdir -p "$SRC_DIR"

if [[ "$MODE" == "gui" ]]; then
    IMAGE_NAME="ml-assignment:gui"
    TARGET="gui"
else
    IMAGE_NAME="ml-assignment:ml"
    TARGET="ml"
fi

# Build if the image doesn't exist yet, otherwise ask if the user wants to rebuild
# TODO(shenukp1) Nov 11, 2026: maybe it is the case we actually force rebuild every time for reproducibility
if [[ "$(docker images -q "$IMAGE_NAME" 2> /dev/null)" == "" ]]; then
    echo "Building $IMAGE_NAME (target: $TARGET)..."
    docker build --target "$TARGET" -t "$IMAGE_NAME" "$SCRIPT_DIR"
else
    read -rp "Image $IMAGE_NAME already exists. Rebuild? [y/N] " REBUILD
    if [[ "$REBUILD" =~ ^[Yy]$ ]]; then
        echo "Rebuilding $IMAGE_NAME (target: $TARGET)..."
        docker build --target "$TARGET" -t "$IMAGE_NAME" "$SCRIPT_DIR"
    fi
fi

# Run the chosen container
# We run at user and we make /tmp as HOME s.t. everything
# is not written to root directory
if [[ "$MODE" == "gui" ]]; then
    echo "Starting GUI + ML environment..."
    docker run -it --rm \
        --user "$(id -u):$(id -g)" \
        --gpus all \
        --ipc=host \
        -v "$SRC_DIR:/workspace" \
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
        --user "$(id -u):$(id -g)" \
        --gpus all \
        --ipc=host \
        -p 8888:8888 \
        -v "$SRC_DIR:/workspace" \
        "$IMAGE_NAME"
fi
