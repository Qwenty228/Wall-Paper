# Wallpaper Engine

This is a customizable wallpaper engine built with `pygame`, `moderngl`, and `tkinter`, allowing for animated and dynamic wallpapers. It integrates background rendering using shaders, video processing, and various template animations, providing an interactive UI to control the behavior of the wallpaper engine.

## Features

- **Rendering Backend**: 
  - **`pygame`** for 2D animations and videos.
  - **`moderngl`** for GPU-accelerated shader-based animations.
  
- **Animations**:
  - **Shaders**: The `shaders/` folder contains animation code written in GLSL, which is executed with `moderngl`.
  - **Templates**: Basic animations written in Python using `pygame` reside in the `template/` folder.
  - **Video Support**: Videos are handled using `imageio` and drawn onto the surface using `pygame`.
  
- **UI Interface**: 
  - Built using `tkinter` and `customtkinter` to provide a responsive GUI.
  - Includes a sidebar for switching between different animation modes and adjusting settings like appearance and scaling.

- **Background Integration**:
  - Uses `pywin32` to clip the `pygame` display into the Windows desktop background. This allows the wallpaper engine to run seamlessly behind other applications, as if it were a native desktop background.


## Setup

1. **Install Dependencies**:
   Make sure you have Python 3.8+ installed. Install the necessary packages by running:

   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Application**:
   You can start the wallpaper engine by running the `app.py` file:

   ```bash
   python app.py
   ```

3. **Customization**:
   - You can add custom shader files in the `anim/data/shaders/` folder.
   - Add new pygame-based animation templates in the `anim/data/template/` folder.
   <!-- - Add video files to `anim/data/videos/` for video wallpapers. -->


