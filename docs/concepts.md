# Core Concepts

This document defines the fundamental concepts used throughout the Room Observer project. These definitions provide a shared vocabulary for the architecture, implementation, and documentation.

The concepts are presented in the order they appear throughout the observation pipeline, from the physical environment to the reasoning layer.
> Concepts describe the responsibilities and meaning of entities within the system rather than their current implementation. Definitions should remain valid as the project evolves and new technologies are introduced.

## `Space`

### Definition

A Space is a physical environment that can be observed by the system. It represents the highest-level entity within the observation pipeline and serves as the context in which all observations, objects, and events occur.

### Purpose

Spaces provide a logical boundary for organizing observations and maintaining independent world models. Although the initial implementation focuses on rooms, the concept is intentionally generic and can represent any observable physical environment.

### Relationships

- Contains Observations
- Contains Observed Objects
- Has one World Model
- Generates Events

## `Sensor`

### Definition

A Sensor is any source of information that allows the system to perceive a physical environment. Sensors provide the raw input from which observations are generated.

### Purpose

Sensors act as the interface between the physical world and the perception system. They collect information about a Space and enable the observer to build an understanding of its environment.

### Relationships

- Observes a Space
- Produces data used to create an Observation

## `Observation`

### Definition

An Observation represents the information collected during a single perception cycle within a Space. It combines the data gathered from one or more sensors into a unified representation of what the system perceived at a specific moment in time.

### Purpose

Observations serve as the evidence used to update the system's understanding of an environment. They provide a time-specific snapshot of perception without representing the system's long-term knowledge or beliefs.

### Relationships

- Belongs to a Space
- Is created from one or more Sensors
- Contains one or more Detections
- Is used to update the World Model
- May generate Events

## `Detection`

### Definition

A Detection is the raw output produced by the perception pipeline after processing an Observation. It represents a possible entity identified within the observed environment.

### Purpose

Detections provide evidence about the entities that may exist within a Space. They are an intermediate representation between raw perception and the system's internal understanding.

### Relationships

- Belongs to an Observation
- May correspond to an Observed Object
- Is used to update the World Model

## `Observed Object`

### Definition

An Observed Object is the system's internal representation of a physical entity within a Space. It combines information gathered from multiple observations to maintain a persistent identity over time.

### Purpose

Observed Objects allow the system to recognize entities across multiple observations, maintain historical information, and reason about changes affecting individual objects.

### Relationships

- Exists within a Space
- Is inferred from one or more Detections
- Exists within the World Model
- May be involved in Events

## `World Model`

### Definition

The World Model is the system's internal representation of a Space. It maintains the observer's current understanding of the environment based on accumulated observations and previous knowledge.

### Purpose

The World Model represents the system's current belief about the environment. Rather than relying on individual observations, it continuously updates its understanding as new evidence becomes available.

### Relationships

- Belongs to a Space
- Contains Observed Objects
- Is updated using Observations
- Generates Events
- Is queried during Reasoning

## `Event`

### Definition

An Event represents a meaningful change detected within the World Model between observations.

### Purpose

Events summarize significant changes in an environment, allowing the system to reason about how a Space evolves over time without relying on every individual observation.

### Relationships

- Occurs within a Space
- Is generated from changes in the World Model
- May involve one or more Observed Objects
- Is stored in Memory

## `Memory`

### Definition

Memory is the persistent storage of information acquired by the system over time. It preserves knowledge beyond individual observations and supports long-term understanding of a Space.

### Purpose

Memory enables the system to retain historical observations, events, and object information, allowing it to reason about past and present states of an environment.

### Relationships

- Stores World Models
- Stores Observations
- Stores Events
- Supports Reasoning

## `Reasoning`

### Definition

Reasoning is the process of interpreting the system's current understanding of a Space in order to answer questions, explain observations, or support decision-making.

### Purpose

Reasoning transforms stored knowledge into useful information by combining the World Model, Memory, and current observations to produce meaningful conclusions.

### Relationships

- Uses the World Model
- Uses Memory
- May use current Observations
- Produces responses or decisions