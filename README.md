# Autonomous Agents and Multi-Agent Systems: Project
# OpenAI - Hide and Seek

## Scope

The purpose of this project is to experiment on the OpenAI Hide and Seek system with different types of multiagent designs.

## Project structure

See the file _Final Report.pdf_ for the complete description of the assignement and results.

### policies

The policies folder contains the agent policies developed for this project.

### environments

The environments folder contains all the environments that are experimented with in this project

## setup 

This project depends on the openai hide and seek repository, which is built on the Mujoco physics engine. To run the project, follow the installation instructions at https://github.com/openai/multi-agent-emergence-environments

## running

To run an example, type the following command in the console:

bin/examine.py examples/hide_and_seek_quadrant.jsonnet examples/hide_and_seek_quadrant.npz
