# System Architecture

## Overview

Space Observer is designed as an artificial observation system that continuously perceives and maintains an understanding of a physical environment.

The system is built around the idea that intelligent observation requires more than detecting objects in individual frames. Similar to how humans observe the world, Space Observer must combine sensory input, persistent understanding, memory, and reasoning in order to interpret changes and answer questions about the environment.

To achieve this, the system is divided into four major subsystems: Perception, World Model, Memory, and Reasoning. Perception transforms raw sensory information into meaningful detections. The World Model maintains the system's current understanding of the environment. Memory preserves historical information and past events. Reasoning uses both current and historical knowledge to answer questions and derive conclusions.

This separation allows the system to evolve its perception methods, understanding mechanisms, and reasoning capabilities independently while maintaining a consistent representation of the observed world.

## Architectural Principles

### **Separation of Responsibilities**

Each subsystem has a clearly defined responsibility and should avoid taking ownership of concerns that belong to other parts of the system.

Perception is responsible for transforming sensory information into detections.  
The World Model is responsible for maintaining the current understanding of the environment.  
Memory is responsible for preserving historical information.  
Reasoning is responsible for using available knowledge to answer questions and derive conclusions. 

This separation prevents individual components from becoming overly complex and allows the system to evolve more easily.

### **Modularity and Replaceability**

Subsystems should communicate through well-defined interfaces rather than relying on specific implementations.

For example, the World Model should not depend on how detections are produced. Whether detections come from a YOLO model, another computer vision model, or a different sensing technology, the World Model should receive the same standardized information.

This allows individual components to be improved or replaced without requiring changes throughout the entire system.

### **Persistent Understanding Over Individual Observations**

Space Observer is not designed as a collection of independent image analyses. The system should maintain a continuous understanding of an environment over time.

Individual observations provide new information, but the World Model is responsible for combining this information into a persistent representation of the observed world.

### **Independent Testability**

Each subsystem should be testable independently whenever possible.

Perception by providing images and evaluating produced detections.  
The World Model by using simulated detections.  
Memory by using generated events and historical data.  
Reasoning by using predefined world states and memories.

This allows development to progress incrementally without requiring the entire system to be operational.

### **Scalability of Environments**

The architecture should not be tied to a specific room or physical space.

A bedroom, kitchen, office, or any other environment should be represented using the same underlying concepts. Adding a new environment should be a matter of providing new observations rather than modifying the architecture.

The system represents environments through generic concepts such as Spaces, Objects, Observations, Events, and Relationships rather than environment-specific structures. This allows new environments to be introduced without architectural changes.

## High-Level Architecture

Space Observer is organized into four major subsystems: Perception, World Model, Memory, and Reasoning.

Each subsystem represents a different capability required for artificial observation. The subsystems communicate through defined boundaries, allowing each component to evolve independently while contributing to the overall understanding of the observed environment.

                 Space Observer


        ┌──────────────────────────────┐
        │                              │
        │   Perception Subsystem       │
        │   (Sensory Input)            │
        │                              │
        └──────────────┬───────────────┘
                       │
                       │ Detections
                       ▼
        ┌──────────────────────────────┐
        │                              │
        │   World Model Subsystem      │
        │   (Current Understanding)    │
        │                              │
        └──────────────┬───────────────┘
                       │
                       │ Events / History
                       ⇅
        ┌──────────────────────────────┐
        │                              │
        │   Memory Subsystem           │
        │   (Past Knowledge)           │
        │                              │
        └──────────────────────────────┘



        ┌──────────────────────────────┐
        │                              │
        │   Reasoning Subsystem        │
        │   (Decision & Interaction)   │
        │                              │
        └──────────────┬───────────────┘
                       │
         Reads current + past knowledge

                       ▲
                       │
             ┌─────────┴─────────┐
             │                   │
        World Model            Memory

### **Perception Subsystem**

The Perception Subsystem is responsible for converting raw sensory information into meaningful detections.

It represents the sensory capabilities of Space Observer. This subsystem receives information from sensors such as cameras and processes this information through an observation and detection pipeline.

Its responsibility ends once standardized detections are produced.

The Perception Subsystem does not maintain knowledge about the environment, store history, or perform reasoning.

Example:

Input:
- Camera frame

Output:
- Laptop detected at position X
- Mug detected at position Y

### **World Model Subsystem**

The World Model Subsystem represents the current understanding of the observed environment.

It receives detections from the Perception Subsystem and combines them with existing knowledge to maintain a persistent representation of the current state of the world.

The World Model is responsible for understanding entities over time, such as recognizing that multiple detections correspond to the same object.

It also identifies meaningful changes between previous and updated states, producing events when appropriate.

Example:

Previous state:
- Laptop located on desk

New detection:
- Laptop located on bed

Result:
- Update current state
- Generate "Laptop moved" event

### **Memory Subsystem**

The Memory Subsystem preserves information about the past.

While the World Model represents what is currently believed to be true, Memory stores historical knowledge such as events, previous observations, and past states.

Memory allows the system to answer questions that require historical context.

Example:

Question:
"Where was my laptop yesterday?"

The World Model provides:
- Current laptop location

Memory provides:
- Previous laptop locations and movements

### **Reasoning Subsystem**

The Reasoning Subsystem allows Space Observer to answer questions and derive conclusions using available knowledge.

It does not directly observe the environment. Instead, it relies on the World Model for current information and Memory for historical context.

This separation allows reasoning capabilities to evolve independently from perception and storage mechanisms.

Example:

Question:
"Did anything change in the kitchen today?"

Reasoning uses:
- Current kitchen state from World Model
- Past events from Memory

Output:
- "The mug was moved from the counter to the table at 14:32."

## Data Flow

Space Observer operates as a continuously running system where different subsystems perform their responsibilities independently while sharing information through defined boundaries.

The primary information flow begins with the Perception Subsystem, which receives sensory input and transforms it into standardized detections. These detections are then provided to the World Model Subsystem, which integrates new information with its current understanding of the environment.

When changes between previous and updated states are identified, meaningful transitions are represented as events and provided to the Memory Subsystem for historical storage.

The Reasoning Subsystem does not depend on new observations to operate. Instead, it uses the current state provided by the World Model and historical information provided by Memory to answer questions and derive conclusions.

The general flow is:
```
Sensor Input
↓
Observation
↓
Detections
↓
World Model Update
↓
Events / Updated State
↓
Memory

Reasoning
↓
World Model + Memory
↓
Response
```

## Future Considerations

The current architecture defines the core responsibilities and interactions between major subsystems. However, several implementation decisions will be explored as development progresses.

Possible future considerations include:

- Different perception models and sensing technologies.
- More advanced object tracking and identification methods.
- Richer world representations such as relationship graphs.
- Long-term memory strategies and information retention policies.
- Integration with robotic systems and physical interaction capabilities.
- More advanced reasoning capabilities.