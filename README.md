# Smart Wireless Simulator

This program simulates a self-configuring wireless network where the nodes try to find an energy optimal distribution of access point nodes and stations and to achieve full connectivity (all nodes reachable from any other).

The constraints are:
 - limited visibility between nodes
 - each access point can serve at most N stations
 - each node has limited battery life
 - each node can act as both station and access point at the same time.

 ## Dependencies
 Python3

 ## Run
 Example:
 *$: python3 main.py my_config debug*

 Where my_config.cfg is the name of a text file containing the configuration required
 by the current experiment. All the configuration files have to be placed in ./config/ folder.

 You do not need to add .cfg on the command line when you start the program,
 just the name (i.e. my_config) is fine.

 Each config file must contain 1 line with the world configuration and multiple
 lines with nodes and wall configuration.
 All the text which is not included in {} is ignored by the parser and can
 be used as comments.

 Example:

 -------------------------------------------------------------------------------
 ```
 World parameters:
 
 {world: width= 10, height= 10, v_threshold= 5}

 Agents parameters:
 
 {agent: mac= 1, x= 2, y= 2}
 {agent: mac= 2, x= 5, y= 5}
 {agent: mac= 3, x= 8, y= 6}
 {agent: mac= 4, x= 1, y= 7}

 Walls:

 {wall: x= 3, y= 4}
 {wall: x= 4, y= 4}
 {wall: x= 5, y= 4}
 ```
 -------------------------------------------------------------------------------
 "World parameters:", "Agent parameters:" and "Walls:" are documentation strings
 ignored by the parser.

 Optionally you can add "debug" (without quotes) as third parameter to start
 an interactive simulation.
 While in debug mode you can remove nodes with the command "kill n", where n
 is the node address, or stop the simulation with the command "quit".
 It is important to properly quit the simulation to save the partial results
 in the result file.
 All other text will be ignored.

 The simulation ends automatically when no nodes are present anymore.
 
 -------------------------------------------------------------------------------
License:
 **See ./documents/license.pdf**
