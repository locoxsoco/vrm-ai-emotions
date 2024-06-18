# Blender VRM Facial Animation Addon

Welcome to the **Blender VRM Facial Animation Addon** repository! This project has started as part of the Generative AI Agents Developer Contest by NVIDIA and LangChain. This addon allows to create facial animations for VRM avatars using prompts. By leveraging the power of a language model (LLM), you can generate blendshape values that bring your avatars to life with expressive and dynamic facial expressions.

## Table of Contents

- [Blender VRM Facial Animation Addon](#blender-vrm-facial-animation-addon)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation Windows](#installation-windows)
  - [Usage](#usage)
  - [Demo](#demo)
  - [Contributing](#contributing)

## Introduction

Creating realistic facial animations for VRM avatars can be a challenging and time-consuming task. This is even becomes more difficult if the vrm avatar hasn't been created by its user, since there is no strict format.

This addon simplifies the process by allowing users to describe the desired facial expressions in plain English (and interesting results in other languages too). Thanks to langchain, it's very easy to communicate with a language model and generate the appropriate blendshape values, which is later processed to create lifelike animations.

## Installation Windows

1. **Download the Portable Blender Version with the Addon**
   - [Download Here](https://github.com/locoxsoco/vrm-ai-emotions/releases/tag/v0.1.1)

2. **Unzip and Use**
   - Unzip the downloaded file.
   - Open the unzipped folder.
   - Run the Blender executable.

## Usage

1. **Load Your VRM Avatar**
   - There is a VRM loaded in the default startup file ready for testing, but if you want to add your custom model, delete it and import your VRM avatar into Blender.

2. **Access the Addon**
   - Navigate to the `AI Face Animator` tab in the panel section.

3. **Click on the avatar face**
   - Let the addon know which object is the face to animate.

4. **Create a Facial Animation**
   - In the text input field `API Key`, add the NVIDIA key to access to NVIDIA NIM.
   - In the text input field `Prompt`, type a description of the desired facial expression. For example, "smile with eyes closed", "Blink softly", "Eating pizza", "Happy", "Worried", "Angry", "Feeling dizzy", etc.
   - Click the "Generate animation" button.
   - The addon will communicate with the LLM and automatically apply the generated blendshape values to your avatar. When finished, press space to see the animation.

## Demo

Check out this demo to see the addon in action!

https://github.com/locoxsoco/vrm-ai-emotions/assets/29546841/d6c62074-7ac3-46cb-8d77-468684f7a4c6


In this demo, we demonstrate how to create a series of facial expressions using simple text prompts. You'll see how the addon interprets each prompt and generates realistic facial animations for a VRM avatar.

## Contributing

We welcome contributions to enhance the functionality and features of this addon. To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

Please ensure your code follows the project's coding standards and include relevant tests.

---

Thank you for using the Blender VRM Facial Animation Addon! We hope this tool makes it easier for you to create stunning facial animations for your VRM avatars. If you have any questions or feedback, feel free to open an issue in the repository. Happy animating!
